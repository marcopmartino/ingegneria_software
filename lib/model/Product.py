class Product:

    def __init__(self, serial: str, type: str, details: str, amount: str):
        super(Product, self).__init__()
        self.serial = serial
        self.type = type
        self.details = details
        self.amount = amount

    # Aggiunge un nuovo prodotto nel magazzino
    @classmethod
    def new(cls, serial: str, type: str, details: str, amount: int):
        return cls(serial, type, details, str(amount))

    def update_amount(self, new_amount):
        self.amount = new_amount
