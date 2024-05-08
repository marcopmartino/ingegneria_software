from lib.firebaseData import Firebase
from lib.utility.HTTPErrorHelper import HTTPErrorHelper
from lib.repository.UsersRepository import UsersRepository
from lib.utility.UtilityClasses import PhoneFormatter


class AccessController:
    def __init__(self):
        super().__init__()
        self.__users_repository: UsersRepository = UsersRepository()
        '''Da spostare in UsersRepository'''
        self.__database = Firebase.database

    # Esegue il login
    # noinspection PyMethodMayBeStatic
    def login(self, form_data: dict[str, any]):
        print("Inizio Login")
        HTTPErrorHelper.differentiate(
            lambda: self.__users_repository.authenticate_user(form_data['email'], form_data['password']))
        print("Fine Login")

    '''Da spostare in UsersRepository'''
    # Registra un nuovo account
    def register(self, form_data: dict[str, any]):
        Firebase.auth.currentUser = HTTPErrorHelper.differentiate(
            lambda: Firebase.auth.create_user_with_email_and_password(form_data["email"], form_data["password"]))
        uid = Firebase.auth.currentUserId()
        data = {
            "company": form_data["nome azienda"],
            "IVA": form_data["partita iva"],
            "mail": form_data["email"],
            "delivery": form_data["indirizzo di recapito"],
            "phone": PhoneFormatter.format(form_data["telefono"]),
            "role": "customer"
        }
        HTTPErrorHelper.differentiate(
            lambda: self.__database.child('users').child(uid).set(data))
