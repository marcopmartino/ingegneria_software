from enum import Enum

from lib.model.Product import Product
from lib.model.StoredItems import StoredShoeLastVariety, StoredMaterial, StoredWaste
from lib.network.StorageNetwork import StorageNetwork
from lib.repository.Repository import Repository
from lib.utility.Singleton import RepositoryMeta


class StorageRepository(Repository, metaclass=RepositoryMeta):

    class Event(Enum):
        SHOE_LASTS_INITIALIZED = 0
        SHOE_LAST_CREATED = 1
        SHOE_LAST_UPDATED = 2
        MATERIALS_INITIALIZED = 3
        MATERIAL_UPDATED = 4
        WASTE_INITIALIZED = 5
        WASTE_UPDATED = 6

    def __init__(self):
        self.__products_list: list[StoredShoeLastVariety] = []
        self.__materials_list: list[StoredMaterial] = []
        self.__waste_list: list[StoredWaste] = []
        self.__storage_network: StorageNetwork = StorageNetwork()
        super().__init__(self.__storage_network.stream)

    def clear(self):
        self.__products_list = []
        self.__materials_list = []
        self.__waste_list = []

    # Usato internamente per istanziare e aggiungere un prodotto alla lista
    def __instantiate_and_append_product(self, serial: str, data: any):
        self.__products_list.append(StoredShoeLastVariety(
            serial, data["type"], data["details"], data["amount"]
        ))

    # Usato internamente per istanziare e aggiungere un materiale alla lista
    def __instantiate_and_append_materials(self, serial: str, data: any):
        self.__materials_list.append(Product(
            serial, data["type"], data["details"], data["amount"]
        ))

    # Usato internamente per istanziare e aggiungere un scarti alla lista
    def __instantiate_and_append_waste(self, serial: str, data: any):
        self.__waste_list.append(Product(
            serial, data["type"], data["details"], data["amount"]
        ))

    # Stream handler che aggiorna automaticamente le liste degli oggetti immagazzinati
    def _stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorno la lista dei prodotti così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        if data is not None:
            path = message["path"]
            match message["event"]:
                case "put":
                    # All'avvio del programma, quando viene caricata l'intera lista di prodotti
                    if path == "/":
                        for key, value in data.items():
                            self.__instantiate_and_append_product(key, value)
                    # Quando viene creato un nuovo prodotto
                    else:
                        self.__instantiate_and_append_product(path.split("/")[1], data)
                case "patch":
                    pass
                case "cancel":
                    pass

        # Notifico gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
        self.notify(message)

    # Ritorna la lista dei prodotti
    def get_products_list(self) -> list[Product]:
        return self.__products_list.copy()

    # Ritorna la lista dei materiali
    def get_materials_list(self) -> list[Product]:
        return self.__materials_list.copy()

    # Ritorna la lista degli scarti
    def get_wastes_list(self) -> list[Product]:
        return self.__waste_list.copy()

    # Ritorna un prodotto in base al suo numero
    def get_product_by_id(self, product_serial: str) -> Product:
        for product in self.__products_list:
            if product.get_serial() == product_serial:
                return product

    # Ritorna un materiale in base al suo numero
    def get_material_by_id(self, material_serial: str) -> Product:
        for material in self.__materials_list:
            if material.get_serial() == material_serial:
                return material

    # Ritorna un materiale in base al suo numero
    def get_waste_by_id(self, waste_serial: str) -> Product:
        for waste in self.__waste_list:
            if waste.get_serial() == waste_serial:
                return waste

    # Se il prodotto esiste già, ne ritorna il seriale. Altrimenti lo crea e ritorna il nuovo seriale
    def create_product(self, new_product_data: dict[str, any]) -> str:
        print(f"Nuovo prodotto:{new_product_data}")
        # Controlla se il prodotto esiste
        for product in self.__products_list:
            print(f"Prodotto:{vars(product)}")
            if (product.get_type() == new_product_data.get("type")
                    and product.get_details() == new_product_data.get("details")
                    and product.get_amount() == new_product_data.get("amount")):
                # Se il prodotto esiste, ne viene ritornato il seriale
                print("Trovato")
                return product.get_serial()

        # Se il prodotto non esiste, ne crea uno nuovo
        product_data = dict(
            type=new_product_data.get("type"),
            details=new_product_data.get("details"),
            amount=new_product_data.get("amount")
        )

        # Salva il prodotto nel database e ritorna il nuovo seriale
        return self.__storage_network.insert_product(product_data)

    # Se il materiale esiste già, ne ritorna il seriale. Altrimenti lo crea e ritorna il nuovo seriale
    def create_material(self, new_material_data: dict[str, any]) -> str:
        print(f"Nuovo materiale:{new_material_data}")
        # Controlla se il materiale esiste
        for material in self.__materials_list:
            print(f"Materiale:{vars(material)}")
            if (material.get_type() == new_material_data.get("type")
                    and material.get_details() == new_material_data.get("details")
                    and material.get_amount() == new_material_data.get("amount")):
                # Se il materiale esiste, ne viene ritornato il seriale
                print("Trovato")
                return material.get_serial()

        # Se il prodotto non esiste, ne crea uno nuovo
        material_data = dict(
            type=new_material_data.get("type"),
            details=new_material_data.get("details"),
            amount=new_material_data.get("amount")
        )

        # Salva il prodotto nel database e ritorna il nuovo seriale
        return self.__storage_network.insert_material(material_data)

    # Se lo scarto esiste già, ne ritorna il seriale. Altrimenti lo crea e ritorna il nuovo seriale
    def create_waste(self, new_waste_data: dict[str, any]) -> str:
        print(f"Nuovo scarto:{new_waste_data}")
        # Controlla se lo scarto esiste
        for waste in self.__waste_list:
            print(f"Scarto:{vars(waste)}")
            if (waste.get_type() == new_waste_data.get("type")
                    and waste.get_details() == new_waste_data.get("details")
                    and waste.get_amount() == new_waste_data.get("amount")):
                # Se lo scarto esiste, ne viene ritornato il seriale
                print("Trovato")
                return waste.get_serial()

            # Se il prodotto non esiste, ne crea uno nuovo
        waste_data = dict(
            type=new_waste_data.get("type"),
            details=new_waste_data.get("details"),
            amount=new_waste_data.get("amount")
        )

        # Salva il prodotto nel database e ritorna il nuovo seriale
        return self.__storage_network.insert_waste(waste_data)

    def get_max_storage(self, department: str):
        match department:
            case "product":
                return self.__storage_network.get_max_products_storage()
            case "material":
                return self.__storage_network.get_max_materials_storage()
            case "waste":
                return self.__storage_network.get_max_wastes_storage()

    def get_available_storage(self, department: str):
        match department:
            case "product":
                return self.__storage_network.get_available_products_storage()
            case "material":
                return self.__storage_network.get_available_materials_storage()
            case "waste":
                return self.__storage_network.get_available_wastes_storage()

    def get_used_storage(self, department: str):
        match department:
            case "product":
                return self.__storage_network.get_used_products_storage()
            case "material":
                return self.__storage_network.get_used_materials_storage()
            case "waste":
                return self.__storage_network.get_used_wastes_storage()

    def sort_list(self, department: str, reverse: bool):
        match department:
            case "product":
                return self.__products_list.sort(key=lambda k: k.get_amount(), reverse=reverse)
            case "material":
                return self.__materials_list.sort(key=lambda k: k.get_amount(), reverse=reverse)
            case "waste":
                return self.__waste_list.sort(key=lambda k: k.get_amount(), reverse=reverse)

