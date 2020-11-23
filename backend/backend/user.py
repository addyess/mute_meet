import asyncio
from collections import namedtuple
import json
import logging
from uuid import uuid4

logger = logging.getLogger(__name__)
Identity = namedtuple('Identity', 'uuid,email')


class User:
    IN_MEMORY = dict()

    def __str__(self):
        return "Basic User"

    def __init__(self, user_id, *args, **kwargs):
        self.controllers = dict()
        self.extensions = dict()
        self.user_id = user_id

    @classmethod
    def authenticate(cls, _data):
        return cls.get(1)

    @classmethod
    def get(cls, user_id, *args, **kwargs):
        user = User.IN_MEMORY.get(user_id)
        if not user:
            user = cls(user_id, *args, **kwargs)
            User.IN_MEMORY[user_id] = user
        return user

    @classmethod
    def register(cls, socket, data):
        """Await user to provide valid google id on new socket."""
        user = cls.authenticate(data)

        if user and "type" in data:
            purpose = data["type"]
            email = data.get('user')
            uuid = uuid4()
            logger.info(f"{user} has arrived w/{purpose} @ {uuid}")
            if purpose == "extension":
                user.extensions[socket.handle] = Identity(uuid, email)
                return user, purpose, uuid
            elif purpose == "controller":
                user.controllers[socket.handle] = Identity(uuid, email)
                return user, purpose, uuid

    def extension_state(self):
        return json.dumps(
            {
                "meet-sessions": [
                    {"id": ws.email or ext_id, "uuid": str(ws.uuid)}
                    for ext_id, (_, ws) in enumerate(self.extensions.items())
                ]
            }
        )

    async def notify_controllers(self):
        logger.info(f"{self} needs controllers notified")
        msg = self.extension_state()
        if self.controllers:
            await asyncio.wait([ws.send(msg) for ws in self.controllers.keys()])

    async def unregister(self, websocket):
        purpose, ws = "extension", self.extensions.pop(websocket, None)
        if not ws:
            purpose, ws = "controller", self.controllers.pop(websocket, None)
        logger.info(f"{self} has left w/{purpose} @ {ws.uuid}")
        await self.notify_controllers()

    async def mute(self, uuid, device_id):
        """Controller says to mute a specific extensions"""
        websockets = [
            ws
            for ws, data in self.extensions.items()
            if str(data.uuid) == uuid
        ]
        if websockets:
            logger.info(f"Toggle {device_id} @ {uuid}")
            msg = json.dumps({"toggle": device_id})
            await asyncio.wait([ws.send(msg) for ws in websockets])
