import firebase_admin.auth
from pyrebase.pyrebase import Stream

from lib import firebaseData as firebase
from lib.model.User import User
from lib.network.UserNetwork import UserNetwork
from lib.utility.ObserverClasses import Observable


class Customer(User, Observable):

    def __init__(self, company: str = None, phone: str = None, mail: str = None,
                 delivery: str = None, IVA: str = None, role: str = None):
        super().__init__(phone, mail, role)
        self.company = company
        self.delivery = delivery
        self.IVA = IVA
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
            self.company = data['company']
            self.phone = data['phone']
            self.email = data['mail']
            self.delivery = data['delivery']
            self.IVA = data['IVA']
            self.role = data['role']

    # Usato per modificare i dati di un utente
    def __edit_data(self, key: str, data: any):
        match key:
            case 'company':
                self.companyName = data
            case 'mail':
                self.mail = data
            case 'phone':
                self.phone = data
            case 'deliveryAddress':
                self.deliveryAddress = data
            case 'IVA':
                self.IVA = data

        # Usato per rimuovere i dati di un utente (in caso di eliminazione)

    # Usato eliminare il profilo dell'utente
    def __remove_data(self):
        self.delete(self, self.mail)
        self.companyName = None
        self.phone = None
        self.uid = None
        self.phone = None
        self.mail = None
        self.delivery = None
        self.IVA = None

    # Stream handler che aggiorna automaticamente i dati dell'utente
    def __stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        data = message['data']
        if data is not None:
            match message['event']:
                case "put":  # Funzione di aggiunta dati
                    data['mail'] = firebase.currentUser['email']
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
        UserNetwork.checkLogin(currentEmail, password)

    # Modifica i dati degli utenti nel database
    @staticmethod
    def setUserData(form_data: dict[str, any], newPassword, uid):
        UserNetwork.update(form_data, newPassword, uid)

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
            UserNetwork.delete_by_email(email)
        except Exception as e:
            print(e)
