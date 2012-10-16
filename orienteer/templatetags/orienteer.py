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
__version__ = '0.3'


import os
import re
import sys
import subprocess
from datetime import datetime
from time import mktime

from django import template
from django.conf import settings


def run(cmd, cwd=None):
    """Return (status, output) of executing cmd."""
    pipe = subprocess.Popen(cmd, shell=False, executable=cmd[0], cwd=cwd,
                            universal_newlines=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    output = str.join('', pipe.stdout.readlines())
    sts = pipe.wait()
    if sts is None:
        sts = 0
    return sts, output

register = template.Library()


@register.simple_tag
def compass(filename, media):
    project_dir = settings.COMPASS_PROJECT_DIR
    ruby_binary = getattr(settings, 'COMPASS_RUBY_BIN', '')
    compass_script = getattr(settings, 'COMPASS_SCRIPT', 'compass')
    output_dir = getattr(settings, 'COMPASS_OUTPUT_DIR', './')
    source_dir = getattr(settings, 'COMPASS_SOURCE_DIR', 'src')
    use_timestamp = getattr(settings, 'COMPASS_USE_TIMESTAMP', True)
    skip_on_equal_timestamp = getattr(settings,
                                      'COMPASS_SKIP_ON_EQUAL_TIMESTAMP',
                                      False)
    debug = getattr(settings, 'COMPASS_DEBUG', settings.DEBUG)

    output_url = getattr(settings, 'COMPASS_OUTPUT_URL', None)
    if not output_url and settings.STATIC_URL:
        output_url = '%scss/' % settings.STATIC_URL

    extra_opts_str = getattr(settings, 'COMPASS_EXTRA_OPTS', '')
    extra_opts = []
    # avoid passing empty options in cmd array
    if extra_opts_str:
        extra_opts = re.split("\s", extra_opts_str)

    # get timestamp of css, if it doesn't exist we need to make it
    try:
        output_file_stat = os.stat(os.path.join(project_dir, output_dir,
                                                filename + '.css'))
        output_file_ts = output_file_stat.st_mtime
    except OSError:
        output_file_ts = 0

    ts = ''
    if use_timestamp:
        # generate timestamp on the fly if there is no target file yet
        if output_file_ts:
            ts = '?%s' % output_file_ts
        else:
            ts = '?%s' % mktime(datetime.now().timetuple())
    css = "<link rel='stylesheet' href='%s%s' type='text/css' media='%s'/>" %\
          (output_url + filename + '.css', ts, media)

    # do not try to find source file if we are not debugging templates
    if not settings.TEMPLATE_DEBUG:
        return css

    source_file_ts = 0
    for root, dirs, files in os.walk(os.path.join(project_dir, source_dir)):
        for source_file in files:
            if source_file[-5:].lower() == '.scss':
                source_file_stat = os.stat(os.path.join(root, source_file))
                if source_file_stat.st_mtime > source_file_ts:
                    source_file_ts = source_file_stat.st_mtime

    if ((source_file_ts < output_file_ts) or
            (skip_on_equal_timestamp and source_file_ts == output_file_ts)):
        return css

    cmd = [compass_script, 'compile', '--css-dir', output_dir,
           '--sass-dir', source_dir, project_dir]
    if ruby_binary:
        cmd.insert(0, ruby_binary)
    cmd.extend(extra_opts)

    if debug:
        sys.stderr.write(' '.join(cmd) + "\n")
    (status, output) = run(cmd)
    if output:
        for line in re.split("\n+", output.strip()):
            sys.stderr.write(re.sub(r'^', '[Compass] ', line) + "\n")

    return css
