from unittest import TestCase

from lib.model.ShoeLastVariety import ShoeLastVariety, Gender, ShoeLastType, PlasticType, ProductType, Processing, \
    CompassType, Shoeing


class ShoeLastVarietyTestCase(TestCase):
    def setUp(self) -> None:
        # Inizializza la lista di forme
        self.shoe_last_variety_list: list[ShoeLastVariety] = [
            ShoeLastVariety(
                Gender.BAMBINO, ShoeLastType.POLACCO, PlasticType.TIPO_1_DISCRETA,
            ),
            ShoeLastVariety(
                Gender.DONNA, ShoeLastType.POLACCO, PlasticType.TIPO_2_BUONA, "40", Processing.SNODO_ALFA
            ),
            ShoeLastVariety(
                Gender.BAMBINO, ShoeLastType.BASSA, PlasticType.TIPO_2_BUONA, "28", Processing.NESSUNA,
                CompassType.STANDARD, CompassType.NESSUNA, False, Shoeing.TACCO_FERRATO, False
            ),
            ShoeLastVariety(
                Gender.UOMO, ShoeLastType.BASSA, PlasticType.TIPO_1_DISCRETA, "43", Processing.CUNEO,
                CompassType.RINFORZATA, CompassType.STANDARD, True, Shoeing.TUTTA_FERRATA, False,
                True, True, False
            ),
        ]

        # Inizializza la lista di tipi di prodotto
        self.product_type_list: list[ProductType] = [
            ProductType.ABBOZZO,
            ProductType.ABBOZZO_SGROSSATO,
            ProductType.FORMA_FINITA,
            ProductType.FORMA_NUMERATA
        ]

        # Inizializza la lista di descrizioni
        self.description_list: list[str] = [
            "Abbozzo, bambino, polacco, tipo 1",
            "Abbozzo sgrossato, donna, polacco, tipo 2, 40, snodo alfa",
            "Forma finita, bambino, bassa, tipo 2, 28, bussola standard, tacco ferrato",
            "Forma numerata, uomo, bassa, tipo 1, 43, cuneo, bussola rinforzata, seconda bussola standard, "
            "perno sotto tallone, tutta ferrata, segno anticollo, segni laterali"
        ]

    def test_shoe_last_variety_product_type(self) -> None:
        for index in range(len(self.shoe_last_variety_list)):
            self.assertEqual(self.shoe_last_variety_list[index].get_product_type(), self.product_type_list[index])

    def test_shoe_last_variety_description(self) -> None:
        for index in range(len(self.shoe_last_variety_list)):
            self.assertEqual(self.shoe_last_variety_list[index].get_description(), self.description_list[index])
