from __future__ import annotations

from enum import Enum

from lib.model.CashRegisterTransaction import CashRegisterTransaction
from lib.network.CashRegisterNetwork import CashRegisterNetwork
from lib.repository.Repository import Repository
from lib.utility.ObserverClasses import Message
from lib.utility.Singleton import RepositoryMeta
from lib.utility.UtilityClasses import DatetimeUtils


class CashRegisterRepository(Repository, metaclass=RepositoryMeta):
    class Event(Enum):
        TRANSACTION_CREATED = 0
        TRANSACTION_DELETED = 1
        TRANSACTION_UPDATED = 2

    def __init__(self):
        super().__init__()
        self.__transaction_list: list[CashRegisterTransaction] = []  # Inizializza il registro di cassa
        self.__cash_register_network = CashRegisterNetwork()

    # Apre uno stream di dati
    def open_stream(self):
        self._stream = self.__cash_register_network.stream(self.__stream_handler)

    # Usato internamente per istanziare e aggiungere una nuova transazione al registro
    def __instantiate_and_append_transaction(self, serial: str, data: any) -> CashRegisterTransaction:
        order = CashRegisterTransaction(
            serial, data["description"], data["creation_date"], data["amount"], data["is_revenue"]
        )
        self.__transaction_list.append(order)
        return order

    # Stream handler che aggiorna automaticamente il registro di cassa
    def __stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorna il registro di cassa così che utenti diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        path = message["path"]
        match message["event"]:

            # Ottenimento\inserimento\eliminazione di transazioni
            case "put":

                # All'avvio del programma, quando viene caricato l'intero registro di cassa
                if path == "/":
                    # Se c'è almeno una transazione nella lista
                    if data:
                        for key, value in data.items():
                            # Crea e aggiunge una transazione al registro di cassa della repository
                            self.__instantiate_and_append_transaction(key, value)

                # Se il path è diverso allora siamo nell'ambito di una singola transazione
                else:
                    # Estrae l'id della transazione dal path
                    transaction_id = path.split("/")[1]

                    # Quando viene creata una nuova transazione, data non è None
                    if data:
                        # Crea e aggiunge una transazione al registro di cassa della repository
                        transaction = self.__instantiate_and_append_transaction(transaction_id, data)

                        # Prepara il messaggio per notificare gli osservatori del registro di cassa
                        message = Message(CashRegisterRepository.Event.TRANSACTION_CREATED, transaction)

                    # Quando viene eliminata una transazione, data è None
                    else:
                        for transaction in self.__transaction_list:
                            if transaction.get_transaction_id() == transaction_id:
                                # Rimuove la transazione dal registro di cassa
                                self.__transaction_list.remove(transaction)

                                # Prepara il messaggio per notificare gli osservatori del registro di cassa
                                message = Message(CashRegisterRepository.Event.TRANSACTION_DELETED)
                                message.setData(transaction_id)
                                break

                    # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                    self.notify(message)

            # Aggiornamento di una transazione
            case "patch":
                # Estrae l'id della transazione dal path
                transaction_id = path.split("/")[1]

                print("Updating transaction " + transaction_id)

                # Prende la transazione corrispondente
                transaction = self.get_transaction_by_id(transaction_id)

                print("Found transaction " + transaction.__str__())

                # Estraggo i dati (possono essere None se rimasti invariati)
                description: str | None = data.get("description")
                is_revenue: bool | None = data.get("is_revenue")
                amount: float | None = data.get("amount")

                # Aggiorna la transazione
                if description is not None:
                    transaction.set_description(description)
                if is_revenue is not None:
                    transaction.set_transaction_type(is_revenue)
                if amount is not None:
                    transaction.set_amount(amount)

                # Prepara il messaggio per notificare gli osservatori della lista delle transazioni
                message = Message(CashRegisterRepository.Event.TRANSACTION_UPDATED, transaction)

                # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                self.notify(message)

            # Terminazione imprevista dello stream
            case "cancel":
                pass

    # Ritorna la lista delle transazioni
    def get_transaction_list(self) -> list[CashRegisterTransaction]:
        return self.__transaction_list

    # Cerca una transazione in base al suo id e lo ritorna
    def get_transaction_by_id(self, transaction_id: str) -> CashRegisterTransaction:
        for transaction in self.__transaction_list:
            if transaction.get_transaction_id() == transaction_id:
                return transaction

    # Salva la nuova transazione nel database
    def create_transaction(self, description: str, amount: float, is_revenue: bool) -> str:
        # Crea un dizionario con i dati dela nuova transazione
        transaction_data = dict(
            description=description,
            amount=amount,
            is_revenue=is_revenue,
            creation_date=DatetimeUtils.current_date()
        )
        # Salva la transazione nel database e ne ritorna l'id
        return self.__cash_register_network.insert(transaction_data)

    # Aggiorna una transazione
    def update_transaction_by_id(self, transaction_id: str, description: str, amount: float, is_revenue: bool):
        # Crea un dizionario con i campi della transazione da aggiornare
        transaction_data = dict(
            description=description,
            amount=amount,
            is_revenue=is_revenue,
        )
        # Salva la transazione nel database e ne ritorna l'id
        return self.__cash_register_network.update(transaction_id, transaction_data)

    # Elimina una transazione
    def delete_transaction_by_id(self, transaction_id: str):
        self.__cash_register_network.delete(transaction_id)
