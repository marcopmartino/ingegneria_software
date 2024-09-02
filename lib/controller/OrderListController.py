# Controller per OrderListView
from typing import Callable

from lib.controller.OrderBaseController import OrderBaseController
from lib.model.Order import Order, OrderState
from lib.model.ShoeLastVariety import ShoeLastVariety


class OrderListController(OrderBaseController):

    def __init__(self):
        super().__init__()

    # Imposta un osservatore per la repository
    def observe_order_list(self, callback: callable):
        self._orders_repository.observe(callback)

    # Ritorna un ordine in base all'id
    def get_order_by_id(self, order_id: str) -> Order:
        return self._orders_repository.get_order_by_id(order_id)

    # Ritorna la lista di ordini filtrata
    def get_order_list(self, filters: dict[str, any]) -> list[Order]:
        return self.filter_orders(filters, *self._orders_repository.get_order_list())

    # Filtra una lista degli ordini
    # noinspection PyMethodMayBeStatic
    def filter_orders(self, filters: dict[str, any], *orders: Order) -> list[Order]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio degli ordini

        # Parametri di filtro scelti dall'utente
        search_field: str = filters["searchcombobox"]  # Campo dell'ordine sulla base di cui filtrare
        search_text: str = filters["searchbox"]  # Valore del campo dell'ordine sulla base di cui filtrare
        allowed_states: list[OrderState] = []  # Stati dell'ordine da mostrare

        # In base ai parametri di filtro, determina se uno stato è ammesso a meno
        def append_state_if_allowed(filter_key: str, order_state: OrderState):
            if filters[filter_key]:
                allowed_states.append(order_state)

        # Eseguo la funzione per tutti gli stati possibili
        append_state_if_allowed("notstarted", OrderState.NOT_STARTED)
        append_state_if_allowed("working", OrderState.PROCESSING)
        append_state_if_allowed("completed", OrderState.COMPLETED)
        append_state_if_allowed("delivered", OrderState.DELIVERED)

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

            # Filtra la lista degli ordini
            for order in orders:

                # Se il testo di ricerca è vuoto viene saltato il filtro sul campo
                if search_text:
                    if search_text.lower() not in filter_field(order).lower():
                        continue

                # Se tutti gli stati sono ammessi viene saltato il filtro sullo stato
                if allowed_states_count != 4:
                    if order.get_state() not in allowed_states:
                        continue

                filtered_order_list.append(order)

        return filtered_order_list

    # Crea un ordine a partire dai dati della form
    def create_order(self, shoe_last_variety: ShoeLastVariety, quantity: int, price: float):

        # Controlla se esiste già un articolo con le caratteristiche desiderate
        article = self._articles_repository.get_article_by_shoe_last_variety(shoe_last_variety)

        # Se non esiste, crea un nuovo articolo con i dati della form. Ottiene il seriale dell'articolo
        if article is None:
            article_serial = self._articles_repository.create_article(shoe_last_variety)
        else:
            article_serial = article.get_article_serial()

        # Crea un nuovo ordine
        self._orders_repository.create_order(article_serial, quantity, price)
