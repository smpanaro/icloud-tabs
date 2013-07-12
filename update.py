# Format of request:
# {
#   "apns-token": "<data>",
#   "apps": [
#     {
#       "bundle-id": "com.apple.Safari",
#       "keys": [
#         {
#           "data": "<data>",
#           "name": ""
#         }
#       ],
#       "kvstore-id": "com.apple.Safari.SyncedTabs",
#       "registry-version": ""
#     }
#   ],
#   "service-id":"iOS"
# }

# Format of "keys" <data> blob:
# {
#   "DeviceName": "",
#   "LastModified": "YYYY-MM-DDTHH:MM:SSZ",
#   "Tabs": [
#     {
#       "Title": "",
#       "URL": ""
#     }
#   ]
# }

import urllib2

import StringIO
import gzip

import plistlib
import biplist
import base64
from time import strftime, gmtime
import uuid

import os

from update_config import *

# Request Header Constants
HOST = "p02-keyvalueservice.icloud.com"
USER_AGENT = "SyncedDefaults/43.27 (Mac OS X 10.8.4 (12E55))"
X_MME_CLIENT_INFO = "<MacBookAir4,2> <Mac OS X;10.8.4;12E55> <com.apple.SyncedDefaults/43.27>"
X_APPLE_REQUEST_UUID = str(uuid.uuid4())
X_APPLE_SCHEDULER_ID = "com.apple.syncedpreferences.browser"

def generate_plist(with_payload, tabs, registry_version="need-something-here"):
    b = {
          "DeviceName": DEVICE_NAME,
          "LastModified": strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
          "Tabs": tabs
        }

    # Write b into a binary plist and base64 encode it.
    out = StringIO.StringIO()
    biplist.writePlist(b, out)
    b_encoded = "".join(map(chr, [1, 0, 0, 0, 0,  0, 0, 23, 0, 0, 0, 0])) + out.getvalue()

    p = {
          "apns-token": plistlib.Data(APNS_TOKEN),
          "apps": [
            {
              "bundle-id": "com.apple.Safari",
              "keys": [
                {
                  "data": plistlib.Data(b_encoded),
                  "name": DEVICE_UUID # a unique id for your device
                }
              ],
              "kvstore-id": "com.apple.Safari.SyncedTabs",
              "registry-version": registry_version, # no idea
            }
          ],
          "service-id":"iOS"
        }

    if with_payload == False:
      p["apps"][0].pop("keys")

    # Write p into a regular plist and return its string value.
    out = StringIO.StringIO()
    plistlib.writePlist(p, out)
    return out.getvalue()


def dogzip(s):
    out = StringIO.StringIO()
    f = gzip.GzipFile(fileobj=out, mode='w')
    f.write(s)
    f.close()
    return out.getvalue()

def ungzip(s):
    data = StringIO.StringIO(s)
    gzipper = gzip.GzipFile(fileobj=data)
    html = gzipper.read()
    return html

def make_request(body):
  URL = "https://p02-keyvalueservice.icloud.com/sync"

  zippedbody = dogzip(body)

  request = urllib2.Request(URL, headers={
      "Host": HOST,
      "User-Agent" : USER_AGENT,
      "Accept": "*/*",
      "Content-Encoding": "gzip",
      "X-MMe-Client-Info": X_MME_CLIENT_INFO,
      "X-Apple-Request-UUID": X_APPLE_REQUEST_UUID,
      "X-Apple-Scheduler-ID": X_APPLE_SCHEDULER_ID,
      "Accept-Language": "en-us",
      "Accept-Encoding": "gzip, deflate",
      "Content-Type": "application/x-www-form-urlencoded",
      "Authorization": AUTHORIZATION,
      "Connection": "keep-alive",
      "Proxy-Connection": "keep-alive",
      "Content-Length": len(zippedbody)
      }, 
      data=zippedbody)

  u = urllib2.urlopen(request)
  data = u.read()

  return ungzip(data)


if __name__ == '__main__':
  TABS = [
          {
            "Title": "XKCD",
            "URL": "http://xkcd.com/"
          },
          {
            "Title": "Stuff on Cats",
            "URL": "http://stuffonmycat.com/"
          }
        ]

  # First make an empty (without tab data) request to get the latest registry string.
  payload_plist = generate_plist(False, [])
  response = make_request(payload_plist)
  response_plist = plistlib.readPlistFromString(response)

  registry_version = response_plist["apps"][0]["registry-version"]

  # Next use that string to make a request with a payload of tabs.
  payload_plist = generate_plist(True, TABS, registry_version=registry_version)
  make_request(payload_plist)
