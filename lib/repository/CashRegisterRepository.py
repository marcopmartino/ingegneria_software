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
        CASH_AVAILABILITY_INITIALIZED = 0
        CASH_AVAILABILITY_UPDATED = 1
        TRANSACTIONS_INITIALIZED = 2
        TRANSACTION_CREATED = 3
        TRANSACTION_DELETED = 4
        TRANSACTION_UPDATED = 5

    def __init__(self):
        self.__cash_availability: float = 0  # Inizializza la disponibilità di cassa
        self.__transaction_list: list[CashRegisterTransaction] = []  # Inizializza la lista delle transazioni
        self.__cash_register_network = CashRegisterNetwork()
        super().__init__(self.__cash_register_network.stream)

    def clear(self):
        self.__cash_availability = 0
        self.__transaction_list = []

    # Usato internamente per istanziare e aggiungere una nuova transazione al registro
    def __instantiate_and_append_transaction(self, serial: str, data: any) -> CashRegisterTransaction:
        order = CashRegisterTransaction(
            serial, data["description"], data["payment_date"], data["amount"]
        )
        self.__transaction_list.append(order)
        return order

    # Stream handler che aggiorna automaticamente il registro di cassa
    def _stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorna il registro di cassa così che utenti diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        path = message["path"]
        match message["event"]:

            # Ottenimento\inserimento\eliminazione di transazioni
            case "put":

                # All'apertura dello Stream, quando viene caricato l'intero registro di cassa
                if path == "/":
                    # Se c'è almeno una transazione nella lista
                    if data:
                        # Aggiorno la disponibilità di cassa
                        self.__cash_availability = data.get("cash_availability", 0)

                        # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                        self.notify(Message(
                            CashRegisterRepository.Event.CASH_AVAILABILITY_INITIALIZED,
                            self.__cash_availability
                        ))

                        # Estraggo le transazioni
                        data = data.get("transactions")

                        if data:
                            for key, value in data.items():
                                # Crea e aggiunge una transazione al registro di cassa della repository
                                self.__instantiate_and_append_transaction(key, value)

                            # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                            self.notify(Message(
                                CashRegisterRepository.Event.TRANSACTIONS_INITIALIZED,
                                self.__transaction_list
                            ))

                # Se il path è diverso allora siamo nell'ambito di una singola transazione
                else:

                    # Estrae le sezioni del percorso
                    path_sections = path.split("/")

                    # Stabilisce se si tratta di un aggiornamento alla disponibilità di cassa o a una transazione
                    if path_sections[1] == "cash_availability":
                        # Aggiorna la disponibilità di cassa
                        self.__cash_availability = data

                        # Prepara il messaggio per notificare gli osservatori del registro di cassa
                        message = Message(CashRegisterRepository.Event.CASH_AVAILABILITY_UPDATED, data)

                    else:
                        # Estrae l'id della transazione dal path
                        transaction_id = path_sections[2]

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
                transaction_id = path.split("/")[2]

                print("Updating transaction " + transaction_id)

                # Prende la transazione corrispondente
                transaction = self.get_transaction_by_id(transaction_id)

                print("Found transaction " + transaction.__str__())

                # Estraggo i dati (possono essere None se rimasti invariati)
                description: str | None = data.get("description")
                date: str | None = data.get("payment_date")
                amount: float | None = data.get("amount")

                # Aggiorna la transazione
                if description is not None:
                    transaction.set_description(description)
                if date is not None:
                    transaction.set_payment_date(date)
                if amount is not None:
                    transaction.set_amount(amount)

                # Prepara il messaggio per notificare gli osservatori del registro di cassa
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
    def create_transaction(self, description: str, amount: float, payment_date: str) -> str:
        # Crea un dizionario con i dati dela nuova transazione
        transaction_data = dict(
            description=description,
            amount=amount,
            payment_date=payment_date
        )
        # Salva la transazione nel database e ne ritorna l'id
        return self.__cash_register_network.insert(transaction_data)

    # Aggiorna una transazione
    def update_transaction_by_id(self, transaction_id: str, description: str, amount: float, payment_date: str):
        # Crea un dizionario con i campi della transazione da aggiornare
        transaction_data = dict(
            description=description,
            amount=amount,
            payment_date=payment_date,
        )
        # Salva la transazione nel database e ne ritorna l'id
        return self.__cash_register_network.update(transaction_id, transaction_data)

    # Elimina una transazione
    def delete_transaction_by_id(self, transaction_id: str):
        self.__cash_register_network.delete(transaction_id)
