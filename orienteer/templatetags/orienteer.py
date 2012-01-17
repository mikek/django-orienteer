# Copyright 2010 Sentinel Design. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Simple Compass integration for Django'''

__author__ = 'Drew Yeaton <drew@sentineldesign.net>'
__version__ = '0.2'


import os
import re
import sys
import subprocess

from django import template
from django.conf import settings


def run(cmd):
    """Return (status, output) of executing cmd."""
    pipe = subprocess.Popen(cmd, shell=False, universal_newlines=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = str.join('', pipe.stdout.readlines())
    sts = pipe.wait()
    if sts is None:
        sts = 0
    return sts, output

register = template.Library()

@register.simple_tag
def compass(filename, media):
    binary = settings.COMPASS_BIN
    output_dir = settings.COMPASS_OUTPUT_DIR
    output_url = settings.COMPASS_OUTPUT_URL
    project_dir = settings.COMPASS_PROJECT_DIR
    source_dir = getattr(settings, 'COMPASS_SOURCE_DIR', 'src')
    extra_opts = re.split("\s", getattr(settings, 'COMPASS_EXTRA_OPTS', ''))
    use_timestamp = getattr(settings, 'COMPASS_USE_TIMESTAMP', True)
    debug = getattr(settings, 'COMPASS_DEBUG', settings.TEMPLATE_DEBUG)

    # get timestamp of css, if it doesn't exist we need to make it
    try:
        output_file_stat = os.stat(os.path.join(project_dir, output_dir, filename + '.css'))
        output_file_ts = output_file_stat.st_mtime
    except OSError:
        output_file_ts = 1

    source_file_ts = 0

    for root, dirs, files in os.walk(os.path.join(project_dir, source_dir)):
        for source_file in files:
            if source_file[-5:].lower() == '.scss':
                source_file_stat = os.stat(os.path.join(root, source_file))
                if source_file_stat.st_mtime > source_file_ts:
                    source_file_ts = source_file_stat.st_mtime

    needs_update = source_file_ts > output_file_ts

    css = "<link rel='stylesheet' href='%s%s' type='text/css' media='%s'/>" % \
          (output_url + filename + '.css',
           use_timestamp and '?%s' % output_file_ts or '',
           media)

    if not settings.TEMPLATE_DEBUG or not needs_update:
        return css

    cmd = [binary, 'compile', '--css-dir', output_dir,
           '--sass-dir', source_dir, project_dir]
    # avoid passing empty options in cmd array
    if extra_opts:
        cmd.extend(extra_opts)
    if debug:
        sys.stderr.write(' '.join(cmd))
    (status, output) = run(cmd)
    if output:
        for line in re.split("\n+", output.strip()):
            sys.stderr.write(re.sub(r'^', '[Compass] ', line) + "\n")

    return css
