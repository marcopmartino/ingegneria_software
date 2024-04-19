from firebase_admin import auth

from lib.firebaseData import firebase
from lib.model.WorkerList import WorkerList
from lib.network.HTTPErrorHelper import HTTPErrorHelper


class WorkerListController:
    def __init__(self):
        super().__init__()
        self.worker_list = WorkerList()
        self.auth = firebase.auth()
        self.database = firebase.database()

    # Crea uno stream sul database per osservare eventuali cambiamenti
    def getWorkerListStream(self, stream_handler):
        print("Inizio ottenimento dati")
        return HTTPErrorHelper.differentiate(
            lambda: self.database.child('users').stream(stream_handler, stream_id="worker_list"))

    # Prende la lista degli operai dal database
    def getWorkerList(self):
        print("Inizio ottenimento dati")
        return HTTPErrorHelper.differentiate(
            lambda: self.database.child('users').get_price_catalog().val())

    # Prende i dati relativi a un singolo operaio
    def getWorkerData(self, uid: str):
        print("Inizio ottenimento dati")
        return HTTPErrorHelper.differentiate(
            lambda: self.database.child('users').child(uid).get_price_catalog().val())

    # Salva i dati degli operai/manager nel database
    def setWorkerData(self, form_data: dict[str, any], newPassword, uid):
        print("Inizio invio dati")
        HTTPErrorHelper.differentiate(
            lambda: self.database.child('users').child(uid).update_price_catalog(form_data))

        if newPassword != "":
            HTTPErrorHelper.differentiate(
                lambda: auth.update_user(uid, password=newPassword))

    # Controllare che le credenziali siano corrette
    def checkLogin(self, currentEmail, password):
        HTTPErrorHelper.differentiate(
            lambda: self.auth.sign_in_with_email_and_password(currentEmail, password))

