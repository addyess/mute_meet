Web Server Configs
-------------------

lighttpd
=========
Here's the working lighttpd config i used for my backend services
* a webserver hosted on :443
* a virtual-host using fqdn to resolve to the right `www` directory
* the websocket is reachable over the same socket at a proxied URI
