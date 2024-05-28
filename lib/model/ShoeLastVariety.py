from __future__ import annotations

from enum import Enum


# Tipo di prodotto (dipende dalle altre proprietà)
class ProductType(Enum):
    ABBOZZO = "Abbozzo"
    ABBOZZO_SGROSSATO = "Abbozzo sgrossato"
    FORMA_FINITA = "Forma finita"
    FORMA_NUMERATA = "Forma numerata"


# Genere della forma
class Gender(Enum):
    UOMO = "uomo"
    DONNA = "donna"
    BAMBINO = "bambino"


# Tipo di forma (data dall'altezza del collo della forma)
class ShoeLastType(Enum):
    BASSA = "bassa"
    POLACCO = "polacco"


# Tipo di plastica di cui è costituita la forma
class PlasticType(Enum):
    TIPO_1_DISCRETA = 1
    TIPO_2_BUONA = 2
    TIPO_3_OTTIMA = 3


# Tipo di bussola (cilindro metallico inserito alla base superiore del collo della forma)
class CompassType(Enum):
    NESSUNA = "nessuna"
    STANDARD = "standard"
    RINFORZATA = "rinforzata"


# Lavorazione della forma (aggiunta di parti mobili)
class Processing(Enum):
    NESSUNA = "nessuna"
    CUNEO = "cuneo"
    SNODO_ALFA = "alfa"
    SNODO_TENDO = "tendo"


# Ferratura della forma (ferratura della pianta della forma)
class Shoeing(Enum):
    NESSUNA = "nessuna"
    TACCO_FERRATO = "tacco"
    MEZZA_FERRATA = "mezza"
    TUTTA_FERRATA = "tutta"


