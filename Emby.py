#!/usr/bin/env python
#
# Copyright (C) 2017 Gunnar Lilleaasen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###

# Updates an Emby movie library.
#
# This is a script for notifying an Emby media server to update the
# movie library with any newly added movies.
#
# NOTE: The script should run after sorting scripts such as VideoSort.

##############################################################################
### OPTIONS                                                                ###

# Host address of the Emby server.
#
#Host=localhost:8096

# API key for Emby.
#
#ApiKey=

### NZBGET POST-PROCESSING SCRIPT                                          ###
##############################################################################

#import urllib
import urllib.request

import sys
import os
import json
import time

time.sleep(5)

# Exit codes used by NZBGet
POSTPROCESS_SUCCESS=93
POSTPROCESS_NONE=95
POSTPROCESS_ERROR=94

host = os.environ['NZBPO_HOST']
apikey = os.environ['NZBPO_APIKEY']
startdir = os.environ['NZBPP_DIRECTORY'].replace('/downloads/nzbget/completed', '')

finaldir = '/mnt/googledrive{0}'.format(startdir)

url = '{0}/mediabrowser/Library/Media/Updated'.format(host)

print('[INFO] DIR: {0}'.format(finaldir))

myCommand = 'find {0}/*.mp4 -exec mv -vf {{}} {1}.mp4 \\;'.format(os.environ['NZBPP_DIRECTORY'], startdir)
print('[INFO] CMD: {0}'.format(myCommand))

os.system(myCommand)

myCommand = 'find {0}/*.mkv -exec mv -vf {{}} {1}.mkv \\;'.format(os.environ['NZBPP_DIRECTORY'], startdir)
print('[INFO] CMD: {0}'.format(myCommand))

os.system(myCommand)

myCommand = 'find {0}/*.avi -exec mv -vf {{}} {1}.avi \\;'.format(os.environ['NZBPP_DIRECTORY'], startdir)
print('[INFO] CMD: {0}'.format(myCommand))

os.system(myCommand)


myCommand = 'find /Other/* -type d  -print -delete'
print('[INFO] CMD: {0}'.format(myCommand))

os.system(myCommand)

os.system('/config/scripts/keepnewest.sh /EPL 5')
os.system('/config/scripts/keepnewest.sh /Boxing 5')

data = {'Updates': [{'Path' : finaldir, 'UpdateType': 'Created'}]}
data = json.dumps(data)

try:
    req = urllib.Request(url, data)

    if apikey:
        req.add_header('X-MediaBrowser-Token', apikey)
        req.add_header('Content-Type', 'application/json')

    response = urllib.urlopen(req)
    result = response.read()
    response.close()

    print('[INFO] HTTP: {0}'.format(url))
    sys.exit(POSTPROCESS_SUCCESS)

except (urllib.error.URLError, IOError) as e:
    print('[ERROR] Couldn\'t reach Emby at {0}: {1}'.format(url, e))
    sys.exit(POSTPROCESS_ERROR)
