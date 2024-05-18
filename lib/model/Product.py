class Product:

    def __init__(self, serial: str, product_type: str, details: str = None, amount: str = "0"):
        super(Product, self).__init__()
        self.__serial = serial
        self._product_type = product_type
        self.__details = details
        self.__amount = amount

    # Aggiunge un nuovo prodotto nel magazzino
    @classmethod
    def new(cls, serial: str, product_type: str, details: str, amount: int):
        return cls(serial, product_type, details, str(amount))

    def update_amount(self, new_amount):
        self.__amount = new_amount

    def get_serial(self):
        return self.__serial

    def get_product_type(self):
        return self._product_type

    def get_details(self):
        return self.__details

    def get_amount(self):
        return self.__amount
