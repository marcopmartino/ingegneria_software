from typing import Callable

from lib.model.CashRegisterTransaction import CashRegisterTransaction
from lib.repository.CashRegisterRepository import CashRegisterRepository


class CashRegisterController:
    def __init__(self):
        self.__cash_register_repository = CashRegisterRepository()

    # Imposta un osservatore per la repository
    def observe_transaction_list(self, callback: callable):
        self.__cash_register_repository.observe(callback)

    # Ritorna una transazione in base all'id
    def get_transaction_by_id(self, transaction_id: str) -> CashRegisterTransaction:
        return self.__cash_register_repository.get_transaction_by_id(transaction_id)

    # Ritorna la lista di transazioni filtrata
    def get_transaction_list(self, filters: dict[str, any]) -> list[CashRegisterTransaction]:
        return self.filter_transactions(filters, *self.__cash_register_repository.get_transaction_list())

    # Filtra una lista delle transazioni
    # noinspection PyMethodMayBeStatic
    def filter_transactions(self, filters: dict[str, any], *transactions: CashRegisterTransaction) \
            -> list[CashRegisterTransaction]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio delle transazioni

        # Parametri di filtro scelti dall'utente
        search_field: str = filters["searchcombobox"]  # Campo della transazione sulla base di cui filtrare
        search_text: str = filters["searchbox"]  # Valore del campo della transazione sulla base di cui filtrare
        allowed_types: list[bool] = []  # Tipi transazione da mostrare

        # In base ai parametri di filtro, determina se un tipo di transazione è ammesso a meno
        def append_type_if_allowed(filter_key: str, type_value: bool):
            if filters[filter_key]:
                allowed_types.append(type_value)

        # Eseguo la funzione per tutti gli stati possibili
        append_type_if_allowed("revenue", True)
        append_type_if_allowed("spending", False)

        # Numero di tipi ammessi
        allowed_types_count: int = len(allowed_types)

        # Inizializzo la lista degli elementi da ritornare
        filtered_transaction_list: list[CashRegisterTransaction] = []

        # Se nessun tipo è ammesso, la lista degli ordini da mostrare è quella vuota
        if allowed_types_count:

            # Funzione che ritorna il campo dell'ordine sulla base di cui filtrare
            filter_field: Callable[[CashRegisterTransaction], str] | None = None

            # Data una transazione, ne ritorna l'id
            def transaction_id(transaction_: CashRegisterTransaction) -> str:
                return transaction_.get_transaction_id()

            # Dato un ordine, ne ritorna la descrizione
            def description(transaction_: CashRegisterTransaction) -> str:
                return transaction_.get_description()

            # In base a un parametro di filtro, assegna la funzione che ritorna il campo da filtrare
            match search_field:
                case "id":
                    filter_field = transaction_id
                case "descrizione":
                    filter_field = description

            # Filtra la lista delle transazioni
            for transaction in transactions:

                # Se il testo di ricerca è vuoto viene saltato il filtro sul campo
                if search_text:
                    if search_text.lower() not in filter_field(transaction).lower():
                        continue

                # Se tutti i tipi sono ammessi viene saltato il filtro sul tipo
                if allowed_types_count != 2:
                    if (transaction.get_amount() > 0) not in allowed_types:
                        continue

                filtered_transaction_list.append(transaction)

        return filtered_transaction_list

    # Crea una transazione a partire dai dati della form
    def create_transaction(self, data: dict[str, any]):
        self.__cash_register_repository.create_transaction(data["descrizione"], data["importo"], data["data"])

    # Aggiorna una transazione
    def update_transaction_by_id(self, transaction_id: str, data: dict[str, any]):
        self.__cash_register_repository.update_transaction_by_id(
            transaction_id, data["descrizione"], data["importo"], data["data"])

    # Elimina una transazione
    def delete_transaction_by_id(self,  transaction_id: str):
        self.__cash_register_repository.delete_transaction_by_id(transaction_id)
