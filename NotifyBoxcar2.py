#!/usr/bin/env python

###########################################################################
### NZBGET QUEUE/POST-PROCESSING SCRIPT
### QUEUE EVENTS: NZB_ADDED

# NZBGet notifications.
#
# The script will send a notification to Boxcar 2.
#
# Info about this notify script:
# URL: https://github.com/srod/nzbget-boxcar2.
# Author: Rodolphe Stoclin (srodolphe@gmail.com).
# Date: Fri, Jul 17th, 2015.
# License: MIT.
# Script Version: 1.0.0
#

###########################################################################
### OPTIONS

# Boxcar 2 token.
#
# Your Boxcar 2 token
#Token=

# Message queue.
#
# The message to be sent on queue notification
#MessageQueue=Snatched:

# Message download.
#
# The message to be sent on download notification
#MessageDownload=Downloaded:

### NZBGET QUEUE/POST-PROCESSING SCRIPT
###########################################################################

import os
import sys
import httplib
import urllib

# NZBGet exit codes
NZBGET_SUCCESS = 93
NZBGET_ERROR = 94
NZBGET_NONE = 95

# Check if the script is called from nzbget 11.0 or later
NZBGetVersion = os.environ['NZBOP_VERSION']
if NZBGetVersion[0:5] < '11.1':
    print('[ERROR] This script requires NZBGet 11.1 or newer. Please update NZBGet')
    sys.exit(NZBGET_ERROR)

token = os.environ['NZBPO_TOKEN']
messageQueue = os.environ['NZBPO_MESSAGEQUEUE']
messageDownload = os.environ['NZBPO_MESSAGEDOWNLOAD']
server = 'new.boxcar.io'
rootPath = '/api/notifications'

def send_request(path):
    httpServ = httplib.HTTPSConnection(server)
    httpServ.connect()
    httpServ.request('POST', path)
    response = httpServ.getresponse()
    httpServ.close()
    if response.status == 201:
        print('notification sent')
        sys.exit(NZBGET_SUCCESS)
    elif response.status == 401:
        print('[ERROR] Notification failed. Please check your boxcar 2 token')
        sys.exit(NZBGET_ERROR)
    else:
        print('[ERROR] Notification failed.', response.status, response.reason)
        sys.exit(NZBGET_ERROR)

def notify_queue():
    params = {
        'user_credentials': token,
        'notification[title]': messageQueue + ' ' + os.environ['NZBNA_NZBNAME']
    }
    path = rootPath + '?' + urllib.urlencode(params)
    send_request(path)

def notify_download():
    params = {
        'user_credentials': token,
        'notification[title]': messageDownload + ' ' + os.environ['NZBPP_NZBNAME']
    }
    path = rootPath + '?' + urllib.urlencode(params)
    send_request(path)

if os.environ.get('NZBNA_EVENT') in ['NZB_ADDED']:
    notify_queue()
else:
    notify_download()

sys.exit(NZBGET_NONE)
