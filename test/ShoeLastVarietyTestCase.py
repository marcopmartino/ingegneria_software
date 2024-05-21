from unittest import TestCase

from lib.model.ShoeLastVariety import ShoeLastVariety, Gender, ShoeLastType, PlasticType, ProductType, Processing, \
    CompassType, Shoeing


class ShoeLastVarietyTestCase(TestCase):
    def setUp(self) -> None:
        # Inizializza la lista di varietà di forme
        self.shoe_last_variety_list: list[ShoeLastVariety] = [
            ShoeLastVariety(
                ProductType.ABBOZZO, Gender.BAMBINO, ShoeLastType.POLACCO, PlasticType.TIPO_1_DISCRETA,
            ),
            ShoeLastVariety(
                ProductType.ABBOZZO_SGROSSATO, Gender.DONNA, ShoeLastType.POLACCO, PlasticType.TIPO_2_BUONA, "40",
                Processing.SNODO_ALFA
            ),
            ShoeLastVariety(
                ProductType.FORMA_FINITA, Gender.BAMBINO, ShoeLastType.BASSA, PlasticType.TIPO_2_BUONA, "28",
                Processing.NESSUNA, CompassType.STANDARD, CompassType.NESSUNA, False,
                Shoeing.TACCO_FERRATO, False
            ),
            ShoeLastVariety(
                ProductType.FORMA_NUMERATA, Gender.UOMO, ShoeLastType.BASSA, PlasticType.TIPO_1_DISCRETA, "43",
                Processing.CUNEO, CompassType.RINFORZATA, CompassType.STANDARD, True,
                Shoeing.TUTTA_FERRATA, False, True, True, False
            ),
        ]

        # Inizializza la lista di descrizioni
        self.description_list: list[str] = [
            "Abbozzo, bambino, polacco, tipo 1",
            "Abbozzo sgrossato, donna, polacco, tipo 2, 40, snodo alfa",
            "Forma finita, bambino, bassa, tipo 2, 28, bussola standard, tacco ferrato",
            "Forma numerata, uomo, bassa, tipo 1, 43, cuneo, bussola rinforzata, seconda bussola standard, "
            "perno sotto tallone, tutta ferrata, segno anticollo, segni laterali"
        ]

    def test_shoe_last_variety_description(self) -> None:
        for index in range(len(self.shoe_last_variety_list)):
            self.assertEqual(self.shoe_last_variety_list[index].get_description(), self.description_list[index])
