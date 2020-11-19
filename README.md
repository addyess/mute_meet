Mute Meet
=========

Why
---
I wanted to use my phone to mute/unmute a google meet where a chromebook is on
my TV.  I don't want to get up -- so i wrote this.

How
---
Run the 'backend' apps on a computer somewhere in your house -- even on that 
laptop on the TV is possible

### Start Controller
```bash
cd backend/
virtualenv -m python3 venv
. venv/bin/activate
pip install -r requirements.txt
python -m backend http &  # starts a simple http server, access it from your phone
python -m backend ws &    # creates a websocket server the extension and controller accesses
```

### Load Extension
* Follow [Google's instructions](https://developer.chrome.com/extensions/getstarted) for loading the extension

### Future
* Create a NORMAL extension to load from the Google Store
* Automate starting the controller
