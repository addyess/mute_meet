import asyncio
from collections import namedtuple
import json
import logging
from uuid import uuid4

logger = logging.getLogger(__name__)
Identity = namedtuple('Identity', 'uuid,email')


class State:
    controllers = dict()
    extensions = dict()

    def __str__(self):
        return f"{self.purpose}> {self.user}"

    def __init__(self, user, purpose, uuid):
        self.user = user
        self.purpose = purpose
        self.uuid = uuid

    @classmethod
    def register(cls, socket, user, data):
        """Await user to provide valid google id on new socket."""
        if not user:
            return cls(None, "Cannot Authenticate", None)
        if "type" not in data:
            return cls(None, "Unsupported Connection", None)

        purpose = data["type"]
        email = data.get('user')
        uuid = uuid4()
        if purpose == "extension":
            user.email = email
            cls.extensions[socket.handle] = Identity(uuid, email)
            self = cls(user, purpose, uuid)
        elif purpose == "controller":
            cls.controllers[socket.handle] = Identity(uuid, email)
            self = cls(user, purpose, uuid)
        else:
            return None

        logger.info(f"{self} has arrived @ {self.uuid}")
        return self

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
