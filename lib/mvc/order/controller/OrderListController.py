# Controller per OrderListView
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
