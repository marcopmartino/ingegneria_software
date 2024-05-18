from lib.model.Product import Product
from lib.model.Sketch import Sketch


class SemiFinished(Sketch):

    def __init__(self, serial: str, product_type: str, gender: str, plastic: str, sketch_type: str,
                 size: str, main_process: str, shoeing: str, first_compass: str,
                 second_compass: str = None, pivot_under_heel: bool = False, iron_tip: bool = False,
                 details: str = None, amount: str = "0"):
        super().__init__(serial, product_type, gender, plastic, sketch_type, details, amount)
        self._size = size  # Taglia
        self._main_process = main_process  # Lavorazione principale
        self._shoeing = shoeing  # Ferratura
        self._first_compass = first_compass  # Prima bussola
        self._second_compass = second_compass  # Seconda bussola
        self._pivot_under_heel = pivot_under_heel  # Perno sotto tacco
        self._iron_tip = iron_tip  # Punta ferrata

    def set_size(self, size: str):
        self._size = size

    def set_main_process(self, main_process: str):
        self._main_process = main_process

    def set_shoeing(self, shoeing: str):
        self._shoeing = shoeing

    def set_first_compass(self, first_compass: str):
        self._first_compass = first_compass

    def set_second_compass(self, second_compass: str):
        self._second_compass = second_compass

    def set_pivot_under_heel(self, pivot_under_heel: bool):
        self._pivot_under_heel = pivot_under_heel

    def set_iron_tip(self, iron_tip: bool):
        self._iron_tip = iron_tip

    def get_size(self):
        return self._size

    def get_main_process(self):
        return self._main_process

    def get_shoeing(self):
        return self._shoeing

    def get_first_compass(self):
        return self._first_compass

    def get_second_compass(self):
        return self._second_compass

    def get_pivot_under_heel(self):
        return self._pivot_under_heel

    def get_iron_tip(self):
        return self._iron_tip
