from lib.model.StoredItems import StoredShoeLastVariety
from lib.repository.StorageRepository import StorageRepository


class ProductController:

    def __init__(self, product: StoredShoeLastVariety):
        super().__init__()

        # Repositories
        self.__products_repository: StorageRepository = StorageRepository()

        # Models
        self.__product: StoredShoeLastVariety = product

    def get_product(self):
        return self.__product

    def get_product_serial(self):
        return self.__product.get_item_id()

    def get_product_type(self):
        return self.__product.get_shoe_last_variety().get_product_type().value

    def get_plastic(self):
        return self.__product.get_shoe_last_variety().get_plastic_type().value

    def get_gender(self):
        return self.__product.get_shoe_last_variety().get_gender().value

    def get_sketch_type(self):
        return self.__product.get_shoe_last_variety().get_shoe_last_type().value

    def get_numbering_heel(self):
        return self.__product.get_shoe_last_variety().get_numbering_heel()

    def get_numbering_lateral(self):
        return self.__product.get_shoe_last_variety().get_numbering_lateral()

    def get_numbering_antineck(self):
        return self.__product.get_shoe_last_variety().get_numbering_antineck()

    def get_size(self):
        size = self.__product.get_shoe_last_variety().get_size()
        return size if size != "" else "N/A"

    def get_main_process(self):
        return self.__product.get_shoe_last_variety().get_processing().value

    def get_shoeing(self):
        return self.__product.get_shoe_last_variety().get_shoeing().value

    def get_first_compass(self):
        return self.__product.get_shoe_last_variety().get_first_compass_type().value

    def get_second_compass(self):
        return self.__product.get_shoe_last_variety().get_second_compass_type().value

    def get_pivot_under_heel(self):
        return self.__product.get_shoe_last_variety().get_pivot_under_heel()

    def get_iron_tip(self):
        return self.__product.get_shoe_last_variety().get_iron_tip()

    def get_description(self):
        return self.__product.get_shoe_last_variety().get_description()

    def get_amount(self):
        return self.__product.get_quantity()

    '''def update_order(self, data: dict[str, any], price: float):
        # Estrae la quantità (numero di paia di forme) dell'ordine
        quantity = data.pop("quantity")

        # Se non esiste, crea un nuovo articolo con i dati della form. Ritorna il seriale dell'ordine
        article_serial = self.__articles_repository.create_article(data)

        # Crea un nuovo ordine
        self.__orders_repository.update_order_by_id(self.get_order_serial(), article_serial, quantity, price)'''

    def delete_product_by_id(self):
        self.__products_repository.update_waste(self.get_plastic().value)
        self.__products_repository.delete_product_by_id(self.get_product_serial())

