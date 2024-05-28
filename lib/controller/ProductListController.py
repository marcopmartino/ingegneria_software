from lib.model.StoredItems import StoredShoeLastVariety
from lib.repository.StorageRepository import StorageRepository


class ProductListController:

    def __init__(self):
        super().__init__()
        self.__products_repository = StorageRepository()

    def observe_product_list(self, callback: callable):
        self.__products_repository.observe(callback)

    # Ritorna un ordine in base all'id
    def get_product_by_id(self, product_id: str) -> StoredShoeLastVariety:
        return self.__products_repository.get_product_by_id(product_id)

    # Ritorna la lista dei prodotti
    def get_products_list(self) -> list[StoredShoeLastVariety]:
        return self.__products_repository.get_products_list()

    # Ritorna la lista dei prodotti filtrata
    def get_filtered_product_list(self, filters: dict[str, any]) -> list[StoredShoeLastVariety]:
        return self.filter_product_list(filters, *self.__products_repository.get_products_list())

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

    # Crea un ordine a partire dai dati della form
    def create_product(self, data: dict[str, any]):

        # Controlla se il prodotto esiste e in caso affermativo ne ritorna anche il seriale
        product_serial = self.__products_repository.create_product(data)

    def get_max_storge(self):
        return self.__products_repository.get_max_storage()

    def sort_products(self, reverse: bool):
        self.__products_repository.sort_list("product", reverse)

