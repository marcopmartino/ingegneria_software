# Controller per OrderListView
from typing import Callable

from lib.mvc.order.model.Article import Article
from lib.mvc.order.model.ArticleList import ArticleList
from lib.mvc.order.model.Order import Order
from lib.mvc.order.model.OrderList import OrderList
from lib.mvc.pricecatalog.model.PriceCatalog import PriceCatalog


class OrderListController:

    def __init__(self):
        super().__init__()
        self.order_list = OrderList()
        self.article_list = ArticleList()
        self.price_catalog = PriceCatalog()

    # Ritorna un ordine in base all'id
    def get_order_by_id(self, order_id: str) -> Order:
        return self.order_list.get_by_id(order_id)

    # Ritorna la lista di ordini
    def get_order_list(self) -> list[Order]:
        return self.order_list.get()

    # Ritorna la lista di ordini filtrata
    def get_filtered_order_list(self, filters: dict[str, any]) -> list[Order]:
        return self.filter_order_list(self.order_list.get().copy(), filters)

    # Filtra una lista degli ordini
    @staticmethod
    def filter_order_list(order_list: list[Order], filters: dict[str, any]) -> list[Order]:

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

        # Numero di campi ammesssi
        allowed_states_count: int = len(allowed_states)

        # Se nessuno stato è ammesso, la lista degli ordini da mostrare è quella vuota
        if allowed_states_count:

            # Funzione che ritorna il campo dell'ordine sulla base di cui filtrare
            filter_field: Callable[[Order], str] | None = None

            # Dato un ordine, ne ritorna il seriale
            def order_serial(order_: Order) -> str:
                return order_.order_serial

            # Dato un ordine, ritorna il seriale del suo articolo
            def article_serial(order_: Order) -> str:
                return order_.article_serial

            # Dato un ordine, ritorna l'email del cliente che lo ha creato
            def customer(order_: Order) -> str:
                return order_.customer_id

            # In base a un parametro di filtro, assegna la funzione che ritorna il campo da filtrare
            match search_field:
                case "ordine":
                    filter_field = order_serial
                case "articolo":
                    filter_field = article_serial
                case "cliente":
                    filter_field = customer

            # Filtra la lista degli ordini
            for order in reversed(order_list):

                # Se il testo di ricerca è vuoto viene saltato il filtro sul campo
                if search_text:
                    if search_text not in filter_field(order):
                        order_list.remove(order)
                        continue

                # Se tutti gli stati sono ammessi viene saltato il filtro sullo stato
                if allowed_states_count != 4:
                    if order.state not in allowed_states:
                        order_list.remove(order)

        else:
            order_list = []

        return order_list

    # Calcola il prezzo dell'ordine in base ai dati della form
    def get_order_price(self, data: dict[str, any]) -> float:
        return self.price_catalog.calculate_price(
            data["gender"], data["type"], data["plastic"], data["first"], data["second"], data["processing"],
            data["shoeing"], data["antineck"], data["lateral"], data["heel"], data["shoetip"], data["pivot"],
            data["quantity"]
        )

    # Crea un ordine a partire dai dati della form
    def create_order(self, data: dict[str, any], price: float):
        # Crea un nuovo articolo con i dati della form
        article = Article.new(
            data["gender"], data["size"], data["type"], data["plastic"], data["first"], data["second"],
            data["processing"], data["shoeing"], data["antineck"], data["lateral"], data["heel"], data["shoetip"],
            data["pivot"]
        )

        print(vars(article))

        # Controlla se l'articolo esiste e in caso affermativo ne ritorna anche il numero
        article_exists, article_serial = self.article_list.exists(article)

        print(article_exists)

        # Se non esiste già, aggiungo il nuovo articolo
        if not article_exists:
            article_serial = self.article_list.add(article)

        print(article_serial)

        # Creo e aggiungo l'ordine
        quantity = data["quantity"]
        self.order_list.add(Order.new(article_serial, quantity, price))
