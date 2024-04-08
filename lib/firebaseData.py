# Firebase Config data
from typing import Any

import firebase_admin
import pyrebase
from requests import RequestException

from lib.network.HTTPErrorHelper import HTTPErrorHelper

firebaseConfig = {
    'apiKey': "AIzaSyA5N-gyqRJ3vnMOg_3AEqElp2Kcp3AM2Tg",
    'authDomain': "provapython-3172a.firebaseapp.com",
    'databaseURL': "https://provapython-3172a-default-rtdb.europe-west1.firebasedatabase.app/",
    'projectId': "provapython-3172a",
    'storageBucket': "provapython-3172a.appspot.com",
    'messagingSenderId': "753165877140",
    'appId': "1:753165877140:web:48fc2fa7ca1c34b4489981"
}

firebase = pyrebase.initialize_app(firebaseConfig)
cred = firebase_admin.credentials.Certificate('lib/firebaseKey.json')
firebase_users = firebase_admin.initialize_app(cred, {
    'database_url': firebaseConfig.get('databaseURL')})
currentUser: Any = None


# noinspection PyPep8Naming
def currentUserId():
    return currentUser["localId"]


# Ottiene il tipo di utente che sta effettuando l'accesso
# noinspection PyPep8Naming
def getUserRole():
    def no_authenticated_user_handler():
        return "unauthenticated"

    return HTTPErrorHelper.handle(
        lambda: firebase.database().child('users').child(currentUserId()).get().val()['role'],
        {TypeError: no_authenticated_user_handler},
        True
    )


def init():
    global currentUser
    currentUser = None
