from lib.firebaseData import firebase
from lib.network.HTTPErrorHelper import HTTPErrorHelper
from lib.utility.UtilityClasses import PhoneFormatter


class AuthenticationNetwork:

    # Esegue il login
    @staticmethod
    def login(form_data: dict[str, any]):
        print("Inizio Login")
        return HTTPErrorHelper.differentiate(
            lambda: firebase.auth().sign_in_with_email_and_password(form_data['email'], form_data['password']))

    # Registra un nuovo account
    @staticmethod
    def register(form_data: dict[str, any]):
        return HTTPErrorHelper.differentiate(
            lambda: firebase.auth().create_user_with_email_and_password(form_data["email"], form_data["password"]))

    # Crea il record nel db per il nuovo account
    @staticmethod
    def createDbData(form_data: dict[str, any]):
        data = {
            "company": form_data["nome azienda"],
            "IVA": form_data["partita iva"],
            'mail': form_data["email"],
            "delivery": form_data["indirizzo di recapito"],
            "phone": PhoneFormatter.format(form_data["telefono"]),
            "role": "customer"
        }
        HTTPErrorHelper.differentiate(
            lambda: firebase.database().child('users').child(form_data['uid']).set(data))

