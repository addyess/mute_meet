#!/usr/bin/env python3
import sys
import backend.ws_serve as ws_server
import backend.ht_serve as ht_server


if 'http' in sys.argv:
    ht_server.run()
if 'ws' in sys.argv:
    ws_server.run()
