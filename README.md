iCloud Tabs Updater
==================

Update iCloud tabs without Safari.

Instructions
------------
Fill your credentials in in update_config.py, edit the tabs list in update.py and run:

```bash
$ python update.py
```

Most constants can be grabbed from watching requests with mitmproxy:

```bash
$ pip install mitmproxy
$ mitmproxy -p 8080 
```
Set your proxy settings to use 8080, open safari and watch for requests to keyvalueservice.icloud.com.
