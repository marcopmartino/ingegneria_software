# Controller per OrderListView
from typing import Callable

from lib.controller.OrderFormController import OrderFormController
from lib.firebaseData import getUserRole, currentUserId
from lib.model.Article import Article
from lib.model.Customer import Customer
from lib.repository.ArticlesRepository import ArticlesRepository
from lib.model.Order import Order
from lib.repository.OrdersRepository import OrdersRepository
from lib.repository.PriceCatalogRepository import PriceCatalogRepository


class OrderListController(OrderFormController):

    def __init__(self):
        super().__init__()
        self.__orders_repository = OrdersRepository()
        self.__articles_repository = ArticlesRepository()

    # Imposta un osservatore per la repository
    def observe_order_list(self, callback: callable):
        self.__orders_repository.observe(callback)

    # Ritorna un ordine in base all'id
    def get_order_by_id(self, order_id: str) -> Order:
        return self.__orders_repository.get_order_by_id(order_id)

    # Ritorna la lista di ordini filtrata
    def get_order_list(self, filters: dict[str, any]) -> list[Order]:
        return self.filter_orders(filters, *self.__orders_repository.get_order_list())

    # Filtra una lista degli ordini
    # noinspection PyMethodMayBeStatic
    def filter_orders(self, filters: dict[str, any], *orders: Order) -> list[Order]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio degli ordini

        # Parametri di filtro scelti dall'utente
        search_field: str = filters["searchcombobox"]  # Campo dell'ordine sulla base di cui filtrare
        search_text: str = filters["searchbox"]  # Valore del campo dell'ordine sulla base di cui filtrare
        allowed_states: list[str] = []  # Stati dell'ordine da mostrare

        # In base ai parametri di filtro, determina se uno stato è ammesso a meno
        def append_state_if_allowed(filter_key: str, state_name: str):
            if filters[filter_key]:
                allowed_states.append(state_name)

        # Eseguo la funzione per tutti gli stati possibili
        append_state_if_allowed("notstarted", "Non iniziato")
        append_state_if_allowed("working", "In lavorazione")
        append_state_if_allowed("completed", "Completato")
        append_state_if_allowed("delivered", "Consegnato")

        # Numero di stati ammessi
        allowed_states_count: int = len(allowed_states)

        # Inizializzo la lista degli elementi da ritornare
        filtered_order_list: list[Order] = []

        # Se nessuno stato è ammesso, la lista degli ordini da mostrare è quella vuota
        if allowed_states_count:

            # Funzione che ritorna il campo dell'ordine sulla base di cui filtrare
            filter_field: Callable[[Order], str] | None = None

            # Dato un ordine, ne ritorna il seriale
            def order_serial(order_: Order) -> str:
                return order_.get_order_serial()

            # Dato un ordine, ritorna il seriale del suo articolo
            def article_serial(order_: Order) -> str:
                return order_.get_article_serial()

            # In base a un parametro di filtro, assegna la funzione che ritorna il campo da filtrare
            match search_field:
                case "ordine":
                    filter_field = order_serial
                case "articolo":
                    filter_field = article_serial

            # Funzione che ritorna True se l'utente non è autorizzato a visualizzare l'ordine
            filter_user: Callable[[str], bool] | None = None

            # Ritorna True se l'ordine è stato creato da un utente diverso
            def customer_filter(creator_id: str) -> bool:
                return creator_id != currentUserId()

            # Il filtro è passato automaticamente
            def no_filter(_: str) -> bool:
                return False

            # In base a un parametro di filtro, assegna la funzione che ritorna il campo da filtrare
            match getUserRole():
                case "customer":
                    filter_user = customer_filter
                case _:
                    filter_user = no_filter

            # Filtra la lista degli ordini
            for order in orders:

                # Stabilisce se l'utente è autorizzato a visualizzare l'ordine
                if filter_user(order.get_customer_id()):
                    continue

                # Se il testo di ricerca è vuoto viene saltato il filtro sul campo
                if search_text:
                    if search_text not in filter_field(order):
                        continue

                # Se tutti gli stati sono ammessi viene saltato il filtro sullo stato
                if allowed_states_count != 4:
                    if order.get_state() not in allowed_states:
                        continue

                filtered_order_list.append(order)

        return filtered_order_list

    # Crea un ordine a partire dai dati della form
    def create_order(self, data: dict[str, any], price: float):
        # Estrae la quantità (numero di paia di forme) dell'ordine
        quantity = data.pop("quantity")

        # Se non esiste, crea un nuovo articolo con i dati della form. Ritorna il seriale dell'ordine
        article_serial = self.__articles_repository.create_article(data)

        # Crea un nuovo ordine
        self.__orders_repository.create_order(article_serial, quantity, price)
