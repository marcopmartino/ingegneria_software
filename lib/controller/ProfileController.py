from lib.firebaseData import Firebase
from lib.model.Customer import Customer
from lib.model.Employee import Employee
from lib.model.Order import OrderState
from lib.repository.OrdersRepository import OrdersRepository
from lib.repository.UsersRepository import UsersRepository
from lib.utility.ObserverClasses import Observer


class ProfileController:
    def __init__(self):
        super().__init__()

        # Repository
        self.__users_repository = UsersRepository()
        self.__orders_repository = OrdersRepository()

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
    def detach_users_repository_observer(self, observer: Observer):
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
        # Elimina tutti gli ordini non consegnati dell'utente (ordini non iniziati)
        for order in self.__orders_repository.get_order_list():
            if order.get_state() != OrderState.DELIVERED:
                self.__orders_repository.delete_order_by_id(order.get_order_serial())

        # Elimina i dati dell'utente
        self.__users_repository.delete_user_by_id(self.__user.get_uid())

    # Autentica nuovamente l'utente corrente
    def reauthenticate_current_user(self, password: str):
        return self.__users_repository.reauthenticate_current_user(password)

    # Determina se l'account può essere eliminato
    def can_delete_user(self):
        # L'account può essere eliminato se nessun ordine dell'utente è in lavorazione o completato
        for order in self.__orders_repository.get_order_list():
            if order.get_state() in (OrderState.PROCESSING, OrderState.COMPLETED):
                return False
        return True
