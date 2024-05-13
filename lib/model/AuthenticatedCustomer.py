from pyrebase.pyrebase import Stream

from lib.model.Customer import Customer
from lib.network.UserNetwork import UserNetwork
from lib.utility.ObserverClasses import Observable
from lib.utility.Singleton import ObservableSingleton


class AuthenticatedCustomer(Customer, Observable):
    def __init__(self, uid: str = None, company: str = None, phone: str = None, mail: str = None,
                 delivery: str = None, IVA: str = None, role: str = None):
        super().__init__(uid, company, phone, mail, delivery, IVA, role)
        self.__stream: Stream | None = None

    def open_stream(self):
        self.__stream = UserNetwork().stream_by_id(self._uid, self.__stream_handler)

    '''def set_data(self, uid: str = None, company: str = None, phone: str = None, mail: str = None,
                 delivery: str = None, IVA: str = None, role: str = None):
        self.__init__(uid, company, phone, mail, delivery, IVA, role)'''

    def close_stream(self):
        self.__stream.close()

    # Usato per modificare i dati di un utente
    def __edit_data(self, key: str, data: any):
        match key:
            case 'uid':
                self._uid = data
            case 'company':
                self._company = data
            case 'mail':
                self._mail = data
            case 'phone':
                self._phone = data
            case 'deliveryAddress':
                self._delivery = data
            case 'IVA':
                self._IVA = data

        # Usato per rimuovere i dati di un utente (in caso di eliminazione)

    # Usato eliminare il profilo dell'utente
    def __remove_data(self):
        self.delete(self, self._mail)
        self._company = None
        self._phone = None
        self._mail = None
        self._delivery = None
        self._IVA = None

    # Stream handler che aggiorna automaticamente i dati dell'utente
    def __stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        data = message['data']
        if data is not None:
            match message['event']:
                case "put":  # Funzione di aggiunta dati
                    pass
                case "patch":  # Funzione di modifica dei dati
                    for key, value in data.items():
                        self.__edit_data(key, value)
                case "cancel":
                    pass
        else:
            # Elimino il profilo
            self.__remove_data()
        # Notifico gli osservatori cosi che possano aggiornarsi
        self.notify(message["data"])

    # Ritorna i dati dell'utente
    def get(self):
        return self

    @staticmethod
    def checkLogin(currentEmail, password):
        UserNetwork().checkLogin(currentEmail, password)

    # Modifica i dati degli utenti nel database
    @staticmethod
    def set_user_data(form_data: dict[str, any], newPassword, uid):
        UserNetwork().update(form_data, newPassword, uid)

    def to_dict(self):
        return vars(self)

    # Elimina un utente dal database
    @staticmethod
    def delete(self, email: str):
        try:
            UserNetwork().delete_by_email(email)
        except Exception as e:
            print(e)
