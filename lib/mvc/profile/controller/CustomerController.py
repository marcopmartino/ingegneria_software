from typing import Any

from firebase_admin import auth

from lib.firebaseData import firebase
from lib import firebaseData as firebaseConfig
from lib.mvc.profile.model.CustomerDataManager import CustomerDataManager
from lib.network.HTTPErrorHelper import HTTPErrorHelper


class CustomerController:
    def __init__(self):
        super().__init__()
        self.customer_data = CustomerDataManager()

        self.auth = firebase.auth()
        self.database = firebase.database()

    # Crea uno stream sul database per osservare eventuali cambiamenti
    def getProfileStream(self, stream_handler):
        print("Inizio ottenimento dati")
        uid = firebaseConfig.currentUser['localId']
        return HTTPErrorHelper.differentiate(
            lambda: self.database.child('users').child(uid).stream(stream_handler, stream_id="profile_data"))

    # Prende i propri data dal database
    def getData(self):
        print("Inizio ottenimento dati")
        uid = firebaseConfig.currentUser['localId']
        return HTTPErrorHelper.differentiate(
             lambda: self.database.child('users').child(uid)).get().val()

    # Crea un profilo utente per il worker
    def registerWorker(self, email: str, password: str):
        return HTTPErrorHelper.differentiate(
            lambda: self.auth.create_user_with_email_and_password(email, password))

    # Modifica i dati degli operai/manager nel database
    def createUserData(self, form_data: dict[str, any], user: Any):
        print("Inizio invio dati")
        HTTPErrorHelper.differentiate(
            lambda: self.database.child('users').child(user['localId']).set(form_data))

    # Modifica i dati degli utenti nel database
    def setUserData(self, form_data: dict[str, any], newPassword, uid):
        print(newPassword)
        print("Inizio invio dati")
        HTTPErrorHelper.differentiate(
            lambda: self.database.child('users').child(uid).update(form_data))

        if newPassword is not None:
            HTTPErrorHelper.differentiate(
                lambda: auth.update_user(uid, password=newPassword))

    # Controlla che le credenziali siano corrette
    def checkLogin(self, currentEmail, password):
        HTTPErrorHelper.differentiate(
            lambda: self.auth.sign_in_with_email_and_password(currentEmail, password))
