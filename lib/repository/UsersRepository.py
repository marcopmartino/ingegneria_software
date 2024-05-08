from lib.model import User
from lib.model.Customer import Customer
from lib.model.Staff import Staff
from lib.network.UsersNetwork import UsersNetwork
from lib.repository.Repository import Repository
from lib.utility.Singleton import RepositoryMeta


class UsersRepository(Repository, metaclass=RepositoryMeta):

    def __init__(self):
        self.__users_list: list[User] = []
        self.__user_network: UsersNetwork = UsersNetwork()
        super().__init__(self.__user_network.stream)

    def clear(self):
        self.__users_list = []

    # Usato internamente per istanziare e aggiungere un utente alla lista
    def __instantiate_and_append_customer(self, uid: str, data: any):
        self.__users_list.append(Customer(
            uid, data["company"], data["phone"], data["mail"], data["delivery"],
            data["IVA"], data["role"]
        ))

    def __instantiate_and_append_staff(self, uid: str, data: any):
        self.__users_list.append(Staff(
            uid, data["name"], data["mail"], data["phone"], data["CF"],
            data["birth_date"], data["role"]))

    # Stream handler che aggiorna automaticamente la lista degli utenti
    def _stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorno la lista degli utenti così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        if data is not None:
            path = message["path"]
            match message["event"]:
                case "put":
                    # All'avvio del programma, quando viene caricata l'intera lista di utenti
                    if path == "/":
                        for key, value in data.items():
                            if value['role'] == 'customer':
                                self.__instantiate_and_append_customer(key, value)
                            else:
                                if value['role'] != 'admin':
                                    self.__instantiate_and_append_staff(key, value)

                    # Quando viene creato un nuovo articolo
                    else:
                        if data['role'] == 'customer':
                            self.__instantiate_and_append_customer(path.split("/")[1], data)
                        else:
                            self.__instantiate_and_append_staff(path.split("/")[1], data)
                case "patch":
                    pass
                case "cancel":
                    pass

        # Notifico gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
        self.notify(message)

    # Ritorna la lista degli articoli
    def get_user_list(self, role: str) -> list[User]:
        new_users_list = list()
        for user in self.__users_list:
            if user.get_role() == role:
                new_users_list.append(user)
        return new_users_list

    # Ritorna un articolo in base al suo numero
    def get_user_by_id(self, user_uid: str) -> User:
        for user in self.__users_list:
            if user.get_uid() == user_uid:
                return user

    # Se l'articolo esiste già, ne ritorna il seriale. Altrimenti lo crea e ritorna il nuovo seriale
    def create_user(self, new_user_data: dict[str, any], password) -> str:
        print(f"Nuovo utente:{new_user_data}")

        user = self.__user_network.create_worker_profile(new_user_data['mail'], password)
        print(new_user_data['mail'])
        user_data = dict()

        if new_user_data.get("role") == "customer":
            user_data["company"] = new_user_data.get("company")
            user_data["phone"] = new_user_data.get("phone")
            user_data["mail"] = new_user_data.get("mail")
            user_data["delivery"] = new_user_data.get("delivery")
            user_data["IVA"] = new_user_data.get("IVA")
            user_data["role"] = new_user_data.get("role")
        else:
            user_data["name"] = new_user_data.get("name")
            user_data["phone"] = new_user_data.get("phone")
            user_data["mail"] = new_user_data.get("mail")
            user_data["birth_date"] = new_user_data.get("birth_date")
            user_data["CF"] = new_user_data.get("CF")
            user_data["role"] = new_user_data.get("role")

        # Salva l'articolo nel database e ritorna il nuovo seriale
        self.__user_network.create_data(user_data, user)

        return user.get_uid()

    def authenticate_user(self, email: str, password: str):
        self.__user_network.authenticate_user(email, password)
