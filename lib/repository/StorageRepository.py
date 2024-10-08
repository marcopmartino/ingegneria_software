from enum import Enum

from lib.model.Order import Order
from lib.model.ShoeLastVariety import ShoeLastVariety, ProductType, Gender, ShoeLastType, PlasticType, CompassType, \
    Processing, Shoeing
from lib.model.StoredItems import StoredShoeLastVariety, StoredMaterial, StoredWaste, StoredItem, MaterialType, \
    MaterialDescription, AssignedShoeLastVariety
from lib.network.StorageNetwork import StorageNetwork
from lib.repository.Repository import Repository
from lib.utility.ObserverClasses import Message
from lib.utility.Singleton import RepositoryMeta


class StorageRepository(Repository, metaclass=RepositoryMeta):
    class Event(Enum):
        PRODUCTS_INITIALIZED = 0
        PRODUCT_CREATED = 1
        PRODUCT_UPDATED = 2
        PRODUCT_DELETED = 3
        MATERIALS_INITIALIZED = 4
        MATERIAL_UPDATED = 5
        WASTE_INITIALIZED = 6
        WASTE_UPDATED = 7
        RAW_SHOE_LAST_CENTER_PRICE_CATALOG_INITIALIZED = 8
        HARDWARE_STORE_PRICE_CATALOG_INITIALIZED = 9

    def __init__(self):
        # Inizializza le liste di oggetti immagazzinati
        self.__product_list: list[StoredShoeLastVariety] = []
        self.__material_list: list[StoredMaterial] = []
        self.__waste_list: list[StoredWaste] = []

        # Inizializza i listini dei fornitori
        self.__raw_shoe_last_center_price_catalog: dict[str, float] = {}
        self.__hardware_store_price_catalog: dict[str, float] = {}

        self.__storage_network: StorageNetwork = StorageNetwork()
        super().__init__(self.__storage_network.stream)

    def clear(self):
        self.__product_list = []
        self.__material_list = []
        self.__waste_list = []
        self.__raw_shoe_last_center_price_catalog = {}
        self.__hardware_store_price_catalog = {}

    # Usato internamente per istanziare e aggiungere un prodotto alla lista
    def __instantiate_and_append_product(self, serial: str, data: any):
        shoe_last_variety = ShoeLastVariety(
            ProductType(data['product_type']),
            Gender(data["gender"]), ShoeLastType(data["shoe_last_type"]), PlasticType(data["plastic_type"]),
            data.get("size"), Processing(data["processing"]), CompassType(data["first_compass_type"]),
            CompassType(data["second_compass_type"]), data["pivot_under_heel"], Shoeing(data["shoeing"]),
            data["iron_tip"], data["numbering_antineck"], data["numbering_lateral"], data["numbering_heel"]
        )

        order_serial = data.get("order_serial")
        product = StoredShoeLastVariety(serial, data['amount'], shoe_last_variety) if order_serial is None else \
            AssignedShoeLastVariety(serial, data['amount'], shoe_last_variety, order_serial)
        self.__product_list.append(product)
        return product

    # Usato internamente per istanziare e aggiungere un materiale alla lista
    def __instantiate_and_append_material(self, serial: str, data: any):
        material = StoredMaterial(
            serial, data['amount'], MaterialType(data['material_type']),
            MaterialDescription(data['material_description'])
        )
        self.__material_list.append(material)
        return material

    # Usato internamente per istanziare e aggiungere un scarti alla lista
    def __instantiate_and_append_waste(self, serial: str, data: any):
        waste = StoredWaste(
            serial, data['amount'], PlasticType(data['plastic_type'])
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
        match message["event"]:
            case "put":
                # All'avvio del programma, quando viene caricata l'intera lista di prodotti
                if path == "/":
                    if data:
                        # Estraggo gli oggetti immagazzinati
                        products = data.get("products")
                        materials = data.get("materials")
                        waste = data.get("waste")

                        # Inizializza i prodotti
                        if products is not None:
                            for key, value in products.items():
                                # Crea e aggiunge un prodotto alla lista dei prodotti
                                self.__instantiate_and_append_product(key, value)

                            # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                            self.notify(Message(
                                StorageRepository.Event.PRODUCTS_INITIALIZED,
                                self.__product_list
                            ))

                        # Inizializza i materiali
                        if materials is not None:
                            for key, value in materials.items():
                                # Crea e aggiunge un materiale alla lista dei materiali
                                self.__instantiate_and_append_material(key, value)

                            # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                            self.notify(Message(
                                StorageRepository.Event.MATERIALS_INITIALIZED,
                                self.__material_list
                            ))

                        # Inizializza gli scarti
                        if waste is not None:
                            for key, value in waste.items():
                                # Crea e aggiunge uo scarto alla lista degli scarti
                                self.__instantiate_and_append_waste(key, value)

                            # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                            self.notify(Message(
                                StorageRepository.Event.WASTE_INITIALIZED,
                                self.__waste_list
                            ))

                        # Inizializza i prezzi del listino del centro abbozzi
                        self.__raw_shoe_last_center_price_catalog.update(
                            data["raw_shoe_last_center_price_list"])

                        # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                        self.notify(Message(
                            StorageRepository.Event.RAW_SHOE_LAST_CENTER_PRICE_CATALOG_INITIALIZED,
                            self.__raw_shoe_last_center_price_catalog
                        ))

                        # Inizializza i prezzi del listino della ferramenta
                        self.__hardware_store_price_catalog.update(
                            data["hardware_store_price_list"])

                        # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                        self.notify(Message(
                            StorageRepository.Event.HARDWARE_STORE_PRICE_CATALOG_INITIALIZED,
                            self.__hardware_store_price_catalog
                        ))

                # Se il path è diverso allora sto operando sul singolo campo
                else:

                    # Estrae il percorso su cui sta operando
                    path = path.split('/')

                    # Estrae l'id del prodotto del magazzino
                    product_id = path[2]

                    # Controlla di che tipo di prodotto si tratta
                    if path[1] == "products":
                        # Se viene creato un prodotto data non è None
                        if data:

                            # Crea e aggiunge un prodotto alla lista dei prodotti
                            product = self.__instantiate_and_append_product(product_id, data)

                            # Prepara il messaggio per notificare gli osservatori del magazzino
                            message = Message(StorageRepository.Event.PRODUCT_CREATED, product)

                            # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                            self.notify(message)

                        # Se data è None, un prodotto è stato eliminato
                        else:
                            for product in self.__product_list:
                                if product.get_item_id() == product_id:
                                    # Rimuove il prodotto dalla lista
                                    self.__product_list.remove(product)

                                    # Prepara il messaggio per notificare gli osservatori del registro di cassa
                                    message = Message(StorageRepository.Event.PRODUCT_DELETED)
                                    message.setData(product_id)

                                    # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                                    self.notify(message)
                                    break

            # Aggiornamento del magazzino
            case "patch":
                element: StoredItem

                # Estrae il percorso dell'elemento che è stato modificato e il suo id
                path = path.split('/')
                element_type = path[1]
                product_id = path[2]

                print("Updating element" + product_id)
                # Prende l'elemento corrispondente

                if element_type == "products":
                    element = self.get_product_by_id(product_id)
                    message = Message(StorageRepository.Event.PRODUCT_UPDATED)
                elif element_type == "materials":
                    element = self.get_material_by_id(product_id)
                    message = Message(StorageRepository.Event.MATERIAL_UPDATED)
                else:
                    element = self.get_waste_by_id(product_id)
                    message = Message(StorageRepository.Event.WASTE_UPDATED)

                element.set_quantity(data['amount'])
                message.setData(element)

                self.notify(message)

            case "cancel":
                pass

    # Ritorna la lista dei prodotti
    def get_product_list(self) -> list[StoredShoeLastVariety]:
        return self.__product_list

    # Ritorna la lista dei materiali
    def get_material_list(self) -> list[StoredMaterial]:
        return self.__material_list

    # Ritorna la lista degli scarti
    def get_waste_list(self) -> list[StoredWaste]:
        return self.__waste_list

    # Ritorna un prodotto in base al suo id
    def get_product_by_id(self, product_serial: str) -> StoredShoeLastVariety:
        for product in self.__product_list:
            if product.get_item_id() == product_serial:
                return product

    # Ritorna un prodotto assegnato in base al seriale dell'ordine associato
    def get_assigned_product_by_order_id(self, order_serial: str) -> AssignedShoeLastVariety:
        for product in self.__product_list:
            if (isinstance(product, AssignedShoeLastVariety) and
                    product.get_assigned_order_id() == order_serial):
                return product

    # Ritorna un prodotto non assegnato in base alla sua varietà di forma
    def get_unassigned_product_by_shoe_last_variety(self, shoe_last_variety: ShoeLastVariety) -> StoredShoeLastVariety:
        for product in self.__product_list:
            if (product.get_shoe_last_variety().equals(shoe_last_variety)
                    and not isinstance(product, AssignedShoeLastVariety)):
                return product

    # Ritorna un materiale in base al suo id
    def get_material_by_id(self, material_serial: str) -> StoredMaterial:
        for material in self.__material_list:
            if material.get_item_id() == material_serial:
                return material

    # Ritorna un materiale in base alla sua descrizione
    def get_material_by_description(self, material_description: MaterialDescription) -> StoredMaterial:
        for material in self.__material_list:
            if material.get_description() == material_description.value:
                return material

    # Ritorna uno scarto in base al suo id
    def get_waste_by_id(self, waste_serial: str) -> StoredWaste:
        for waste in self.__waste_list:
            if waste.get_item_id() == waste_serial:
                return waste

    # Ritorna uno scarto in base al suo tipo di plastica
    def get_waste_by_plastic_type(self, plastic_type: PlasticType) -> StoredWaste:
        for waste in self.__waste_list:
            if waste.get_plastic_type() == plastic_type:
                return waste

    # Ritorna il listino prezzi del centro abbozzi
    def get_raw_shoe_last_center_price_catalog(self) -> dict[str, float]:
        return self.__raw_shoe_last_center_price_catalog

    # Ritorna il listino prezzi della ferramenta
    def get_hardware_store_price_catalog(self) -> dict[str, float]:
        return self.__hardware_store_price_catalog

    # Crea un prodotto e ne ritorna il nuovo seriale
    def create_unassigned_product(self, shoe_last_variety: ShoeLastVariety, quantity: int = 0) -> str:
        print(f"Nuovo prodotto: {shoe_last_variety.get_description()}")

        # Se il prodotto non esiste, ne crea uno nuovo
        product_data = dict(
            product_type=shoe_last_variety.get_product_type().value,
            gender=shoe_last_variety.get_gender().value,
            shoe_last_type=shoe_last_variety.get_shoe_last_type().value,
            plastic_type=shoe_last_variety.get_plastic_type().value,
            size=shoe_last_variety.get_size(),
            processing=shoe_last_variety.get_processing().value,
            first_compass_type=shoe_last_variety.get_first_compass_type().value,
            second_compass_type=shoe_last_variety.get_second_compass_type().value,
            pivot_under_heel=shoe_last_variety.get_pivot_under_heel(),
            shoeing=shoe_last_variety.get_shoeing().value,
            iron_tip=shoe_last_variety.get_iron_tip(),
            numbering_antineck=shoe_last_variety.get_numbering_antineck(),
            numbering_lateral=shoe_last_variety.get_numbering_lateral(),
            numbering_heel=shoe_last_variety.get_numbering_heel(),
            amount=quantity
        )

        # Salva il prodotto nel database e ritorna il nuovo seriale
        return self.__storage_network.insert_product(product_data)

    # Crea un prodotto, lo assegna a un ordine e ne ritorna il nuovo seriale
    def create_assigned_product(self, shoe_last_variety: ShoeLastVariety, order: Order) -> str:
        print(f"Nuovo prodotto: {shoe_last_variety.get_description()}, ordine {order.get_order_serial()}")

        # Se il prodotto non esiste, ne crea uno nuovo
        product_data = dict(
            product_type=shoe_last_variety.get_product_type().value,
            gender=shoe_last_variety.get_gender().value,
            shoe_last_type=shoe_last_variety.get_shoe_last_type().value,
            plastic_type=shoe_last_variety.get_plastic_type().value,
            size=shoe_last_variety.get_size(),
            processing=shoe_last_variety.get_processing().value,
            first_compass_type=shoe_last_variety.get_first_compass_type().value,
            second_compass_type=shoe_last_variety.get_second_compass_type().value,
            pivot_under_heel=shoe_last_variety.get_pivot_under_heel(),
            shoeing=shoe_last_variety.get_shoeing().value,
            iron_tip=shoe_last_variety.get_iron_tip(),
            numbering_antineck=shoe_last_variety.get_numbering_antineck(),
            numbering_lateral=shoe_last_variety.get_numbering_lateral(),
            numbering_heel=shoe_last_variety.get_numbering_heel(),
            amount=order.get_quantity(),
            order_serial=order.get_order_serial()
        )

        # Salva il prodotto nel database e ritorna il nuovo seriale
        return self.__storage_network.insert_product(product_data)

    # Cerca il prodotto assegnato all'ordine il cui seriale è "order_id" e lo elimina
    def delete_assigned_product(self, order_id: str):
        self.__storage_network.delete_product(self.get_assigned_product_by_order_id(order_id).get_item_id())

    def update_product_quantity(self, product_id: str, quantity: int):
        self.__storage_network.update_product_amount(product_id, quantity)

    def update_material_quantity(self, material_id: str, quantity: int):
        self.__storage_network.update_material_amount(material_id, quantity)

    def update_waste_quantity(self, waste_id: str, quantity: int):
        self.__storage_network.update_waste_amount(waste_id, quantity)
