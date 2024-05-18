from lib.model.Product import Product


class Sketch(Product):

    def __init__(self, serial: str, product_type: str, gender: str, plastic: str,
                 sketch_type: str, details: str = None, amount: str = "0"):
        super().__init__(serial, product_type, details, amount)
        self._gender = gender
        self._plastic = plastic
        self._sketch_type = sketch_type

    def set_gender(self, gender: str):
        self._gender = gender

    def set_plastic(self, plastic: str):
        self._plastic = plastic

    def set_sketch_type(self, sketch_type: str):
        self._sketch_type = sketch_type

    def get_gender(self):
        return self._gender

    def get_plastic(self):
        return self._plastic

    def get_sketch_type(self):
        return self._sketch_type
