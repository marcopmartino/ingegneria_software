class Product:

    def __init__(self, serial: str, type: str, details: str, amount: str):
        super(Product, self).__init__()
        self.__serial = serial
        self.__type = type
        self.__details = details
        self.__amount = amount

    # Aggiunge un nuovo prodotto nel magazzino
    @classmethod
    def new(cls, serial: str, type: str, details: str, amount: int):
        return cls(serial, type, details, str(amount))

    def update_amount(self, new_amount):
        self.__amount = new_amount

    def get_serial(self):
        return self.__serial

    def get_type(self):
        return self.__type

    def get_details(self):
        return self.__details

    def get_amount(self):
        return self.__amount
