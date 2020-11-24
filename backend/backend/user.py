import logging

from google.oauth2 import id_token
from google.auth.transport import requests

logger = logging.getLogger(__name__)


class User:
    IN_MEMORY = dict()

    def __str__(self):
        return f"{self.name} ({self.email})"

    def __init__(self, user_id, *args, **kwargs):
        self.controllers = dict()
        self.extensions = dict()
        self.user_id = user_id
        self.name = "Basic User"
        self.email = ""

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


class GoogleUser(User):
    client_id = None
    authorized_ids = ''

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(user_id, *args, **kwargs)
        self.name = kwargs['gapi']["name"]
        self.email = kwargs['gapi']['email']

    @classmethod
    def authenticate(cls, _data):
        token = _data.get("token")
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), cls.client_id)
            user_id = idinfo['sub']
        except ValueError:
            # invalid Token
            return None

        if user_id not in filter(None, cls.authorized_ids.split(',')):
            return None

        return cls.get(user_id, gapi=idinfo)
