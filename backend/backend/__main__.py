#!/usr/bin/env python3
import sys
import backend.ws_serve as ws_server


if 'ws' in sys.argv:
    ws_server.run()
