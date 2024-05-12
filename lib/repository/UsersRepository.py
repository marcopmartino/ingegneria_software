from enum import Enum

from lib.firebaseData import Firebase
from lib.model import User
from lib.model.Customer import Customer
from lib.model.Employee import Employee
from lib.network.UsersNetwork import UsersNetwork
from lib.repository.Repository import Repository
from lib.utility.ObserverClasses import Message
from lib.utility.Singleton import RepositoryMeta
from lib.utility.UtilityClasses import PhoneFormatter


class UsersRepository(Repository, metaclass=RepositoryMeta):
    class Event(Enum):
        USERS_INITIALIZED = 0
        USER_CREATED = 1
        USER_DELETED = 2
        USER_UPDATED = 3

    def __init__(self):
        self.__users_list: list[User] = []
        self.__users_network: UsersNetwork = UsersNetwork()
        super().__init__(self.__users_network.stream)

    def clear(self):
        self.__users_list = []

    # Usato internamente per istanziare e aggiungere un utente alla lista
    def __instantiate_and_append_customer(self, uid: str, data: any):
        customer = Customer(
            uid, data["mail"], data["phone"], data["company"], data["delivery"], data["IVA"]
        )
        self.__users_list.append(customer)
        return customer

    def __instantiate_and_append_employee(self, uid: str, data: any):
        employee = Employee(
            uid, data["mail"], data["phone"], data["name"], data["CF"], data["birth_date"], data["role"] == "manager"
        )
        self.__users_list.append(employee)
        return employee

    # Stream handler che aggiorna automaticamente la lista degli utenti
    def _stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorno la lista degli utenti così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        path = message["path"]
        match message["event"]:
            case "put":
                # All'avvio del programma, quando viene caricata l'intera lista di utenti
                if path == "/":
                    if data is not None:
                        # Se l'utente attuale è un cliente, gli unici dati da caricare sono i suoi
                        if Firebase.auth.currentUserRole() == "customer":
                            self.__instantiate_and_append_customer(Firebase.auth.currentUserId(), data)


                        # Se l'utente attuale è un dipendente, bisogna caricare i dati di tutti gli utenti
                        else:
                            for key, value in data.items():
                                # Aggiunge un cliente o un dipendente in base al ruolo
                                if value['role'] == 'customer':
                                    self.__instantiate_and_append_customer(key, value)
                                else:
                                    self.__instantiate_and_append_employee(key, value)

                        # Notifico gli osservatori che la repository ha concluso l'inizializzazione
                        self.notify(Message(UsersRepository.Event.USERS_INITIALIZED, self.__users_list))

                    elif Firebase.auth.currentUserRole() == "customer":
                        # Caso in cui un cliente elimina il proprio account
                        for user in self.__users_list:
                            if user.get_uid() == Firebase.auth.currentUserId():
                                # Rimuove l'utente dalla lista
                                self.__users_list.remove(user)

                                # Prepara il messaggio per notificare gli osservatori della lista degli utenti
                                message = Message(UsersRepository.Event.USER_DELETED)
                                user.notify(message)  # Notifica eventuali osservatori del singolo utente
                                message.setData(user.get_uid())

                                # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                                self.notify(message)
                                break

                    else:
                        # Notifico gli osservatori che la repository ha concluso l'inizializzazione
                        self.notify(Message(UsersRepository.Event.USERS_INITIALIZED, self.__users_list))

                # Se il path è diverso allora siamo nell'ambito di un singolo utente della lista
                else:

                    # Estrae l'id dell'utente dal path
                    uid = path.split("/")[1]

                    # Quando viene creato un nuovo utente, data non è None
                    if data:
                        # Crea e aggiunge un utente alla lista di utenti della repository
                        new_user = self.__instantiate_and_append_customer(uid, data) if data['role'] == 'customer' \
                            else self.__instantiate_and_append_employee(uid, data)

                        # Prepara il messaggio per notificare gli osservatori della lista degli utenti
                        message = Message(UsersRepository.Event.USER_CREATED, new_user)

                        # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                        self.notify(message)

                    # Quando viene eliminato un utente, data è None
                    else:
                        for user in self.__users_list:
                            if user.get_uid() == uid:
                                # Rimuove l'utente dalla lista
                                self.__users_list.remove(user)

                                # Prepara il messaggio per notificare gli osservatori della lista degli utenti
                                message = Message(UsersRepository.Event.USER_DELETED)
                                user.notify(message)  # Notifica eventuali osservatori del singolo utente
                                message.setData(uid)

                                # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                                self.notify(message)
                                break

            # Aggiornamento di un utente
            case "patch":

                # Estrae e aggiorna i dati dei clienti (possono essere None se rimasti invariati)
                if path == "/":

                    print(self.__users_list[0])
                    print("Current UID: " + Firebase.auth.currentUserId())

                    # Prende l'utente corrispondente
                    user = self.get_user_by_id(Firebase.auth.currentUserId())

                    # Se un utente è stato trovato
                    if user is not None:

                        email = data.get("mail")
                        phone = data.get("phone")
                        company = data.get("company")
                        delivery = data.get("delivery")
                        iva = data.get("IVA")

                        if email is not None:
                            user.set_email(email)
                        if phone is not None:
                            user.set_phone(phone)
                        if company is not None:
                            user.set_company_name(company)
                        if delivery is not None:
                            user.set_delivery_address(delivery)
                        if iva is not None:
                            user.set_IVA(iva)

                        # Prepara il messaggio per notificare gli osservatori della lista degli utenti
                        message = Message(UsersRepository.Event.USER_UPDATED)
                        user.notify(message)  # Notifica eventuali osservatori del singolo utente
                        message.setData(user)

                        # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                        self.notify(message)

                # Estrae e aggiorna i dati dei dipendenti (possono essere None se rimasti invariati)
                else:

                    # Estrae il seriale dell'ordine dal path
                    uid = path.split("/")[1]

                    # Prende l'utente corrispondente
                    user = self.get_user_by_id(uid)

                    # Se un utente è stato trovato
                    if user is not None:

                        email = data.get("mail")
                        phone = data.get("phone")
                        name = data.get("name")
                        cf = data.get("CF")
                        birth_date = data.get("birth_date")

                        if email is not None:
                            user.set_email(email)
                        if phone is not None:
                            user.set_phone(phone)
                        if name is not None:
                            user.set_name(name)
                        if cf is not None:
                            user.set_CF(cf)
                        if birth_date is not None:
                            user.set_birth_date(birth_date)

                        # Prepara il messaggio per notificare gli osservatori della lista degli utenti
                        message = Message(UsersRepository.Event.USER_UPDATED)
                        user.notify(message)  # Notifica eventuali osservatori del singolo utente
                        message.setData(user)

                        # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                        self.notify(message)

            # Terminazione imprevista dello stream
            case "cancel":
                pass

    # Ritorna la lista degli utenti
    def get_user_list(self) -> list[User]:
        return self.__users_list

    # Ritorna un utente in base al suo numero
    def get_user_by_id(self, user_uid: str) -> User:
        for user in self.__users_list:
            if user.get_uid() == user_uid:
                return user

    # Crea un nuovo account utente cliente
    def create_customer(self, new_user_data: dict[str, any]) -> str:
        print(f"Nuovo cliente:{new_user_data}")

        # Crea un dizionario con i dati del nuovo utente
        user_data = dict(
            mail=new_user_data.get("email"),
            password=new_user_data.get("password"),
            phone=PhoneFormatter.format(new_user_data.get("telefono")),
            company=new_user_data.get("nome azienda"),
            delivery=new_user_data.get("indirizzo di recapito"),
            IVA=new_user_data.get("partita iva"),
            role="customer"
        )

        # Salva l'utente nel database e ne ritorna l'id
        return self.__users_network.register_user(user_data)

    # Crea un nuovo account utente operaio
    def create_worker(self, new_user_data: dict[str, any]) -> str:
        print(f"Nuovo operaio:{new_user_data}")

        # Crea un dizionario con i dati del nuovo utente
        user_data = dict(
            mail=new_user_data.get("email"),
            password=new_user_data.get("password"),
            phone=PhoneFormatter.format(new_user_data.get("telefono")),
            name=new_user_data.get("nome"),
            CF=new_user_data.get("codice fiscale"),
            birth_date=new_user_data.get("data di nascita"),
            role="worker"
        )

        # Salva l'utente nel database e ne ritorna l'id
        return self.__users_network.register_user(user_data)

    # Aggiorna un utente
    def update_user_by_id(self, user_id: str, new_user_data: dict[str, any]):
        # Crea un dizionario con i dati del nuovo utente
        user_data = dict(
            password=new_user_data.get("nuova password", new_user_data.get("password")),
            phone=PhoneFormatter.format(new_user_data.get("telefono")),
            name=new_user_data.get("nome"),
            CF=new_user_data.get("codice fiscale"),
            birth_date=new_user_data.get("data di nascita"),
            company=new_user_data.get("nome azienda"),
            delivery=new_user_data.get("indirizzo di recapito"),
            IVA=new_user_data.get("partita iva"),
        )

        # Aggiorna i dati dell'utente nel database
        return self.__users_network.update(user_id, user_data)

    # Elimina un utente
    def delete_user_by_id(self, user_id: str):
        self.__users_network.delete(user_id)

    # Autentica un utente (esegue il login)
    def authenticate_user(self, email: str, password: str):
        self.__users_network.authenticate_user(email, password)

    # Ri-autentica l'utente corrente
    def reauthenticate_current_user(self, password: str):
        self.__users_network.reauthenticate_current_user(password)
