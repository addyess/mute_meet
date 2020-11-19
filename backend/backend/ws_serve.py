#!/usr/bin/env python3

import asyncio
import json
import logging
import websockets

from backend.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def mute_meet(websocket, _path):
    """Handle an opened socket."""
    user, purpose, uuid = await User.register(websocket)
    try:
        await user.notify_controllers()
        async for message in websocket:
            data = json.loads(message)
            logout = data.get("logout")
            action = data.get("action")
            if logout:
                break
            if action:
                uuid, device = action.get('uuid'), action.get('device')
                await user.mute(uuid, device)
    finally:
        await user.unregister(websocket)


def run():
    start_server = websockets.serve(mute_meet, "", 8001)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
