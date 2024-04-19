from lib.repository.PriceCatalogRepository import PriceCatalogRepository


class Article:
    def __init__(self, article_serial: str,
                 gender: str, size: str, shoe_last_type: str, plastic_type: int,
                 reinforced_compass: bool, second_compass_type: str, processing: str,
                 shoeing: str, numbering_antineck: bool, numbering_lateral: bool, numbering_heel: bool,
                 iron_tip: bool, pivot_under_heel: bool, creation_date: str, produced_article_shoe_lasts: int):
        super(Article, self).__init__()
        self.__article_serial = article_serial
        self.__gender = gender
        self.__size = size
        self.__shoe_last_type = shoe_last_type
        self.__plastic_type = plastic_type
        self.__reinforced_compass = reinforced_compass
        self.__second_compass_type = second_compass_type
        self.__processing = processing
        self.__shoeing = shoeing
        self.__numbering_antineck = numbering_antineck
        self.__numbering_lateral = numbering_lateral
        self.__numbering_heel = numbering_heel
        self.__iron_tip = iron_tip
        self.__pivot_under_heel = pivot_under_heel
        self.__creation_date = creation_date
        self.__produced_article_shoe_lasts = produced_article_shoe_lasts

    def get_article_serial(self):
        return self.__article_serial

    def get_gender(self):
        return self.__gender

    def get_size(self):
        return self.__size

    def get_shoe_last_type(self):
        return self.__shoe_last_type

    def get_plastic_type(self):
        return self.__plastic_type

    def get_reinforced_compass(self):
        return self.__reinforced_compass

    def get_second_compass_type(self):
        return self.__second_compass_type

    def get_processing(self):
        return self.__processing

    def get_shoeing(self):
        return self.__shoeing

    def get_numbering_antineck(self):
        return self.__numbering_antineck

    def get_numbering_lateral(self):
        return self.__numbering_lateral

    def get_numbering_heel(self):
        return self.__numbering_heel

    def get_iron_tip(self):
        return self.__iron_tip

    def get_pivot_under_heel(self):
        return self.__pivot_under_heel
