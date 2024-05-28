from enum import Enum

from lib.model.ShoeLastVariety import ShoeLastVariety
from lib.model.StoredItems import StoredShoeLastVariety, StoredMaterial, StoredWaste, StoredItem
from lib.network.StorageNetwork import StorageNetwork
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.repository.Repository import Repository
from lib.utility.ObserverClasses import Message
from lib.utility.Singleton import RepositoryMeta


class StorageRepository(Repository, metaclass=RepositoryMeta):
    class Event(Enum):
        MAX_STORAGE_INITIALIZED = 0
        MAX_STORAGE_UPDATED = 1
        PRODUCTS_INITIALIZED = 2
        PRODUCT_CREATED = 3
        PRODUCT_DELETED = 4
        PRODUCT_UPDATED = 5
        MATERIALS_INITIALIZED = 6
        MATERIAL_CREATED = 7
        MATERIAL_DELETED = 8
        MATERIAL_UPDATED = 9
        WASTE_INITIALIZED = 10
        WASTE_CREATED = 11
        WASTE_DELETED = 12
        WASTE_UPDATED = 13

    def __init__(self):
        self.__max_storage = 0
        self.__products_list: list[StoredShoeLastVariety] = []
        self.__materials_list: list[StoredMaterial] = []
        self.__waste_list: list[StoredWaste] = []
        self.__storage_network: StorageNetwork = StorageNetwork()
        super().__init__(self.__storage_network.stream)

    def clear(self):
        self.__max_storage = 0
        self.__products_list = []
        self.__waste_list = []

    # Usato internamente per istanziare e aggiungere un prodotto alla lista
    def __instantiate_and_append_product(self, serial: str, data: any):
        shoe = ShoeLastVariety(
            data['product_type'], data['gender'], data['shoe_last_type'],
            data['plastic_type'], data['size'], data['processing'],
            data['first_compass_type'], data['second_compass_type'], data['pivot_under_heel'],
            data['shoeing'], data['iron_tip'], data['numbering_antineck'],
            data['numbering_lateral'], data['numbering_heel']
        )

        product = StoredShoeLastVariety(serial, data['amount'], shoe)
        self.__products_list.append(product)
        return product

    # Usato internamente per istanziare e aggiungere un materiale alla lista
    def __instantiate_and_append_material(self, serial: str, data: any):
        material = StoredMaterial(
            serial, data['amount'], data['material_type'], data['material_description']
        )
        self.__materials_list.append(material)
        return material

    # Usato internamente per istanziare e aggiungere un scarti alla lista
    def __instantiate_and_append_waste(self, serial: str, data: any):
        waste = StoredWaste(
            serial, data['amount'], data['plastic_type']
        )

        self.__waste_list.append(waste)
        return waste

    # Stream handler che aggiorna automaticamente la lista di prodotto, materiali e scarti
    def _stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorno la lista dei prodotti così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        path = message["path"]
        if data is not None:
            match message["event"]:
                case "put":
                    # All'avvio del programma, quando viene caricata l'intera lista di prodotti
                    if path == "/":
                        if data:
                            self.__max_storage = data.get('max_capacity', 0)

                            # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                            self.notify(Message(
                                StorageRepository.Event.MAX_STORAGE_INITIALIZED,
                                self.__max_storage
                            ))

                            # Estraggo i prodotti
                            products = data.get("products")
                            materials = data.get("materials")
                            waste = data.get("waste")

                            if products:
                                for key, value in products.items():
                                    # Crea e aggiunge un prodotto alla lista dei prodotti
                                    self.__instantiate_and_append_product(key, value)

                                # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                                self.notify(Message(
                                    StorageRepository.Event.PRODUCTS_INITIALIZED,
                                    self.__products_list
                                ))

                            if materials:
                                for key, value in materials.items():
                                    # Crea e aggiunge un materiale alla lista dei materiali
                                    self.__instantiate_and_append_material(key, value)

                                # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                                self.notify(Message(
                                    StorageRepository.Event.MATERIALS_INITIALIZED,
                                    self.__materials_list
                                ))

                            if waste:
                                for key, value in waste.items():
                                    # Crea e aggiunge uo scarto alla lista degli scarti
                                    self.__instantiate_and_append_waste(key, value)

                                # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                                self.notify(Message(
                                    StorageRepository.Event.WASTE_INITIALIZED,
                                    self.__waste_list
                                ))

                    # Se il path è diverso allora sto operando sul singolo campo
                    else:
                        # Estrae il percorso su cui sta operando
                        path = path.split('/')

                        # Controlla se si tratta della capacità massima del magazzino
                        if path[1] == "max_capacity":
                            # Aggiorna magazzino massimo
                            self.__max_storage = data

                            # Prepara il messaggio per notificare gli osservatori del magazzino
                            message = Message(StorageRepository.Event.MAX_STORAGE_UPDATED, data)

                        else:
                            # Estrae l'id del prodotto del magazzino
                            element_id = path[2]

                            # Controlla di che tipo di prodotto si tratta
                            match path[1]:
                                case "products":
                                    # Se viene creato un prodotto data non è None
                                    if data:
                                        # Crea e aggiunge un prodotto alla lista dei prodotti
                                        product = self.__instantiate_and_append_product(element_id, data)

                                        # Prepara il messaggio per notificare gli osservatori del magazzino
                                        message = Message(StorageRepository.Event.PRODUCT_CREATED, product)

                                    # Quando viene eliminato un prodotto data è None
                                    else:
                                        for product in self.__products_list:
                                            if product.get_item_id() == element_id:
                                                # Rimuove il prodotto dalla lista dei prodotti
                                                self.__products_list.remove(product)

                                                # Prepara il messaggio per notificare gli osservatori del magazzino
                                                message = Message(StorageRepository.Event.PRODUCT_DELETED)
                                                message.setData(element_id)
                                                break
                                case "materials":
                                    # Se viene creato un materiale data non è None
                                    if data:
                                        # Crea e aggiunge un materiale alla lista dei materiali
                                        material = self.__instantiate_and_append_material(element_id, data)

                                        # Prepara il messaggio per notificare gli osservatori del magazzino
                                        message = Message(StorageRepository.Event.MATERIAL_CREATED, material)

                                    # Quando viene eliminato un prodotto data è None
                                    else:
                                        for material in self.__materials_list:
                                            if material.get_item_id() == element_id:
                                                # Rimuove il materiale dalla lista dei materiali
                                                self.__materials_list.remove(material)

                                                # Prepara il messaggio per notificare gli osservatori del magazzino
                                                message = Message(StorageRepository.Event.MATERIAL_DELETED)
                                                message.setData(element_id)
                                                break
                                case "waste":
                                    # Se viene creato uno scarto data non è None
                                    if data:
                                        # Crea e aggiunge uno scarto alla lista degli scarti
                                        waste = self.__instantiate_and_append_waste(element_id, data)

                                        # Prepara il messaggio per notificare gli osservatori del magazzino
                                        message = Message(StorageRepository.Event.WASTE_CREATED, waste)

                                    # Quando viene eliminato un prodotto data è None
                                    else:
                                        for waste in self.__waste_list:
                                            if waste.get_item_id() == element_id:
                                                # Rimuove lo scarto dalla lista degli scarti
                                                self.__waste_list.remove(waste)

                                                # Prepara il messaggio per notificare gli osservatori del magazzino
                                                message = Message(StorageRepository.Event.WASTE_DELETED)
                                                message.setData(element_id)
                                                break

                        # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                        self.notify(message)

                # Aggiornamento del magazzino
                case "patch":

                    element: StoredItem

                    # Estrae il percorso dell'elemento che è stato modificato e il suo id
                    path = path.split('/')
                    element_type = path[1]
                    element_id = path[2]

                    if len(data) != 1:
                        if element_type == "products":
                            element = self.__instantiate_and_append_product(element_id, data)
                            message = Message(StorageRepository.Event.PRODUCT_CREATED, element)
                    else:
                        print("Updating element" + element_id)
                        # Prende l'elemento corrispondente

                        if element_type == "products":
                            element = self.get_product_by_id(element_id)
                            message = Message(StorageRepository.Event.PRODUCT_UPDATED)
                        elif element_type == "materials":
                            element = self.get_material_by_id(element_id)
                            message = Message(StorageRepository.Event.MATERIAL_UPDATED)
                        else:
                            element = self.get_waste_by_id(element_id)
                            message = Message(StorageRepository.Event.WASTE_UPDATED)

                        element.set_quantity(data['amount'])
                        message.setData(element)

                    self.notify(message)

                case "cancel":
                    pass

    # Ritorna la lista dei prodotti
    def get_products_list(self) -> list[StoredShoeLastVariety]:
        return self.__products_list.copy()

    # Ritorna la lista dei materiali
    def get_materials_list(self) -> list[StoredMaterial]:
        return self.__materials_list.copy()

    # Ritorna la lista degli scarti
    def get_waste_list(self) -> list[StoredWaste]:
        return self.__waste_list.copy()

    # Ritorna un prodotto in base al suo numero
    def get_product_by_id(self, product_serial: str) -> StoredShoeLastVariety:
        for product in self.__products_list:
            if product.get_item_id() == product_serial:
                return product

    # Ritorna un materiale in base al suo numero
    def get_material_by_id(self, material_serial: str) -> StoredMaterial:
        for material in self.__materials_list:
            if material.get_item_id() == material_serial:
                return material

    # Ritorna un materiale in base al suo numero
    def get_waste_by_id(self, waste_serial: str) -> StoredWaste:
        for waste in self.__waste_list:
            if waste.get_item_id() == waste_serial:
                return waste

    # Se il prodotto esiste già, ne ritorna il seriale. Altrimenti lo crea e ritorna il nuovo seriale
    def create_product(self, data: dict[str, any]) -> str:
        print(f"Nuovo prodotto:{data}")
        new_shoe = ShoeLastVariety(
            data['product_type'], data['gender'], data['shoe_last_type'],
            data['plastic_type'], data['size'], data['processing'],
            data['first_compass_type'], data['second_compass_type'], data['pivot_under_heel'],
            data['shoeing'], data['iron_tip'], data['numbering_antineck'],
            data['numbering_lateral'], data['numbering_heel']
        )
        # Controlla se il prodotto esiste
        for product in self.__products_list:
            print(f"Prodotto:{vars(product)}")
            if product.get_shoe_last_variety().equals(new_shoe):
                # Se il prodotto esiste, ne viene ritornato il seriale
                print("Trovato")
                return product.get_item_id()

        # Se il prodotto non esiste, ne crea uno nuovo
        product_data = dict(
            product_type=data.get("product_type"),
            gender=data.get("gender"),
            shoe_last_type=data.get("shoe_last_type"),
            plastic_type=data.get("plastic_type"),
            size=data.get("size"),
            processing=data.get("processing"),
            first_compass_type=data.get("first_compass_type"),
            second_compass_type=data.get("second_compass_type"),
            pivot_under_heel=data.get("pivot_under_heel"),
            shoeing=data.get("shoeing"),
            iron_tip=data.get("iron_tip"),
            numbering_antineck=data.get("numbering_antineck"),
            numbering_lateral=data.get("numbering_lateral"),
            numbering_heel=data.get("numbering_heel"),
            amount=data.get("amount")
        )

        # Salva il prodotto nel database e ritorna il nuovo seriale
        return self.__storage_network.insert_product(product_data)

    # Se il materiale esiste già, ne ritorna il seriale. Altrimenti lo crea e ritorna il nuovo seriale
    def create_material(self, new_material_data: dict[str, any]) -> str:
        print(f"Nuovo materiale:{new_material_data}")
        # Controlla se il materiale esiste
        for material in self.__materials_list:
            print(f"Materiale:{vars(material)}")
            if (material.get_material_type() == new_material_data.get("material_type")
                    and material.get_description == new_material_data.get("material_description")
                    and material.get_quantity() == new_material_data.get("amount")):
                # Se il materiale esiste, ne viene ritornato il seriale
                print("Trovato")
                return material.get_item_id()

        # Se il prodotto non esiste, ne crea uno nuovo
        material_data = dict(
            material_type=new_material_data.get("material_type"),
            material_description=new_material_data.get("material_description"),
            amount=new_material_data.get("amount")
        )

        # Salva il prodotto nel database e ritorna il nuovo seriale
        return self.__storage_network.insert_material(material_data)

    def get_max_storage(self):
        return self.__storage_network.get_max_storage()

    def sort_list(self, department: str, reverse: bool):
        match department:
            case "product":
                return self.__products_list.sort(key=lambda k: k.get_amount(), reverse=reverse)
            case "material":
                return self.__materials_list.sort(key=lambda k: k.get_amount(), reverse=reverse)
            case "waste":
                return self.__waste_list.sort(key=lambda k: k.get_amount(), reverse=reverse)

    def delete_product_by_id(self, product_id: str):
        self.__storage_network.delete_product_by_id(product_id)

    def delete_material_by_id(self, material_id: str):
        self.__storage_network.delete_material_by_id(material_id)

    def delete_waste_by_id(self, waste_id: str):
        self.__storage_network.delete_waste_by_id(waste_id)

    def update_and_sell_waste(self, waste_id: str, new_quantity: int):
        for waste in self.__waste_list:
            if waste.get_item_id() == waste_id:
                transaction_amount = 0
                if waste.get_plastic_type().value == 1:
                    transaction_amount = new_quantity * 1.0
                elif waste.get_plastic_type() == 2:
                    transaction_amount = new_quantity * 1.5
                else:
                    transaction_amount = new_quantity * 2.0

                CashRegisterRepository().create_transaction(
                    f"Vendità scarti plastica tipo {waste.get_plastic_type().value}",
                    transaction_amount)

                new_quantity = self.get_waste_by_id(waste_id).get_quantity() - new_quantity
                self.__storage_network.update_waste_amount(waste.get_item_id(), new_quantity)
