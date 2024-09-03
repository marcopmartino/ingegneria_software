from __future__ import annotations

import json
import threading

import firebase_admin
import pyrebase
from firebase_admin import auth as admin_auth
from pyrebase import initialize_app
from pyrebase.pyrebase import ClosableSSEClient
from requests import ConnectionError

from lib.utility.ResourceManager import ResourceManager
from lib.utility.Singleton import Singleton

# Firebase Config data
firebaseConfig = {
    'apiKey': "AIzaSyA5N-gyqRJ3vnMOg_3AEqElp2Kcp3AM2Tg",
    'authDomain': "provapython-3172a.firebaseapp.com",
    'databaseURL': "https://provapython-3172a-default-rtdb.europe-west1.firebasedatabase.app/",
    'projectId': "provapython-3172a",
    'storageBucket': "provapython-3172a.appspot.com",
    'messagingSenderId': "753165877140",
    'appId': "1:753165877140:web:48fc2fa7ca1c34b4489981"
}


class Stream(pyrebase.pyrebase.Stream):
    def __init__(self, url, stream_handler, on_connection_lost, build_headers, stream_id, is_async):
        super().__init__(url, stream_handler, build_headers, stream_id, is_async)

        self.on_connection_lost: callable = on_connection_lost

    def start(self):
        self.thread = threading.Thread(target=self.start_stream)
        self.thread.start()
        return self

    def start_stream(self):
        try:
            self.sse = ClosableSSEClient(self.url, session=self.make_session(), build_headers=self.build_headers)
            for msg in self.sse:
                if msg:
                    msg_data = json.loads(msg.data)
                    msg_data["event"] = msg.event
                    if self.stream_id:
                        msg_data["stream_id"] = self.stream_id
                    self.stream_handler(msg_data)
        except ConnectionError:
            self.on_connection_lost()


# noinspection PyPep8Naming
class Auth(pyrebase.pyrebase.Auth):

    def __init__(self, api_key, requests, credentials):
        super().__init__(api_key, requests, credentials)
        self.current_user = dict()  # Sovrascrive None con un dizionario vuoto

    def currentUserRole(self) -> str:
        return self.current_user.get("role", "unauthenticated")

    def currentUserId(self) -> str:
        return self.current_user.get("localId")

    def currentUserEmail(self) -> str:
        return self.current_user.get("email")

    def create_user_with_email_and_password(self, email: str, password: str, sign_in: bool = True) -> str:
        if sign_in:
            self.sign_out()
            self.current_user = super().create_user_with_email_and_password(email, password)
            return self.currentUserId()
        else:
            return admin_auth.create_user(email=email, password=password).uid

    def setCurrentUserRole(self, role: str):
        self.current_user["role"] = role

    @staticmethod
    def updateUserPasswordById(uid: str, new_password: str):
        admin_auth.update_user(uid, password=new_password)

    @staticmethod
    def deleteUserById(uid: str):
        admin_auth.delete_user(uid)

    def sign_out(self) -> None:
        self.current_user = dict()


class Database(pyrebase.pyrebase.Database):

    def __init__(self, credentials, api_key, database_url, requests):
        super().__init__(credentials, api_key, database_url, requests)

        self.on_collection_lost: callable = None

    def stream(self, stream_handler, token=None, stream_id=None, is_async=True):
        request_ref = self.build_request_url(token)
        return Stream(request_ref, stream_handler, self.on_collection_lost, self.build_headers, stream_id, is_async)

    def register_connection_lost_callback(self, callback: callable):
        self.on_collection_lost = callback


class Firebase(metaclass=Singleton):

    # Classi Auth e Database
    auth: Auth
    database: Database

    @classmethod
    def initialize_app(cls):
        # Inizializzo Pyrebase
        firebase: pyrebase.pyrebase.Firebase = initialize_app(firebaseConfig)

        # Inizializzo FirebaseAdmin
        credentials = firebase_admin.credentials.Certificate(ResourceManager.file_path('lib/firebaseKey.json'))
        firebase_admin.initialize_app(credentials, {
            'database_url': firebaseConfig.get('databaseURL')})

        # Inizializzo le componenti Auth e Database
        cls.auth = Auth(firebase.api_key, firebase.requests, firebase.credentials)
        cls.database = Database(firebase.credentials, firebase.api_key, firebase.database_url, firebase.requests)

    @classmethod
    def register_connection_lost_callback(cls, callback: callable):
        if cls.database is not None:
            cls.database.register_connection_lost_callback(callback)
