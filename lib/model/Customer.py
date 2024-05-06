from pyrebase.pyrebase import Stream

from lib import firebaseData as firebase
from lib.firebaseData import Firebase
from lib.model.User import User
from lib.network.UsersNetwork import UsersNetwork
from lib.utility.ObserverClasses import Observable


class Customer(User, Observable):

    def __init__(self, uid: str = None, company: str = None, phone: str = None, mail: str = None,
                 delivery: str = None, IVA: str = None, role: str = None):
        super().__init__(uid, phone, mail, role)
        self.__company = company
        self.__delivery = delivery
        self.__IVA = IVA
        self.__stream: Stream | None = None

    def open_stream(self):
        self._uid = Firebase.auth.currentUserId()
        self.__stream = UsersNetwork.stream_by_id(self._uid, self.__stream_handler)

    def close_stream(self):
        self.__stream.close()

    # Usato per aggiungere i dati di un utente
    def __add_data(self, data: any):
        if data is not None:
            self._uid = data['uid']
            self.__company = data['company']
            self._phone = data['phone']
            self._email = data['mail']
            self.__delivery = data['delivery']
            self.__IVA = data['IVA']
            self._role = data['role']

    # Usato per modificare i dati di un utente
    def __edit_data(self, key: str, data: any):
        match key:
            case 'uid':
                self._uid = data
            case 'company':
                self.__companyName = data
            case 'mail':
                self._mail = data
            case 'phone':
                self._phone = data
            case 'deliveryAddress':
                self.__delivery = data
            case 'IVA':
                self.__IVA = data

        # Usato per rimuovere i dati di un utente (in caso di eliminazione)

    # Usato eliminare il profilo dell'utente
    def __remove_data(self):
        self.delete(self, self._mail)
        self.__companyName = None
        self._phone = None
        self._mail = None
        self.__delivery = None
        self.__IVA = None

    # Stream handler che aggiorna automaticamente i dati dell'utente
    def __stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        data = message['data']
        if data is not None:
            match message['event']:
                case "put":  # Funzione di aggiunta dati
                    data['uid'] = Firebase.auth.currentUserId()
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

    # Ritorna i dati dell'utente
    def get(self):
        return self

    @staticmethod
    def checkLogin(currentEmail, password):
        UsersNetwork.checkLogin(currentEmail, password)

    # Modifica i dati degli utenti nel database
    @staticmethod
    def setUserData(form_data: dict[str, any], newPassword, uid):
        UsersNetwork.update(form_data, newPassword, uid)

    # Salva un nuovo utente nel database
    # @staticmethod
    '''def add(customer: Customer) -> str:
        # Converte l'utente in dizionario
        customer_dict = vars(customer)
        # Salva l'utente nel database e ne ritorna l'id
        return UserNetwork.create(customer_dict)'''

    def to_dict(self):
        return vars(self)

    # Elimina un utente dal database
    @staticmethod
    def delete(self, email: str):
        try:
            UsersNetwork.delete_by_email(email)
        except Exception as e:
            print(e)
