from pyrebase.pyrebase import Stream

from lib import firebaseData as firebase
from lib.model.User import User
from lib.network.UserNetwork import UserNetwork
from lib.utility.ObserverClasses import Observable


class Staff(User, Observable):

    def __init__(self, uid: str = None, name: str = None, mail: str = None,
                 phone: str = None, CF: str = None, birth_date: str = None, role: str = None):
        super().__init__(uid, phone, mail, role)
        self.__name = name
        self.__CF = CF
        self.__birth_date = birth_date
        self.__stream: Stream | None = None

    def open_stream(self):
        self._uid = firebase.currentUserId()
        self.__stream = UserNetwork.stream_by_id(self._uid, self.__stream_handler)

    def close_stream(self):
        self.__stream.close()

    # Usato per aggiungere i dati di un utente
    def __add_data(self, data: any):
        print(f"{data}")
        if data is not None:
            self._uid = data['uid']
            self.__name = data['name']
            self._mail = data['mail']
            self._phone = data['phone']
            self.__CF = data['CF']
            self.__birth_date = data['birth_date']
            self._role = data['role']

    # Usato per modificare i dati di un utente
    def __edit_data(self, key: str, data: any):
        match key:
            case 'uid':
                self._uid = data
            case 'name':
                self.__name = data
            case 'mail':
                self._mail = data
            case 'phone':
                self._phone = data
            case 'birth_date':
                self.__birth_date = data
            case 'CF':
                self.__CF = data

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
                case "put":  # Funzione di aggiunta dati
                    data['uid'] = firebase.currentUserId()
                    self.__add_data(data)
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
        UserNetwork.checkLogin(currentEmail, password)

    # Modifica i dati degli utenti nel database
    @staticmethod
    def setUserData(form_data: dict[str, any], newPassword, uid):
        UserNetwork.update(form_data, newPassword, uid)

    # Ritorna i dati dell'utente
    def get(self):
        return self

    # Crea il profilo di un nuovo utente
    @staticmethod
    def add_profile(email: str, password: str):
        UserNetwork.create_profile(email, password)

    # Salva un nuovo utente nel database
    @staticmethod
    def add_data(form_data: dict[str, any], user):
        UserNetwork.create_data(form_data, user)

    def get_dict(self):
        return dict(
            uid=self._uid,
            name=self.__name,
            mail=self._mail,
            CF=self.__CF,
            birth_date=self.__birth_date,
            role=self._role,
            phone=self._phone
        )

    # Elimina un utente dal database
    @staticmethod
    def delete(self, email: str):
        try:
            UserNetwork.delete_by_email(email)
            self.__remove_data()
        except Exception as e:
            print(e)
