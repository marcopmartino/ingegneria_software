from lib.model.SemiFinished import SemiFinished


class Finished(SemiFinished):
    def __init__(self, serial: str, product_type: str, gender: str, plastic: str, sketch_type: str,
                 numbering: str, size: str, main_process: str, shoeing: str, first_compass: str,
                 second_compass: str = None, pivot_under_heel: bool = False, iron_tip: bool = False,
                 details: str = None, amount: str = "0"):
        super().__init__(serial, product_type, gender, plastic, sketch_type, size, main_process, shoeing,
                         first_compass, second_compass, pivot_under_heel, iron_tip, details, amount)
        self._numbering = numbering

    def set_numbering(self, numbering: str):
        self._numbering = numbering

    def get_numbering(self):
        return self._numbering
