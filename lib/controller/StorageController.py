from lib.model.ShoeLastVariety import PlasticType, ProductType, ShoeLastVariety
from lib.model.StoredItems import StoredShoeLastVariety, StoredWaste, StoredMaterial, MaterialType, MaterialDescription
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.repository.StorageRepository import StorageRepository


class StorageController:

    def __init__(self):
        super().__init__()
        self.__storage_repository = StorageRepository()
        self.__cash_register_repository = CashRegisterRepository()

    def observe_storage(self, callback: callable):
        self.__storage_repository.observe(callback)

    # Ritorna un prodotto in base all'id
    def get_product_by_id(self, product_id: str) -> StoredShoeLastVariety:
        return self.__storage_repository.get_product_by_id(product_id)

    # Ritorna un materiale in base all'id
    def get_material_by_id(self, material_id: str) -> StoredMaterial:
        return self.__storage_repository.get_material_by_id(material_id)

    # Ritorna uno scarto in base all'id
    def get_waste_by_id(self, waste_id: str) -> StoredWaste:
        return self.__storage_repository.get_waste_by_id(waste_id)

    # Ritorna uno scarto in base al tipo di plastica
    def get_waste_by_plastic_type(self, plastic_type: PlasticType) -> StoredWaste:
        return self.__storage_repository.get_waste_by_plastic_type(plastic_type)

    # Ritorna il totale di prodotti immagazzinati
    def get_total_stored_products_quantity(self) -> int:
        total = 0

        for product in self.__storage_repository.get_product_list():
            total += product.get_quantity()

        return total

    # Ritorna il totale di prodotti immagazzinati
    def get_total_stored_waste_quantity(self) -> int:
        total = 0

        for waste in self.__storage_repository.get_waste_list():
            total += waste.get_quantity()

        return total

    # Ritorna la lista dei prodotti filtrata
    def get_product_list(self, filters: dict[str, any]) -> list[StoredShoeLastVariety]:
        return self.filter_product_list(filters, *self.__storage_repository.get_product_list())

    # Ritorna la lista dei materiali filtrata
    def get_material_list(self, filters: dict[str, any]) -> list[StoredMaterial]:
        return self.filter_material_list(filters, *self.__storage_repository.get_material_list())

    # Ritorna la lista di scarti filtrata
    def get_waste_list(self, filters: dict[str, any]) -> list[StoredWaste]:
        return self.filter_waste_list(filters, *self.__storage_repository.get_waste_list())

    # Filtra una lista dei prodotti
    # noinspection PyMethodMayBeStatic
    def filter_product_list(self, filters: dict[str, any],
                            *product_list: StoredShoeLastVariety) -> list[StoredShoeLastVariety]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio dei prodotti

        # Parametri di filtro scelti dall'utente
        search_text: str = filters["searchbox"]  # Valore del campo del prodotto sulla base di cui filtrare
        allowed_types: list[ProductType] = []  # Tipi di prodotto da mostrare

        # In base ai parametri di filtro, determina se un tipo è ammesso a meno
        def append_types_if_allowed(filter_key: str, product_type: ProductType):
            if filters[filter_key]:
                allowed_types.append(product_type)

        # Eseguo la funzione per tutti i tipi possibili
        append_types_if_allowed("sketch", ProductType.ABBOZZO)
        append_types_if_allowed("worked", ProductType.ABBOZZO_SGROSSATO)
        append_types_if_allowed("finished", ProductType.FORMA_FINITA)
        append_types_if_allowed("numbered", ProductType.FORMA_NUMERATA)

        # Numero di campi ammessi
        allowed_types_count: int = len(allowed_types)

        filtered_product_list: list[StoredShoeLastVariety] = []

        # Se nessuno stato è ammesso, la lista dei prodotti da mostrare è quella vuota
        if allowed_types_count:

            # Dato un prodotto, ne ritorna i dettagli
            def product_details(product_: StoredShoeLastVariety) -> str:
                return product_.get_description()

            filter_field = product_details

            # Filtra la lista dei prodotti
            for product in product_list:

                # Se il testo di ricerca è vuoto viene saltato il filtro sul campo
                if search_text:
                    if search_text.lower() not in filter_field(product).lower():
                        continue

                # Se tutti i tipi sono ammessi viene saltato il filtro sul tipo
                if allowed_types_count != 4:
                    if product.get_shoe_last_variety().get_product_type() not in allowed_types:
                        continue

                filtered_product_list.append(product)

        return filtered_product_list

    # Filtra una lista dei materiali
    # noinspection PyMethodMayBeStatic
    def filter_material_list(self, filters: dict[str, any], *material_list: StoredMaterial) -> list[StoredMaterial]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio dei materiali

        # Parametri di filtro scelti dall'utente
        search_text: str = filters["searchbox"]  # Valore del campo del materiale sulla base di cui filtrare
        allowed_types: list[MaterialType] = []  # Tipi di materiale da mostrare

        # In base ai parametri di filtro, determina se un tipo è ammesso a meno
        def append_types_if_allowed(filter_key: str, material_type: MaterialType):
            if filters[filter_key]:
                allowed_types.append(material_type)

        # Eseguo la funzione per tutti i tipi possibili
        append_types_if_allowed("shoeing", MaterialType.PARTE_PER_FERRATURA)
        append_types_if_allowed("turning", MaterialType.PARTE_PER_TORNITURA)
        append_types_if_allowed("compass", MaterialType.BUSSOLA)
        append_types_if_allowed("other", MaterialType.ALTRO)

        # Numero di campi ammessi
        allowed_types_count: int = len(allowed_types)

        filtered_material_list: list[StoredMaterial] = []

        # Se nessuno stato è ammesso, la lista dei materiali da mostrare è quella vuota
        if allowed_types_count:

            # Dato un materiale ne ritorna i dettagli
            def material_details(material_: StoredMaterial) -> str:
                return material_.get_description()

            filter_field = material_details

            # Filtra la lista dei materiali
            for material in material_list:

                # Se il testo di ricerca è vuoto viene saltato il filtro sul campo
                if search_text:
                    if search_text.lower() not in filter_field(material).lower():
                        continue

                # Se tutti i tipi sono ammessi viene saltato il filtro sul tipo
                if allowed_types_count != 4:
                    if material.get_material_type() not in allowed_types:
                        continue

                filtered_material_list.append(material)

        return filtered_material_list

    # Filtra una lista degli scarti
    # noinspection PyMethodMayBeStatic
    def filter_waste_list(self, filters: dict[str, any], *waste_list: StoredWaste) -> list[StoredWaste]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio degli scarti

        # Parametri di filtro scelti dall'utente
        # search_text: str = filters["searchbox"] # Valore del campo del prodotto sulla base di cui filtrare
        allowed_plastic: list[PlasticType] = []  # Tipi di plastica da mostrare

        # In base ai parametri di filtro, determina se un tipo di plastica è ammesso a meno
        def append_plastic_if_allowed(filter_key: str, plastic_type: PlasticType):
            if filters[filter_key]:
                allowed_plastic.append(plastic_type)

        # Eseguo la funzione per tutti gli stati possibili
        append_plastic_if_allowed("plastic1", PlasticType.TIPO_1_DISCRETA)
        append_plastic_if_allowed("plastic2", PlasticType.TIPO_2_BUONA)
        append_plastic_if_allowed("plastic3", PlasticType.TIPO_3_OTTIMA)

        allowed_plastic_count: int = len(allowed_plastic)

        filtered_wastes_list: list[StoredWaste] = []

        # Se nessuno stato è ammesso, la lista degli scarti da mostrare è quella vuota
        if allowed_plastic_count:

            # Filtra la lista degli scarti
            for waste in waste_list:

                # Se tutti i tipi di plastica sono ammessi viene saltato il filtro sul tipo di plastica
                if allowed_plastic_count != 3:
                    if waste.get_plastic_type() not in allowed_plastic:
                        continue

                filtered_wastes_list.append(waste)

        return filtered_wastes_list

    # Ritorna il listino prezzi del centro abbozzi
    def get_raw_shoe_last_center_price_catalog(self) -> dict[str, float]:
        return self.__storage_repository.get_raw_shoe_last_center_price_catalog()

    # Ritorna il listino prezzi della ferramenta
    def get_hardware_store_price_catalog(self) -> dict[str, float]:
        return self.__storage_repository.get_hardware_store_price_catalog()

    def update_product_quantity(self, product_id: str, new_quantity: int):
        self.__storage_repository.update_product_quantity(product_id, new_quantity)

    def update_material_quantity(self, material_id: str, new_quantity: int):
        self.__storage_repository.update_material_quantity(material_id, new_quantity)

    def update_waste_quantity(self, waste_id: str, new_quantity: int):
        self.__storage_repository.update_waste_quantity(waste_id, new_quantity)

    def purchase_product(self, shoe_last_variety: ShoeLastVariety, purchased_quantity: int,
                         transaction_description: str, transaction_amount: float):

        # Crea una nuova transazione per registrare l'acquisto
        self.__cash_register_repository.create_transaction(transaction_description, transaction_amount)

        # Cerca il prodotto tra quelli presenti in magazzino
        stored_shoe_last_variety = self.__storage_repository.get_product_by_shoe_last_variety(shoe_last_variety)

        # Se il prodotto non è presente in magazzino, inserisce il prodotto con la quantità acquistata
        if stored_shoe_last_variety is None:
            self.__storage_repository.create_product(shoe_last_variety, purchased_quantity)

        # Altrimenti aggiorna la quantità immagazzinata del prodotto
        else:
            new_quantity = stored_shoe_last_variety.get_quantity() + purchased_quantity
            self.__storage_repository.update_product_quantity(stored_shoe_last_variety.get_item_id(), new_quantity)

    def purchase_material(self, material_description: MaterialDescription, purchased_quantity: int,
                          transaction_description: str, transaction_amount: float):

        # Crea una nuova transazione per registrare l'acquisto
        self.__cash_register_repository.create_transaction(transaction_description, transaction_amount)

        # Cerca il materiale tra quelli presenti in magazzino
        stored_material = self.__storage_repository.get_material_by_description(material_description)

        # Altrimenti aggiorna la quantità immagazzinata del materiale
        new_quantity = stored_material.get_quantity() + purchased_quantity
        self.__storage_repository.update_material_quantity(stored_material.get_item_id(), new_quantity)

    def sell_waste(self, stored_waste: StoredWaste, sold_quantity: int,
                   transaction_description: str, transaction_amount: float):

        # Crea una nuova transazione per registrare l'acquisto
        self.__cash_register_repository.create_transaction(transaction_description, transaction_amount)

        # Aggiorna la quantità immagazzinata di scarti
        new_quantity = stored_waste.get_quantity() - sold_quantity
        self.__storage_repository.update_waste_quantity(stored_waste.get_item_id(), new_quantity)
