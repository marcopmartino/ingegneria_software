from pyrebase.pyrebase import Stream

from lib.firebaseData import firebase
from lib.mvc.profile.model.User import User
from lib.network.UserNetwork import UserNetwork
from lib.utility.ObserverClasses import Observable
from lib.utility.Singleton import ObservableSingleton


class Staff(User, Observable, metaclass=ObservableSingleton):

    def __init__(self, name: str = None, mail: str = None,
                 phone: str = None, CF: str = None, birth_date: str = None, role: str = None):
        super().__init__(phone, mail, role)
        self.name = name
        self.CF = CF
        self.birth_date = birth_date
        self.stream: Stream | None = None

    def open_stream(self):
        self.uid = firebase.currentUserId()
        self.stream = UserNetwork.stream_by_id(self.uid, self.__stream_handler)

    def close_stream(self):
        self.stream.close()

    # Usato per aggiungere i dati di un utente
    def __add_data(self, data: any):
        print(f"{data}")
        if data is not None:
            self.name = data['name']
            self.mail = data['mail']
            self.phone = data['phone']
            self.CF = data['CF']
            self.birth_date = data['birth_date']
            self.role = data['role']

    # Usato per modificare i dati di un utente
    def __edit_data(self, key: str, data: any):
        match key:
            case 'name':
                self.name = data
            case 'mail':
                self.mail = data
            case 'phone':
                self.phone = data
            case 'birth_date':
                self.birthDate = data
            case 'CF':
                self.CF = data

    # Usato per rimuovere i dati di un utente (in caso di eliminazione)
    def __remove_data(self):
        self.delete(self, self.email)
        self.name = None
        self.phone = None
        self.uid = None
        self.phone = None
        self.email = None
        self.birth_date = None
        self.CF = None

    # Stream handler che aggiorna automaticamente i dati dell'utente
    def __stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        data = message['data']
        if data is not None:
            match message['event']:
                case "put":  # Funzione di aggiunta dati
                    data['mail'] = firebase.currentUser['mail']
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
        self.notify(self.to_dict())

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

    def to_dict(self):
        return vars(self)

    # Elimina un utente dal database
    @staticmethod
    def delete(self, email: str):
        try:
            UserNetwork.delete_by_email(email)
            self.__remove_data()
        except Exception as e:
            print(e)


