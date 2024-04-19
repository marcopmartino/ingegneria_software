from lib.controller.OrderFormController import OrderFormController
from lib.model.Order import Order
from lib.repository.ArticlesRepository import ArticlesRepository
from lib.repository.OrdersRepository import OrdersRepository
from lib.utility.ObserverClasses import Observer, AnonymousObserver
from res.Strings import OrderStateStrings


class OrderController(OrderFormController):
    def __init__(self, order: Order):
        super().__init__()

        # Repositories
        self.__orders_repository: OrdersRepository = OrdersRepository()
        self.__articles_repository: ArticlesRepository = ArticlesRepository()

        # Models
        self.__order: Order = order

    def get_order(self):
        return self.__order

    def get_order_serial(self):
        return self.__order.get_order_serial()

    def get_order_state(self):
        return self.__order.get_state()

    def get_order_article(self):
        return self.__articles_repository.get_article_by_id(self.__order.get_article_serial())

    def get_order_article_serial(self):
        return self.__order.get_article_serial()

    def update_order(self, data: dict[str, any], price: float):
        # Estrae la quantità (numero di paia di forme) dell'ordine
        quantity = data.pop("quantity")

        # Se non esiste, crea un nuovo articolo con i dati della form. Ritorna il seriale dell'ordine
        article_serial = self.__articles_repository.create_article(data)

        # Crea un nuovo ordine
        self.__orders_repository.update_order_by_id(self.get_order_serial(), article_serial, quantity, price)

    def delete_order(self):
        self.__orders_repository.delete_order_by_id(self.get_order_serial())

    def start_order(self):
        self.__orders_repository.update_order_state_by_id(self.get_order_serial(), OrderStateStrings.PROCESSING)

    def complete_order(self):
        self.__orders_repository.update_order_state_by_id(self.get_order_serial(), OrderStateStrings.COMPLETED)
        ''' Assegnare le forme finite all'ordine '''

    def deliver_order(self):
        self.__orders_repository.update_order_state_by_id(self.get_order_serial(), OrderStateStrings.DELIVERED)
        ''' Rimuovere le form associate all'ordine dal magazzino '''

    def observe_order(self, callback: callable) -> Observer:
        observer = AnonymousObserver(callback)
        self.__order.attach(observer)
        return observer

    def detach_order_observer(self, observer: Observer):
        self.__order.detach(observer)
