from lib.firebaseData import Firebase
from lib.model.Customer import Customer
from lib.model.Employee import Employee
from lib.model.User import User
from lib.repository.UsersRepository import UsersRepository
from lib.utility.ObserverClasses import Observer


class ProfileController:
    def __init__(self):
        super().__init__()

        # Respository
        self.__users_repository = UsersRepository()

        # Model
        self.__user: Customer | Employee | None = None

    # Inizializza il controller
    def initialize_user(self):
        self.__user = self.__users_repository.get_user_by_id(Firebase.auth.currentUserId())

    # Imposta un osservatore sui dati di un utente
    def observe_user(self, callback: callable) -> Observer:
        return self.__user.observe(callback)

    # Imposta un osservatore sulla repository
    def observe_users_repository(self, callback: callable) -> Observer:
        return self.__users_repository.observe(callback)

    # Imposta un osservatore sui dati di un utente
    def detach_users_repositor_observer(self, observer: Observer):
        return self.__users_repository.detach(observer)

    # Restituisce l'utente
    def get_user(self) -> Customer | Employee | None:
        return self.__user

    # Restituisce l'id dell'utente
    def get_user_id(self) -> str:
        return self.__user.get_uid()

    # Aggiorna l'utente
    def update_user(self, form_data: dict[str, any]):
        self.__users_repository.reauthenticate_current_user(form_data.pop("password"))
        self.__users_repository.update_user_by_id(self.__user.get_uid(), form_data)

    # Elimina l'utente
    def delete_user(self):
        self.__users_repository.delete_user_by_id(self.__user.get_uid())

    # Autentica nuovamente l'utente corrente
    def reauthenticate_current_user(self, password: str):
        return self.__users_repository.reauthenticate_current_user(password)