# Classe che rappresenta una varietà della forma (insieme delle caratteristiche di una forma)
# Non rappresenta una forma concreta
class ShoeLastVariety:
    def __init__(self, product_type: ProductType | str, gender: Gender | str, shoe_last_type: ShoeLastType | str,
                 plastic_type: PlasticType | str, size: str = None, processing: Processing | str = Processing.NESSUNA,
                 first_compass_type: CompassType | str = CompassType.NESSUNA,
                 second_compass_type: CompassType | str = CompassType.NESSUNA, pivot_under_heel: bool = False,
                 shoeing: Shoeing | str = Shoeing.NESSUNA, iron_tip: bool = False, numbering_antineck: bool = False,
                 numbering_lateral: bool = False, numbering_heel: bool = False):
        super().__init__()
        # Tipo di prodotto
        self.__product_type = ProductType[product_type.upper()] if type(product_type) is str \
            else product_type

        # Genere
        self.__gender = Gender[gender.upper()] if type(gender) is str else gender

        # Tipo di forma
        self.__shoe_last_type = ShoeLastType[shoe_last_type.upper()] if type(shoe_last_type) is str \
            else shoe_last_type

        # Tipo di plastica
        self.__plastic_type = PlasticType[plastic_type.upper()] if type(plastic_type) is str \
            else plastic_type

        self.__size = size  # Taglia

        # Lavorazione
        self.__processing = Processing[processing.upper()] if type(processing) is str else processing

        # Prima bussola
        self.__first_compass_type = CompassType[first_compass_type.upper()] if type(first_compass_type) is str \
            else first_compass_type

        # Seconda bussola
        self.__second_compass_type = CompassType[second_compass_type.upper()] if type(second_compass_type) is str \
            else second_compass_type

        # Perno sotto tallone
        self.__pivot_under_heel = pivot_under_heel

        # Ferratura
        self.__shoeing = Shoeing[shoeing.upper()] if type(shoeing) is str else shoeing

        # Punta ferrata
        self.__iron_tip = iron_tip

        self.__numbering_antineck = numbering_antineck  # Segno anticollo
        self.__numbering_lateral = numbering_lateral  # Segni laterali
        self.__numbering_heel = numbering_heel  # Segno sul tallone

    def get_product_type(self) -> ProductType:
        return self.__product_type

    def get_gender(self) -> Gender:
        return self.__gender

    def get_shoe_last_type(self) -> ShoeLastType:
        return self.__shoe_last_type

    def get_plastic_type(self) -> PlasticType:
        return self.__plastic_type

    def get_size(self) -> str:
        return self.__size

    def get_first_compass_type(self) -> CompassType:
        return self.__first_compass_type

    def get_second_compass_type(self) -> CompassType:
        return self.__second_compass_type

    def get_processing(self) -> Processing:
        return self.__processing

    def get_shoeing(self) -> Shoeing:
        return self.__shoeing

    def get_numbering_antineck(self) -> str:
        return "Si" if self.__numbering_antineck else "No"

    def get_numbering_lateral(self) -> str:
        return "Si" if self.__numbering_lateral else "No"

    def get_numbering_heel(self) -> str:
        return "Si" if self.__numbering_heel else "No"

    def get_iron_tip(self) -> str:
        return "Si" if self.__iron_tip else "No"

    def get_pivot_under_heel(self) -> str:
        return "Si" if self.__pivot_under_heel else "No"

    def get_description(self) -> str:
        description_abbozzo = (f"{self.__product_type.value}, {self.__gender.value}, {self.__shoe_last_type.value}, "
                               f"tipo {str(self.__plastic_type.value)}")
        if self.__product_type == ProductType.ABBOZZO:
            return description_abbozzo

        else:
            description_abbozzo_sgrossato = (f"{description_abbozzo}, {self.__size}" +
                                             ("" if self.__processing == Processing.NESSUNA else
                                              f", {self.__processing.name.lower().replace("_", " ")}"))
            if self.__product_type == ProductType.ABBOZZO_SGROSSATO:
                return description_abbozzo_sgrossato

            else:
                description_forma_finita = (f"{description_abbozzo_sgrossato}, bussola "
                                            f"{self.__first_compass_type.value}" +
                                            ("" if self.__second_compass_type == CompassType.NESSUNA else
                                             f", seconda bussola {self.__second_compass_type.value}") +
                                            (", perno sotto tallone" if self.__pivot_under_heel else "") +
                                            ("" if self.__shoeing == Shoeing.NESSUNA else
                                             f", {self.__shoeing.name.lower().replace("_", " ")}") +
                                            (", punta ferrata" if self.__iron_tip else ""))
                if self.__product_type == ProductType.FORMA_FINITA:
                    return description_forma_finita

                else:
                    return (f"{description_forma_finita}" +
                            (", segno anticollo" if self.__numbering_antineck else "") +
                            (", segni laterali" if self.__numbering_lateral else "") +
                            (", segno sul tallone" if self.__numbering_heel else ""))

    def equals(self, shoe_last_variety: ShoeLastVariety) -> bool:
        return (
                self.__product_type == shoe_last_variety.get_product_type() and
                self.__gender == shoe_last_variety.get_gender() and
                self.__shoe_last_type == shoe_last_variety.get_shoe_last_type() and
                self.__plastic_type == shoe_last_variety.get_plastic_type() and
                self.__size == shoe_last_variety.get_size() and
                self.__processing == shoe_last_variety.get_processing() and
                self.__first_compass_type == shoe_last_variety.get_first_compass_type() and
                self.__second_compass_type == shoe_last_variety.get_second_compass_type() and
                self.__pivot_under_heel == shoe_last_variety.get_pivot_under_heel() and
                self.__shoeing == shoe_last_variety.get_shoeing() and
                self.__iron_tip == shoe_last_variety.get_iron_tip() and
                self.__numbering_antineck == shoe_last_variety.get_numbering_antineck() and
                self.__numbering_lateral == shoe_last_variety.get_numbering_lateral() and
                self.__numbering_heel == shoe_last_variety.get_numbering_heel()
        )