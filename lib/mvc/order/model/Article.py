from enum import Enum
from lib.mvc.pricecatalog.model.PriceCatalog import PriceCatalog


class Article:
    def __init__(self, article_serial: str,
                 gender: str, size: str, shoe_last_type: str, plastic_type: int,
                 reinforced_compass: bool, second_compass_type: str, processing: str,
                 shoeing: str, numbering_antineck: bool, numbering_lateral: bool, numbering_heel: bool,
                 iron_tip: bool, pivot_under_heel: bool, produced_article_shoe_lasts: int):
        super(Article, self).__init__()
        self.article_serial = article_serial
        self.gender = gender
        self.size = size
        self.shoe_last_type = shoe_last_type
        self.plastic_type = plastic_type
        self.reinforced_compass = reinforced_compass
        self.second_compass_type = second_compass_type
        self.processing = processing
        self.shoeing = shoeing
        self.numbering_antineck = numbering_antineck
        self.numbering_lateral = numbering_lateral
        self.numbering_heel = numbering_heel
        self.iron_tip = iron_tip
        self.pivot_under_heel = pivot_under_heel
        self.produced_article_shoe_lasts = produced_article_shoe_lasts

    # Crea un nuovo articolo
    @classmethod
    def new(cls, gender: str, size: str, shoe_last_type: str, plastic_type: int,
            reinforced_compass: bool, second_compass_type: str, processing: str, shoeing: str, numbering_antineck: bool,
            numbering_lateral: bool, numbering_heel: bool, iron_tip: bool, pivot_under_heel: bool):
        return cls('', gender, size, shoe_last_type, plastic_type, reinforced_compass, second_compass_type, processing,
                   shoeing, numbering_antineck, numbering_lateral, numbering_heel, iron_tip, pivot_under_heel, 0)

    # Calcola il prezzo di un certo numero di paia di forme associate all'articolo in base agli attuali prezzi di
    # listino
    def price(self, quantity: int = 1) -> float:
        return PriceCatalog().calculate_price(
            self.gender, self.shoe_last_type, self.plastic_type, self.reinforced_compass, self.second_compass_type,
            self.processing, self.shoeing, self.numbering_antineck, self.numbering_lateral, self.numbering_heel,
            self.iron_tip, self.pivot_under_heel, quantity
        )
