#!/usr/bin/env python3

import asyncio
import configparser
import json
import logging
import websockets

from backend.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MuteMeetSocket:
    config = configparser.ConfigParser()

    @staticmethod
    def run():
        MuteMeetSocket.config.read('config.ini')
        start_server = websockets.serve(MuteMeetSocket.create, "", 8001)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    @staticmethod
    async def create(websocket, path):
        """Handle an opened socket."""
        try:
            message_str = await websocket.recv()
            msg = json.loads(message_str)
        except:
            logger.exception("Registration Error")
            raise

        if "get_client_id" in msg['type']:
            socket = CredsSocket(websocket, path)
        elif msg['type'] in ["controller", "extension", ""]:
            socket = UserSocket(websocket, path)
        else:
            return
        await socket.runtime(msg)

    def __init__(self, handle, path):
        self.handle = handle
        self.path = path

    async def runtime(self, first_msg):
        pass


class CredsSocket(MuteMeetSocket):
    async def runtime(self, first_msg):
        try:
            msg = json.dumps({"client_id": self.config['gapi']['client_id']})
        except KeyError:
            msg = json.dumps({})
        await self.handle.send(msg)


class UserSocket(MuteMeetSocket):
    async def runtime(self, first_msg):
        user, purpose, uuid = User.register(self, first_msg)
        try:
            await user.notify_controllers()
            async for message in self.handle:
                data = json.loads(message)
                logout = data.get("logout")
                action = data.get("action")
                if logout:
                    break
                if action:
                    uuid, device = action.get('uuid'), action.get('device')
                    await user.mute(uuid, device)
        finally:
            await user.unregister(self.handle)
