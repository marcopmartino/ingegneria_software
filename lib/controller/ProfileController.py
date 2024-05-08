from lib.model.AuthenticatedCustomer import AuthenticatedCustomer
from lib.model.AuthenticatedStaff import AuthenticatedStaff
from lib.utility.AuthenticationClass import Authentication
from lib.utility.Singleton import AuthenticationSingleton


class ProfileController(Authentication, metaclass=AuthenticationSingleton):
    def __init__(self):
        super().__init__()
        self._user_data = None

    def register(self, form_data: dict[str, any]):
        auth_data = self._authentication_network.register(form_data)
        form_data['uid'] = auth_data['localId']
        self._authentication_network.createDbData(form_data)
        self._user_data = AuthenticatedCustomer(form_data['uid'], form_data['nome azienda'],
                                                form_data['telefono'], form_data['email'],
                                                form_data['indirizzo di recapito'], form_data['IVA'],
                                                form_data['role'])

    def login(self, form_data: dict[str, any]):
        auth_data = self._authentication_network.login(form_data)
        storage_data = self._user_network.get_by_id(auth_data['localId'])
        if storage_data['role'] == 'customer':
            self._user_data = AuthenticatedCustomer(auth_data['localId'], storage_data['company'],
                                                    storage_data['phone'], storage_data['mail'],
                                                    storage_data['delivery'], storage_data['IVA'],
                                                    storage_data['role'])
        else:
            self._user_data = AuthenticatedStaff(auth_data['localId'], storage_data['name'],
                                                 storage_data['mail'], storage_data['phone'],
                                                 storage_data['CF'], storage_data['birth_date'],
                                                 storage_data['role'])
            print(":)")
        print(f"Dati utente: {self._user_data.get_dict()}")

    # Apre uno stream sul profilo
    def open_stream(self):
        self._user_data.open_stream()

    # Imposta un osservatore sui dati di un profilo
    def set_observer(self, callback: callable):
        self._user_data.observe(callback)

    # Controlla che le credenziali inserite in fase di modifica dei dati siano corrette
    def check_login(self, currentEmail, password):
        self._user_data.checkLogin(currentEmail, password)

    # Imposta i nuovi dati per un cliente
    def set_user_data(self, data, newPassword, uid):
        self._user_data.set_user_data(data, newPassword, uid)

    # Crea un nuovo profilo per un operaio
    def staff_add_profile(self, email, password):
        self._user_data.add_profile(email, password)

    # Aggiunge i dati di nuovo operaio nel database
    def staff_add_data_newprofile(self, data, user):
        self._user_data.add_data(data, user)

    def get_user_data(self):
        return self._user_data.get_dict() if self._user_data is not None else None

    def get_role(self):
        return self._user_data.get_role() if self._user_data is not None else None

    def get_uid(self):
        return self._user_data.get_uid() if self._user_data is not None else None
