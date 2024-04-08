from lib.firebaseData import currentUserId
from lib.mvc.order.model.Article import Article
from lib.mvc.order.model.ArticleList import ArticleList
from datetime import datetime

from res.Strings import OrderStateStrings


class Order:

    def __init__(self, order_serial: str, article_serial: str, state: str, customer_id: str, quantity: int,
                 price: float, first_product_serial: int, creation_date: str):
        super(Order, self).__init__()
        self.order_serial = order_serial
        self.article_serial = article_serial
        self.state = state
        self.customer_id = customer_id
        self.quantity = quantity
        self.price = price
        self.first_product_serial = first_product_serial
        self.creation_date = creation_date

    # Crea un nuovo ordine
    @classmethod
    def new(cls, article_serial: str, quantity: int, price: float):
        return cls('', article_serial, OrderStateStrings.NOT_STARTED, currentUserId(), quantity, price, -1,
                   datetime.today().strftime('%d/%m/%Y'))

    def article(self) -> Article:
        return ArticleList().get_by_id(self.article_serial)

    def update_price(self):
        self.price = self.article().price(self.quantity)
