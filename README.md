iCloud Tabs Updater
==================

Update iCloud tabs without Safari.

**This may mess up your iCloud account! Use at your own risk.**

Try it
-------
```bash
$ pip install -r requirements.txt
$ mv update_config.py.template update_config.py
```

Fill in your credentials in update_config.py (see the Config section below).
Then edit the tabs list in update.py and run the following to upload new tabs to iCloud:
```bash
$ python update.py
```

Config
------
Most constants for update_config.py can be grabbed from watching requests with mitmproxy:

```bash
$ pip install mitmproxy
$ mitmproxy -p 8080 
```
Set your proxy settings to use 8080, open Safari and watch for requests to `keyvalueservice.icloud.com`.


Chrome Extension
----------------
Send currently open Chrome tabs to iCloud every 5 minutes.

After filling in update_config.py, run the simple server:

```bash
$ python server.py
```

Then, load the chrome extension in the chrome_extension/ directory:

- Open `chrome://extensions/`
- Check the developer mode checkbox. 
- Click `Load Unpacked Extension`.
- Navigate to the chrome_extension/ directory and select it.
