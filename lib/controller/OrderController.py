from lib.controller.OrderBaseController import OrderBaseController
from lib.model.Order import Order
from lib.repository.ArticlesRepository import ArticlesRepository
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.repository.OrdersRepository import OrdersRepository
from lib.repository.StorageRepository import StorageRepository
from lib.repository.UsersRepository import UsersRepository
from lib.utility.ObserverClasses import Observer, AnonymousObserver
from res.Strings import OrderStateStrings


class OrderController(OrderBaseController):
    def __init__(self, order: Order):
        super().__init__()

        # Repositories
        self.__orders_repository: OrdersRepository = OrdersRepository()
        self.__articles_repository: ArticlesRepository = ArticlesRepository()
        self.__users_repository: UsersRepository = UsersRepository()
        self.__cash_register_repository: CashRegisterRepository = CashRegisterRepository()
        self.__storage_repository: StorageRepository = StorageRepository()

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

    def get_order_creator(self):
        return self.__users_repository.get_user_by_id(self.__order.get_customer_id())

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
        # Aggiorna lo stato dell'ordine
        self.__orders_repository.update_order_state_by_id(self.get_order_serial(), OrderStateStrings.PROCESSING)

    def complete_order(self):
        # Aggiorna lo stato dell'ordine
        self.__orders_repository.update_order_state_by_id(self.get_order_serial(), OrderStateStrings.COMPLETED)

        # Ottiene l'articolo dell'ordine
        order_article = self.get_order_article()

        # Cerca le forme compatibili con l'ordine
        product = self.__storage_repository.get_unassigned_product_by_shoe_last_variety(
            order_article.get_shoe_last_variety())

        # Sottrae la quantità da assegnare dalla quantità totale delle forme dello stesso tipo
        self.__storage_repository.update_product_quantity(
            product.get_item_id(), product.get_quantity() - self.__order.get_quantity())

        # Assegna le forme all'ordine
        self.__storage_repository.create_assigned_product(order_article.get_shoe_last_variety(), self.__order)

        # Numero attuale di paia prodotte dell'articolo dell'ordine
        current_produced_article_shoe_lasts = order_article.get_produced_article_shoe_lasts()

        # Aggiorna il numero del primo paio dell'ordine (totale prodotto finora + 1)
        self.__orders_repository.update_order_first_product_serial_by_id(
            self.get_order_serial(), current_produced_article_shoe_lasts + 1)

        # Aggiorna il numero di paia prodotte dell'articolo (totale prodotto finora + quantità dell'ordine)
        self.__articles_repository.update_article_production_counter_by_id(
            self.get_order_article_serial(), current_produced_article_shoe_lasts + self.__order.get_quantity())

    def deliver_order(self):
        # Aggiorna lo stato dell'ordine
        self.__orders_repository.update_order_state_by_id(self.get_order_serial(), OrderStateStrings.DELIVERED)

        # Cerca il prodotto
        product = self.__storage_repository.get_assigned_product_by_order_id(
            self.get_order_serial())

        # Rimuove le forme assegnate dal magazzino
        self.__storage_repository.delete_product(product.get_item_id())

        # Genera una transazione con l'incasso dell'ordine
        self.__cash_register_repository.create_transaction(
            f"Incasso ordine {self.get_order_serial()} ({self.__order.get_quantity()} paia)",
            self.__order.get_price()
        )

    # Ritorna il numero di paia di forme prodotte dell'ordine
    def get_produced_order_shoe_lasts(self) -> int:
        # Cerca il prodotto
        product = self.__storage_repository.get_unassigned_product_by_shoe_last_variety(
            self.get_order_article().get_shoe_last_variety())

        # Ritorna la quantità
        return product.get_quantity() if product is not None else 0

    def observe_order(self, callback: callable) -> Observer:
        observer = AnonymousObserver(callback)
        self.__order.attach(observer)
        self.__storage_repository.attach(observer)
        return observer

    def detach_order_observer(self, observer: Observer):
        self.__order.detach(observer)
        self.__storage_repository.detach(observer)
