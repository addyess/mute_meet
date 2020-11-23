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

### Configure Controller
a `config.ini` file needs to be in the `backend` folder
it should contain a section like this
```ini
[gapi]
client_id = <yourclientid>.apps.googleusercontent.com
controllers = <id1-of-authorized-controller>,<id1-of-authorized-controller>,
```
If this file is missing, no worries -- anyone with access to your sight
will be a controller (obviously less secure)

### Start Controller
```bash
cd backend
make prepare
```

### Load Extension
* Build the extension
```bash
make build
```
* Follow [Google's instructions](https://developer.chrome.com/extensions/getstarted) for loading the extension

### Future
* Create a NORMAL extension to load from the Google Store
* Automate starting the controller
