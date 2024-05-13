from typing import Callable

from lib.model import Employee
from lib.model.Customer import Customer
from lib.model.User import User
from lib.repository.UsersRepository import UsersRepository


class WorkerListController:
    def __init__(self):
        super().__init__()
        self.__users_repository = UsersRepository()

    # Imposta un osservatore per la repository
    def observe_worker_list(self, callback: callable):
        self.__users_repository.observe(callback)

    # Ritorna un operaio in base all'id
    def get_worker_by_id(self, uid: str) -> Employee:
        return self.__users_repository.get_user_by_id(uid)

    # Ritorna la lista di operai filtrata
    def get_worker_list(self, filters: dict[str, any]) -> list[Employee]:
        return self.filter_workers(filters, *self.__users_repository.get_user_list())

    # Filtra una lista delle transazioni
    # noinspection PyMethodMayBeStatic
    def filter_workers(self, filters: dict[str, any], *users: User) -> list[Employee]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio degli operai

        # Parametri di filtro scelti dall'utente
        search_field: str = filters["searchcombobox"]  # Campo dell'operaio sulla base di cui filtrare
        search_text: str = filters["searchbox"]  # Valore del campo dell'operaio sulla base di cui filtrare

        # Inizializzo la lista degli elementi da ritornare
        filtered_worker_list: list[Employee] = []

        # Funzione che ritorna il campo dell'ordine sulla base di cui filtrare
        filter_field: Callable[[Employee], str] | None = None

        # Dato un dipendente, ne ritorna il nome
        def name(employee_: Employee) -> str:
            return employee_.get_name()

        # Dato un dipendente, ne ritorna l'email
        def email(employee_: Employee) -> str:
            return employee_.get_email()

        # Dato un dipendente, ne ritorna il numero di telefono
        def phone_number(employee_: Employee) -> str:
            return employee_.get_phone()

        # Dato un dipendente, ne ritorna il codice fiscale
        def fiscal_code(employee_: Employee) -> str:
            return employee_.get_CF()

        # In base a un parametro di filtro, assegna la funzione che ritorna il campo da filtrare
        match search_field:
            case "nome":
                filter_field = name
            case "email":
                filter_field = email
            case "telefono":
                filter_field = phone_number
            case "codice fiscale":
                filter_field = fiscal_code

        # Filtra la lista degli utenti
        for user in users:
            # Scarta gli utenti che non sono operai (i clienti e il manager)
            if isinstance(user, Customer) or user.is_manager():
                continue

            # Se il testo di ricerca è vuoto viene saltato il filtro sul campo
            if search_text:
                if search_text.lower() not in filter_field(user).lower():
                    continue

            filtered_worker_list.append(user)
            print(filtered_worker_list)

        return filtered_worker_list

    # Crea un nuovo operaio
    def create_worker(self, data):
        return self.__users_repository.create_worker(data)

    # Aggiorna un operaio
    def update_worker(self, data):
        return self.__users_repository.update_user_by_id(data["form_token"], data)

    # Elimina un operaio
    def delete_worker_by_id(self, worker_id: str):
        return self.__users_repository.delete_user_by_id(worker_id)
