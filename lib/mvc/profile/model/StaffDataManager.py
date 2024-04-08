from pyrebase.pyrebase import Stream

from lib.mvc.profile.model.Customer import Customer
from lib.mvc.profile.model.Staff import Staff
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
            self.__staff_data = Staff(data['uid'], data['name'], data['mail'],
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
        if data is not None and len(data) == 1:
            match message['event']:
                case "put":  # Funzione di aggiunta dati
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

    # Ritorna i dati dell'utente
    def get(self) -> Staff:
        return self.__staff_data

    # Salva un nuovo utente nel database
    @staticmethod
    def add(staff: Staff) -> str:
        # Converte l'utente in dizionario
        staff_dict = vars(staff)
        # Salva l'utente nel database e ne ritorna l'id
        return UserNetwork.create(staff_dict)

    # Elimina un utente dal database
    @staticmethod
    def delete(email: str):
        UserNetwork.delete_by_email(email)
