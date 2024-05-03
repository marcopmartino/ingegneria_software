import operator

from lib.model.Product import Product
from lib.network.ProductNetwork import ProductNetwork
from lib.utility.ObserverClasses import Observable
from lib.utility.Singleton import ObservableSingleton


class StorageRepository(Observable, metaclass=ObservableSingleton):

    def __init__(self):
        super().__init__()
        self.__products_list: list[Product] = []
        self.__materials_list: list[Product] = []
        self.__storage_network: ProductNetwork = ProductNetwork()
        self.__storage_network.products_stream(self.__product_stream_handler)
        self.__storage_network.materials_stream(self.__materials_stream_handler)

    # Usato internamente per istanziare e aggiungere un prodotto alla lista
    def __instantiate_and_append_product(self, serial: str, data: any):
        self.__products_list.append(Product(
            serial, data["type"], data["details"], data["amount"]
        ))

    # Usato internamente per istanziare e aggiungere un materiale alla lista
    def __instantiate_and_append_materials(self, serial: str, data: any):
        self.__materials_list.append(Product(
            serial, data["type"], data["details"], data["amount"]
        ))

    # Stream handler che aggiorna automaticamente la lista dei prodotti
    def __product_stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorno la lista dei prodotti così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        if data is not None:
            path = message["path"]
            match message["event"]:
                case "put":
                    # All'avvio del programma, quando viene caricata l'intera lista di utenti
                    if path == "/":
                        for key, value in data.items():
                            self.__instantiate_and_append_product(key, value)

                    # Quando viene creato un nuovo articolo
                    else:
                        self.__instantiate_and_append_product(path.split("/")[1], data)
                case "patch":
                    pass
                case "cancel":
                    pass

        # Notifico gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
        self.notify(message)

    # Stream handler che aggiorna automaticamente la lista dei materiali
    def __materials_stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorno la lista dei prodotti così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        if data is not None:
            path = message["path"]
            match message["event"]:
                case "put":
                    # All'avvio del programma, quando viene caricata l'intera lista di utenti
                    if path == "/":
                        for key, value in data.items():
                            self.__instantiate_and_append_materials(key, value)

                    # Quando viene creato un nuovo articolo
                    else:
                        self.__instantiate_and_append_materials(path.split("/")[1], data)
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

    # Ritorna un prodotto in base al suo numero
    def get_product_by_id(self, product_serial: str) -> Product:
        for product in self.__products_list:
            if product.get_serial() == product_serial:
                return product

    # Ritorna un materiale in base al suo numero
    def get_materials_by_id(self, material_serial: str) -> Product:
        for material in self.__materials_list:
            if material.get_serial() == material_serial:
                return material

    # Se il prodotto esiste già, ne ritorna il seriale. Altrimenti lo crea e ritorna il nuovo seriale
    def create_product(self, new_product_data: dict[str, any]) -> str:
        print(f"Nuovo prodotto:{new_product_data}")
        # Controlla se il prodotto esiste
        for product in self.__products_list:
            print(f"Prodotto:{vars(product)}")
            if (product.get_type() == new_product_data.get("type")
                    and product.get_details() == new_product_data.get("details")
                    and product.get_amount() == new_product_data.get("amount")):
                # Se l'articolo esiste, ne viene ritornato il seriale
                print("Trovato")
                return product.get_serial()

        # Se il prodotto non esiste, ne crea uno nuovo
        product_data = dict(
            type=new_product_data.get("type"),
            details=new_product_data.get("details"),
            amount=new_product_data.get("amount")
        )

        # Salva il prodotto nel database e ritorna il nuovo seriale
        return self.__storage_network.insert(product_data)

    # Se il materiale esiste già, ne ritorna il seriale. Altrimenti lo crea e ritorna il nuovo seriale
    def create_material(self, new_material_data: dict[str, any]) -> str:
        print(f"Nuovo materiale:{new_material_data}")
        # Controlla se il materiale esiste
        for material in self.__materials_list:
            print(f"Materiale:{vars(material)}")
            if (material.get_type() == new_material_data.get("type")
                    and material.get_details() == new_material_data.get("details")
                    and material.get_amount() == new_material_data.get("amount")):
                # Se l'articolo esiste, ne viene ritornato il seriale
                print("Trovato")
                return material.get_serial()

        # Se il prodotto non esiste, ne crea uno nuovo
        material_data = dict(
            type=new_material_data.get("type"),
            details=new_material_data.get("details"),
            amount=new_material_data.get("amount")
        )

        # Salva il prodotto nel database e ritorna il nuovo seriale
        return self.__storage_network.insert(material_data)

    def get_max_storage(self):
        return self.__storage_network.get_max_storage()

    def get_available_storage(self):
        return self.__storage_network.get_available_storage()

    def get_used_storage(self):
        return self.__storage_network.get_used_storage()

    def sort_products_list(self, reverse: bool):
        self.__products_list.sort(key=lambda k: k.get_amount(), reverse=reverse)

    def sort_materials_list(self, reverse: bool):
        self.__materials_list.sort(key=lambda k: k.get_amount(), reverse=reverse)
