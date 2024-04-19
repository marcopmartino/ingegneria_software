from pyrebase.pyrebase import Stream

from lib.model.Staff import Staff
from lib.network.UserNetwork import UserNetwork
from lib.utility.ObserverClasses import Observable
from lib.utility.Singleton import ObservableSingleton
from lib import firebaseData as firebase


class StaffDataManager(Observable, metaclass=ObservableSingleton):

    def __init__(self):
        super().__init__()
        self.__staff_data = Staff()
        self.stream: Stream | None = None

    def open_stream(self):
        self.stream = UserNetwork.stream_by_id(firebase.currentUserId(), self.__stream_handler)

    def close_stream(self):
        self.stream.close()

    # Usato per aggiungere i dati di un utente
    def __add_data(self, data: any):
        print(f"{data}")
        if data is not None:
            self.__staff_data = Staff(data['uid'], data['name'], data['email'],
                                      data['phone'], data['CF'], data['birth_date'], data['role'])

    # Usato per modificare i dati di un utente
    def __edit_data(self, key: str, data: any):
        match key:
            case 'name':
                self.__staff_data.companyName = data
            case 'mail':
                self.__staff_data.email = data
            case 'phone':
                self.__staff_data.phone = data
            case 'birth_date':
                self.__staff_data.birthDate = data
            case 'CF':
                self.__staff_data.CF = data

    # Usato per rimuovere i dati di un utente (in caso di eliminazione)
    def __remove_data(self):
        self.delete(self.__staff_data.email)
        self.__staff_data = None

    # Stream handler che aggiorna automaticamente i dati dell'utente
    def __stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        data = message['data']
        if data is not None:
            match message['event']:
                case "put":  # Funzione di aggiunta dati
                    data['email'] = firebase.currentUser['email']
                    data['uid'] = firebase.currentUserId()
                    self.__add_data(data)
                case "patch":  # Funzione di modifica dei dati
                    for key, value in data.items():
                        print(key)
                        self.__edit_data(key, value)
                case "cancel":
                    pass
        else:
            # Elimino il profilo
            if len(data) == 1:
                self.__remove_data()

        # Notifico gli osservatori cosi che possano aggiornarsi
        message['notifier'] = StaffDataManager
        self.notify(self.__staff_data)

    @staticmethod
    def checkLogin(currentEmail, password):
        UserNetwork.checkLogin(currentEmail, password)

    # Modifica i dati degli utenti nel database
    @staticmethod
    def setUserData(form_data: dict[str, any], newPassword, uid):
        UserNetwork.update(form_data, newPassword, uid)

    # Ritorna i dati dell'utente
    def get(self) -> Staff:
        return self.__staff_data

    # Crea il profilo di un nuovo utente
    @staticmethod
    def add_profile(email: str, password: str):
        UserNetwork.create_profile(email, password)

    # Salva un nuovo utente nel database
    @staticmethod
    def add_data(form_data: dict[str, any], user):
        UserNetwork.create_data(form_data, user)

    # Elimina un utente dal database
    @staticmethod
    def delete(email: str):
        UserNetwork.delete_by_email(email)
