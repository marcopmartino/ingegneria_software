from lib.controller.OrderBaseController import OrderBaseController
from lib.model.Order import Order
from lib.model.Product import Product
from lib.repository.ArticlesRepository import ArticlesRepository
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.repository.OrdersRepository import OrdersRepository
from lib.repository.StorageRepository import StorageRepository
from lib.repository.UsersRepository import UsersRepository
from lib.utility.ObserverClasses import Observer, AnonymousObserver
from res.Strings import OrderStateStrings


class ProductController:

    def __init__(self, product: Product):
        super().__init__()

        # Repositories
        self.__products_repository: StorageRepository = StorageRepository()

        # Models
        self.__product: Product = product

    def get_product(self):
        return self.__product

    def get_product_serial(self):
        return self.__product.get_serial()

    def get_product_type(self):
        return self.__product.get_product_type()

    def get_plastic(self):
        return self.get_plastic()

    def get_gender(self):
        return self.__product.get_gender()

    def get_sketch_type(self):
        return self.__product.get_sketch_type()

    def get_numbering(self):
        return self.__product.get_numbering()

    def get_size(self):
        return self.__product.get_size()

    def get_main_process(self):
        return self.__product.get_main_process()

    def get_shoeing(self):
        return self.__product.get_shoeing()

    def get_first_compass(self):
        return self.__product.get_first_compass()

    def get_second_compass(self):
        return self.__product.get_second_compass()

    def get_pivot_under_heel(self):
        return self.__product.get_pivot_under_heel()

    def get_iron_tip(self):
        return self.__product.get_iron_tip()

    def get_details(self):
        return self.__product.get_details()

    def get_amount(self):
        return self.__product.get_amount()

    '''def update_order(self, data: dict[str, any], price: float):
        # Estrae la quantità (numero di paia di forme) dell'ordine
        quantity = data.pop("quantity")

        # Se non esiste, crea un nuovo articolo con i dati della form. Ritorna il seriale dell'ordine
        article_serial = self.__articles_repository.create_article(data)

        # Crea un nuovo ordine
        self.__orders_repository.update_order_by_id(self.get_order_serial(), article_serial, quantity, price)'''

    def delete_product_by_id(self):
        self.__products_repository.update_waste(self.get_plastic())
        self.__products_repository.delete_product_by_id(self.get_product_serial())

