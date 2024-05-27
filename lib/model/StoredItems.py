from abc import ABC, abstractmethod
from enum import Enum

from lib.model.ShoeLastVariety import ShoeLastVariety, PlasticType


class StoredItem(ABC):
    def __init__(self, item_id: str, stored_quantity: int):
        super().__init__()
        self.__item_id = item_id
        self.__stored_quantity = stored_quantity

    def get_item_id(self) -> str:
        return self.__item_id

    def get_quantity(self) -> int:
        return self.__stored_quantity

    def set_quantity(self, quantity: int) -> None:
        self.__stored_quantity = quantity

    @abstractmethod
    def update(self, new_data: dict[str, any]):
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class UncategorizedItem(StoredItem):
    def __init__(self, item_id: str, stored_quantity: int, description: str):
        super().__init__(item_id, stored_quantity)
        self.__description = description

    def get_description(self) -> str:
        return self.__description

    def update(self, new_data: dict[str, any]):
        for key, value in new_data.items():
            match key:
                case "amount":
                    self.set_quantity(value)


class StoredWaste(StoredItem):
    def __init__(self, item_id: str, stored_quantity: int, plastic_type: PlasticType | str):
        super().__init__(item_id, stored_quantity)
        self.__plastic_type = PlasticType[str(plastic_type).upper()]

    def get_plastic_type(self) -> PlasticType:
        return self.__plastic_type

    def get_description(self):
        return f"Scarti di produzione - Plastica tipo {self.__plastic_type.value}"

    def update(self, new_data: dict[str, any]):
        for key, value in new_data.items():
            match key:
                case "amount":
                    self.set_quantity(value)
                case "plastic_type":
                    self.__plastic_type = value


class MaterialType(Enum):
    PARTE_PER_FERRATURA = "Parte per ferratura"
    PARTE_PER_TORNITURA = "Parte per tornitura"
    BUSSOLA = "Bussola"
    ALTRO = "Altro"


class MaterialDescription(Enum):
    PIASTRA_CORTA = "Piastra sottile corta"
    PIASTRA_MEDIA = "Piastra sottile media"
    PIASTRA_LUNGA = "Piastra sottile lunga"
    PIASTRA_PUNTA = "Piastra per punta"
    BUSSOLA_STANDARD = "Bussola standard"
    BUSSOLA_RINFORZATA = "Bussola rinforzata"
    INCHIOSTRO = "Inchiostro indelebile"
    PERNO = "Perno"
    MOLLA = "Molla per cuneo"
    GANCIO_ALFA = "Gancio per snodo alfa"
    GANCIO_TENDO = "Gancio per snodo tendo"


class StoredMaterial(StoredItem):
    def __init__(self, item_id: str, stored_quantity: int, material_type: MaterialType | str,
                 material_description: MaterialDescription | str):
        super().__init__(item_id, stored_quantity)
        self.__material_type = MaterialType[material_type.upper()] if type(material_type) is str else material_type
        self.__material_description = MaterialDescription[material_description.upper()] if type(material_description) is str \
            else material_description

    def get_material_type(self) -> MaterialType:
        return self.__material_type

    @property
    def get_description(self):
        return self.__material_description.value

    def update(self, new_data: dict[str, any]):
        for key, value in new_data.items():
            match key:
                case "material_description":
                    self.__material_description = MaterialDescription[str(value)]
                case "material_type":
                    self.__material_type = MaterialType[str(value)]
                case "amount":
                    self.set_quantity(value)


class StoredShoeLastVariety(StoredItem):
    def __init__(self, item_id: str, stored_quantity: int, shoe_last_variety: ShoeLastVariety):
        super().__init__(item_id, stored_quantity)
        self.__shoe_last_variety = shoe_last_variety

    def get_shoe_last_variety(self) -> ShoeLastVariety:
        return self.__shoe_last_variety

    def set_shoe_last_variety(self, shoe_last_variety: ShoeLastVariety) -> None:
        self.__shoe_last_variety = shoe_last_variety

    def get_description(self) -> str:
        return self.__shoe_last_variety.get_description()

    def update(self, new_data: dict[str, any]):
        for key, value in new_data.items():
            match key:
                case "amount":
                    self.set_quantity(value)
                case _:
                    self.__shoe_last_variety.update(key, value)


class AssignedShoeLastVariety(StoredShoeLastVariety):
    def __init__(self, item_id: str, quantity: int, shoe_last_variety: ShoeLastVariety, assigned_order_id: str):
        super().__init__(item_id, quantity, shoe_last_variety)
        self.__assigned_order_id = assigned_order_id

    def get_assigned_order_id(self) -> str:
        return self.__assigned_order_id

    def set_assigned_order_id(self, assigned_order_id: str) -> None:
        self.__assigned_order_id = assigned_order_id

    def get_description(self) -> str:
        return f"Forma assegnate all'ordine {self.__assigned_order_id}"
