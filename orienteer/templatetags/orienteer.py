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
from commands import getstatusoutput

from django import template
from django.conf import settings


register = template.Library()

@register.simple_tag
def compass(filename, media):
    proj_dir = settings.COMPASS_PROJECT_DIR
    source_dir = getattr(settings, 'COMPASS_SOURCE_DIR', 'src')
    output_dir = settings.COMPASS_OUTPUT_DIR
    output_url = settings.COMPASS_OUTPUT_URL
    quiet_mode = getattr(settings, 'COMPASS_QUIET', False)
    use_timestamp = getattr(settings, 'COMPASS_USE_TIMESTAMP', True)
    
    # get timestamp of css, if it doesn't exist we need to make it
    try:
        output_file_stat = os.stat(os.path.join(proj_dir, output_dir, filename + '.css'))
        output_file_ts = output_file_stat.st_mtime
    except OSError:
        output_file_ts = 1
    
    source_file_ts = 0
    
    for root, dirs, files in os.walk(os.path.join(proj_dir, source_dir)):
        for source_file in files:
            if source_file[-5:].lower() == '.scss':
                source_file_stat = os.stat(os.path.join(root, source_file))
                if source_file_stat.st_mtime > source_file_ts:
                    source_file_ts = source_file_stat.st_mtime
    
    needs_update = source_file_ts > output_file_ts
    
    css = "<link rel='stylesheet' href='%s%s' type='text/css' media='%s' />" % (output_url + filename + '.css', use_timestamp and '?%s' % output_file_ts or '', media)
    
    # if we aren't debugging (in production for example), short-cicuit this madness
    if not settings.TEMPLATE_DEBUG or not needs_update:
        return css
    
    cmd_dict = {
        'bin': settings.COMPASS_BIN, 
        'sass_style': settings.COMPASS_STYLE, 
        'project_dir': proj_dir,  
        'output_dir': output_dir, 
        'quiet_flag': quiet_mode and "--quiet" or ""
    }
    
    cmd = "%(bin)s compile %(quiet_flag)s -s %(sass_style)s --css-dir %(output_dir)s %(project_dir)s" % cmd_dict
    (status, output) = getstatusoutput(cmd)
    if output:
        for line in re.split("\n+", output):
            sys.stderr.write(re.sub(r'^', '[Compass] ', line) + "\n")
    
    return css
