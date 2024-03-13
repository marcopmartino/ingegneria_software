from lib.firebaseData import firebase
from lib import firebaseData as firebaseConfig
from lib.network.HTTPErrorHelper import HTTPErrorHelper


class AccessController:
    def __init__(self):
        super().__init__()
        self.auth = firebase.auth()
        self.database = firebase.database()

    # Esegue il login
    def login(self, form_data: dict[str, any]):
        print("Inizio Login")
        firebaseConfig.currentUser = HTTPErrorHelper.handle_request(
            lambda: self.auth.sign_in_with_email_and_password(form_data['email'], form_data['password']))
        print("Fine Login")

    # Registra un nuovo account
    def register(self, form_data: dict[str, any]):
        firebaseConfig.currentUser = HTTPErrorHelper.handle_request(
            lambda: self.auth.create_user_with_email_and_password(form_data["email"], form_data["password"]))
        uid = firebaseConfig.currentUser['localId']
        data = {
            "company": form_data["nome azienda"],
            "IVA": form_data["partita iva"],
            "delivery": form_data["indirizzo di recapito"],
            "phone": form_data["telefono"],
            "role": "user"
        }
        self.database.child('users').child(uid).set(data)

    # Ottiene il tipo di utente che sta effettuando l'accesso
    def getUserRole(self):
        data = HTTPErrorHelper.handle_request(
            lambda: self.database.child('users').child(firebaseConfig.currentUser['localId'])).get().val()
        return data['role']
