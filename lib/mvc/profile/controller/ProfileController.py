from firebase_admin import auth

from lib.firebaseData import firebase
from lib import firebaseData as firebaseConfig
from lib.network.HTTPErrorHelper import HTTPErrorHelper


class ProfileController:
    def __init__(self):
        super().__init__()
        self.auth = firebase.auth()
        self.database = firebase.database()

    # Prende i dati dal database
    def getData(self, user_id):
        print("Inizio ottenimento dati")
        return HTTPErrorHelper.differentiate(
             lambda: self.database.child('users').child(user_id)).get().val()

    # Salva i dati degli operai/manager nel database
    def setWorkerData(self, form_data: dict[str, any], newPassword, uid):
        print("Inizio invio dati")
        HTTPErrorHelper.differentiate(
            lambda: self.database.child('worker').child(uid).update(form_data))

        if newPassword is not None:
            HTTPErrorHelper.differentiate(
                lambda: auth.update_user(uid, password=newPassword))

    # Salva i dati degli utenti nel database
    def setUserData(self, form_data: dict[str, any], newPassword, uid):
        print(newPassword)
        print("Inizio invio dati")
        HTTPErrorHelper.differentiate(
            lambda: self.database.child('users').child(uid).update(form_data))

        if newPassword is not None:
            HTTPErrorHelper.differentiate(
                lambda: auth.update_user(uid, password=newPassword))

    # Controllare che le credenziali siano corrette
    def checkLogin(self, currentEmail, password):
        HTTPErrorHelper.differentiate(
            lambda: self.auth.sign_in_with_email_and_password(currentEmail, password))
