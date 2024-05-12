from __future__ import annotations
import firebase_admin
from firebase_admin import auth as admin_auth
import pyrebase
from pyrebase import initialize_app

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


class Firebase(metaclass=Singleton):
    auth: Auth
    database: pyrebase.pyrebase.Database

    @classmethod
    def initialize_app(cls):
        # Inizializzo Firebase
        firebase: pyrebase.pyrebase.Firebase = initialize_app(firebaseConfig)

        # Inizializzo FirebaseAdmin
        credentials = firebase_admin.credentials.Certificate('lib/firebaseKey.json')
        firebase_admin.initialize_app(credentials, {
            'database_url': firebaseConfig.get('databaseURL')})

        # Inizializzo le componenti Auth e Database
        cls.auth = Auth(firebase.api_key, firebase.requests, firebase.credentials)
        cls.database = firebase.database()
