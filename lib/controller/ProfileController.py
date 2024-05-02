from lib.model.Customer import Customer
from lib.model.Staff import Staff


class ProfileController:
    def __init__(self):
        super().__init__()
        self.__customer_model: Customer | None = None
        self.__staff_model: Staff | None = None

    # Apre uno stream sul profilo di un cliente
    def open_customer_stream(self):
        self.__customer_model = Customer()
        self.__customer_model.open_stream()

    # Apre uno stream sul profilo di un membro dello staff
    def open_staff_stream(self):
        self.__staff_model = Staff()
        self.__staff_model.open_stream()

    # Imposta un osservatore sui dati di un cliente
    def set_customer_observer(self, callback: callable):
        self.__customer_model.observe(callback)

    # Imposta un osservatore sui dati di un membro dello staff
    def set_staff_observer(self, callback: callable):
        self.__staff_model.observe(callback)

    # Restituisce il model di un cliente
    def get_customer_model(self):
        return self.__customer_model.get()

    # Restituisce il model di un membro dello staff
    def get_staff_model(self):
        return self.__staff_model.get_dict()

    # Controlla che le credenziali inserite in fase di modifica dei dati siano corrette per un cliente
    def customer_checkLogin(self, currentEmail, password):
        self.__customer_model.checkLogin(currentEmail, password)

    # Controlla che le credenziali inserite in fase di modifica dei dati siano corrette per membro dello staff
    def staff_checkLogin(self, currentEmail, password):
        self.__staff_model.checkLogin(currentEmail, password)

    # Imposta i nuovi dati per un cliente
    def customer_setUserData(self, data, newPassword, uid):
        self.__customer_model.setUserData(data, newPassword, uid)

    # Imposta i nuovi dati per un membro dello staff
    def staff_setUserData(self, data, newPassword, uid):
        self.__staff_model.setUserData(data, newPassword, uid)

    # Crea un nuovo profilo per un operaio
    def staff_add_profile(self, email, password):
        self.__staff_model.add_profile(email, password)

    # Aggiunge i dati di nuovo operaio nel database
    def staff_add_data_newprofile(self, data, user):
        self.__staff_model.add_data(data, user)
