from pyrebase.pyrebase import Stream

from lib.model.Staff import Staff
from lib.network.UserNetwork import UserNetwork
from lib.utility.ObserverClasses import Observable
from lib.utility.Singleton import ObservableSingleton


class AuthenticatedStaff(Staff, Observable):
    def __init__(self, uid: str = None, name: str = None, mail: str = None,
                 phone: str = None, CF: str = None, birth_date: str = None, role: str = None):
        super().__init__(uid, name, mail, phone, CF, birth_date, role)
        self.__stream: Stream | None = None

    # Usato per aprire lo stream
    def open_stream(self):
        self.__stream = UserNetwork().stream_by_id(self._uid, self.__stream_handler)

    '''def set_data(self, uid: str = None, name: str = None, mail: str = None,
                 phone: str = None, CF: str = None, birth_date: str = None, role: str = None):
        self.__init__(uid, name, mail, phone, CF, birth_date, role)'''

    # Usato per chiudere lo stream
    def close_stream(self):
        self.__stream.close()

    # Usato per modificare i dati di un utente
    def __edit_data(self, key: str, data: any):
        match key:
            case 'uid':
                self._uid = data
            case 'name':
                self._name = data
            case 'mail':
                self._mail = data
            case 'phone':
                self._phone = data
            case 'birth_date':
                self._birth_date = data
            case 'CF':
                self._CF = data

    # Usato per rimuovere i dati di un utente (in caso di eliminazione)
    def __remove_data(self):
        self.delete(self, self._mail)
        self.__name = None
        self._phone = None
        self._email = None
        self.__birth_date = None
        self.__CF = None
        self._role = None

    # Stream handler che aggiorna automaticamente i dati dell'utente
    def __stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        data = message['data']
        if data is not None:
            match message['event']:
                case "put":
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

    @staticmethod
    def checkLogin(currentEmail, password):
        UserNetwork().checkLogin(currentEmail, password)

    # Modifica i dati degli utenti nel database
    @staticmethod
    def set_user_data(form_data: dict[str, any], newPassword, uid):
        UserNetwork().update(form_data, newPassword, uid)

    # Ritorna i dati dell'utente
    def get(self):
        return self

    # Crea il profilo di un nuovo utente
    @staticmethod
    def add_profile(email: str, password: str):
        UserNetwork().create_profile(email, password)

    # Salva un nuovo utente nel database
    @staticmethod
    def add_data(form_data: dict[str, any], user):
        UserNetwork().create_data(form_data, user)

    def get_dict(self):
        return dict(
            uid=self._uid,
            name=self._name,
            mail=self._mail,
            CF=self._CF,
            birth_date=self._birth_date,
            role=self._role,
            phone=self._phone
        )

    # Elimina un utente dal database
    @staticmethod
    def delete(self, email: str):
        try:
            UserNetwork().delete_by_email(email)
            self.__remove_data()
        except Exception as e:
            print(e)
