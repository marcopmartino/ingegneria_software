from lib.mvc.profile.model.Customer import Customer
from lib.network.UserNetwork import UserNetwork
from lib.utility.ObserverClasses import Observable
from lib.utility.Singleton import ObservableSingleton
from lib import firebaseData as firebase


class CustomerDataManager(Observable, metaclass=ObservableSingleton):

    def __init__(self):
        super().__init__()
        self.__customer_data = Customer()
        UserNetwork.stream(self.__stream_handler)

    # Usato per aggiungere i dati di un utente
    def __add_data(self, data: any):
        print(f"{data}")
        if data is not None:
            self.__customer_data = Customer(data['uid'], data['companyName'], data['mail'],
                                            data['phone'], data['deliveryAddress'], data['IVA'])

    # Usato per modificare i dati di un utente
    def __edit_data(self, key: str, data: any):
        match key:
            case 'company':
                self.__customer_data.companyName = data
            case 'mail':
                self.__customer_data.mail = data
            case 'phone':
                self.__customer_data.phone = data
            case 'deliveryAddress':
                self.__customer_data.deliveryAddress = data
            case 'mail':
                self.__customer_data.IVA = data

    # Usato per rimuovere i dati di un utente (in caso di eliminazione)
    def __remove_data(self):
        self.delete(self.__customer_data.email)
        self.__customer_data = None

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
        message['notifier'] = CustomerDataManager
        self.notify(message)

    # Ritorna i dati dell'utente
    def get(self) -> Customer:
        return self.__customer_data

    # Salva un nuovo utente nel database
    @staticmethod
    def add(customer: Customer) -> str:
        # Converte l'utente in dizionario
        customer_dict = vars(customer)
        # Salva l'utente nel database e ne ritorna l'id
        return UserNetwork.create(customer_dict)

    # Elimina un utente dal database
    @staticmethod
    def delete(email: str):
        UserNetwork.delete_by_email(email)
