#!/usr/bin/env python3

import asyncio
import configparser
import json
import logging
import websockets

from backend.user import User, GoogleUser
from backend.state import State

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
        elif msg['type'] in ["controller"]:
            socket = ControllerSocket(websocket, path)
        elif msg['type'] in ["extension", ""]:
            socket = ExtensionSocket(websocket, path)
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


class ExtensionSocket(MuteMeetSocket):
    @property
    def klass(self):
        return User

    async def runtime(self, first_msg):
        user = self.klass.authenticate(first_msg)
        if not user:
            return

        state = State.register(self, user, first_msg)
        if not state:
            return

        try:
            await state.notify_controllers()
            async for message in self.handle:
                data = json.loads(message)
                logout = data.get("logout")
                action = data.get("action")
                if logout:
                    break
                if action:
                    uuid, device = action.get('uuid'), action.get('device')
                    await state.mute(uuid, device)
        finally:
            await state.unregister(self.handle)


class ControllerSocket(ExtensionSocket):
    @property
    def klass(self):
        try:
            GoogleUser.client_id = self.config['gapi']['client_id']
            GoogleUser.authorized_ids = self.config['gapi']['authorized_ids']
            return GoogleUser
        except ValueError:
            return super().klass
