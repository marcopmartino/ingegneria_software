from lib.firebaseData import Firebase
from lib.utility.HTTPErrorHelper import HTTPErrorHelper
from lib.repository.UsersRepository import UsersRepository
from lib.utility.UtilityClasses import PhoneFormatter


class AccessController:
    def __init__(self):
        super().__init__()
        self.__users_repository: UsersRepository = UsersRepository()

    # Esegue il login
    def login(self, form_data: dict[str, any]):
        print("Inizio Login")
        self.__users_repository.authenticate_user(form_data['email'], form_data['password'])
        print("Fine Login")

    # Registra un nuovo account
    def register(self, form_data: dict[str, any]):
        print("Inizio Registrazione")
        self.__users_repository.create_customer(form_data)
        print("Fine Registrazione")
