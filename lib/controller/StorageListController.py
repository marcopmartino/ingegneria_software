from lib.model.StoredItems import StoredShoeLastVariety, StoredWaste, StoredMaterial
from lib.repository.StorageRepository import StorageRepository


class StorageListController:

    def __init__(self):
        super().__init__()
        self.__storage_repository = StorageRepository()

    def observe_storage_list(self, callback: callable):
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

    # Ritorna la lista dei prodotti filtrata
    def get_filtered_product_list(self, filters: dict[str, any]) -> list[StoredShoeLastVariety]:
        return self.filter_product_list(filters, *self.__storage_repository.get_products_list())

    # Ritorna la lista dei materiali filtrata
    def get_filtered_materials_list(self, filters: dict[str, any]) -> list[StoredMaterial]:
        return self.filter_materials_list(filters, *self.__storage_repository.get_materials_list())

    # Ritorna la lista di scarti filtrata
    def get_filtered_waste_list(self, filters: dict[str, any]) -> list[StoredWaste]:
        return self.filter_waste_list(filters, *self.__storage_repository.get_waste_list())

    # Filtra una lista dei prodotti
    def filter_product_list(self, filters: dict[str, any],
                            *product_list: StoredShoeLastVariety) -> list[StoredShoeLastVariety]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio dei prodotti

        # Parametri di filtro scelti dall'utente
        search_text: str = filters["searchbox"]  # Valore del campo del prodotto sulla base di cui filtrare
        allowed_types: list[str] = []  # Tipi di prodotto da mostrare

        # In base ai parametri di filtro, determina se un tipo è ammesso a meno
        def append_types_if_allowed(filter_key: str, type_name: str):
            if filters[filter_key]:
                allowed_types.append(type_name)

        # Eseguo la funzione per tutti i tipi possibili
        append_types_if_allowed("sketch", "Abbozzo")
        append_types_if_allowed("worked", "Abbozzo sgrossato")
        append_types_if_allowed("finished", "Forma finita")
        append_types_if_allowed("numbered", "Forma numerata")

        # Numero di campi ammessi
        allowed_types_count: int = len(allowed_types)

        filtered_products_list: list[StoredShoeLastVariety] = []

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

                filtered_products_list.append(product)

        return filtered_products_list

    # Filtra una lista dei materiali
    @staticmethod
    def filter_materials_list(filters: dict[str, any], *materials_list: StoredMaterial) -> list[StoredMaterial]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio dei materiali

        # Parametri di filtro scelti dall'utente
        search_text: str = filters["searchbox"]  # Valore del campo del materiale sulla base di cui filtrare
        allowed_types: list[str] = []  # Tipi di materiale da mostrare

        # In base ai parametri di filtro, determina se un tipo è ammesso a meno
        def append_types_if_allowed(filter_key: str, type_name: str):
            if filters[filter_key]:
                allowed_types.append(type_name)

        # Eseguo la funzione per tutti i tipi possibili
        append_types_if_allowed("shoeing", "Parte per ferratura")
        append_types_if_allowed("turning", "Parte per tornitura")
        append_types_if_allowed("compass", "Bussola")
        append_types_if_allowed("other", "Altro")

        # Numero di campi ammessi
        allowed_types_count: int = len(allowed_types)

        filtered_materials_list: list[StoredMaterial] = []

        # Se nessuno stato è ammesso, la lista dei materiali da mostrare è quella vuota
        if allowed_types_count:

            # Dato un materiale ne ritorna i dettagli
            def material_details(product_: StoredMaterial) -> str:
                return product_.get_description

            filter_field = material_details

            # Filtra la lista dei materiali
            for material in materials_list:

                # Se il testo di ricerca è vuoto viene saltato il filtro sul campo
                if search_text:
                    if search_text.lower() not in filter_field(material).lower():
                        continue

                # Se tutti i tipi sono ammessi viene saltato il filtro sul tipo
                if allowed_types_count != 4:
                    if material.get_material_type() not in allowed_types:
                        continue

                filtered_materials_list.append(material)

        return filtered_materials_list

    # Filtra una lista degli scarti
    @staticmethod
    def filter_waste_list(filters: dict[str, any], *waste_list: StoredWaste) -> list[StoredWaste]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio degli scarti

        # Parametri di filtro scelti dall'utente
        # search_text: str = filters["searchbox"] # Valore del campo del prodotto sulla base di cui filtrare
        allowed_plastic: list[str] = []  # Tipi di plastica da mostrare

        # In base ai parametri di filtro, determina se un tipo di plastica è ammesso a meno
        def append_plastic_if_allowed(filter_key: str, plastic_name: str):
            if filters[filter_key]:
                allowed_plastic.append(plastic_name)

        # Eseguo la funzione per tutti gli stati possibili
        append_plastic_if_allowed("plastic1", "1")
        append_plastic_if_allowed("plastic2", "2")
        append_plastic_if_allowed("plastic3", "3")

        allowed_plastic_count: int = len(allowed_plastic)

        filtered_wastes_list: list[StoredWaste] = []

        # Se nessuno stato è ammesso, la lista degli scarti da mostrare è quella vuota
        if allowed_plastic_count:

            # Filtra la lista degli scarti
            for waste in waste_list:

                # Se tutti i tipi di plastica sono ammessi viene saltato il filtro sul tipo di plastica
                if allowed_plastic_count != 3:
                    if str(waste.get_plastic_type()) not in allowed_plastic:
                        if waste in waste_list:
                            continue

                filtered_wastes_list.append(waste)

        return filtered_wastes_list

    def update_waste_quantity(self, waste_id: str, new_quantity: int):
        self.__storage_repository.update_and_sell_waste(waste_id, new_quantity)

    def get_max_storge(self):
        return self.__storage_repository.get_max_storage()


