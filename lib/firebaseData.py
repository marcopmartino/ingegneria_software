# Firebase Config data
from typing import Any

import pyrebase

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

currentUser: Any


# noinspection PyPep8Naming
def currentUserId():
    return currentUser["localId"]


def init():
    global currentUser
    currentUser = None
