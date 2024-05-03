from lib.firebaseData import firebase
from lib.model.Product import Product
from lib.repository.StorageRepository import StorageRepository


class ProductListController:

    def __init__(self):
        super().__init__()
        self.__products_repository = StorageRepository()
        self.__database = firebase.database()

    def observe_product_list(self, callback: callable):
        self.__products_repository.observe(callback)

    # Ritorna un ordine in base all'id
    def get_product_by_id(self, product_id: str) -> Product:
        return self.__products_repository.get_product_by_id(product_id)

    # Ritorna la lista di ordini
    def get_products_list(self) -> list[Product]:
        return self.__products_repository.get_products_list()

    # Ritorna la lista di ordini filtrata
    def get_filtered_product_list(self, filters: dict[str, any]) -> list[Product]:
        return self.filter_product_list(self.__products_repository.get_products_list().copy(), filters)

    # Filtra una lista dei prodotti
    @staticmethod
    def filter_product_list(product_list: list[Product], filters: dict[str, any]) -> list[Product]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio degli ordini

        # Parametri di filtro scelti dall'utente
        search_text: str = filters["searchbox"]  # Valore del campo del prodotto sulla base di cui filtrare
        allowed_types: list[str] = []  # Stati del prodotto da mostrare

        # In base ai parametri di filtro, determina se uno stato è ammesso a meno
        def append_types_if_allowed(filter_key: str, state_name: str):
            if filters[filter_key]:
                allowed_types.append(state_name)

        # Eseguo la funzione per tutti gli stati possibili
        append_types_if_allowed("sketches", "Abbozzo")
        append_types_if_allowed("semifinished", "Semi-lavorato")
        append_types_if_allowed("finished", "Forma finita")

        # Numero di campi ammessi
        allowed_types_count: int = len(allowed_types)

        # Se nessuno stato è ammesso, la lista degli ordini da mostrare è quella vuota
        if allowed_types_count:

            # Dato un prodotto, ne ritorna i dettagli
            def product_details(product_: Product) -> str:
                return product_.get_details()

            filter_field = product_details

            # Filtra la lista degli ordini
            for product in reversed(product_list):

                # Se il testo di ricerca è vuoto viene saltato il filtro sul campo
                if search_text:
                    if search_text not in filter_field(product):
                        product_list.remove(product)
                        continue

                # Se tutti gli stati sono ammessi viene saltato il filtro sullo stato
                if allowed_types_count != 3:
                    if product.get_type() not in allowed_types:
                        product_list.remove(product)

        else:
            product_list = []

        return product_list

    # Crea un ordine a partire dai dati della form
    def create_product(self, data: dict[str, any]):

        # Controlla se il prodotto esiste e in caso affermativo ne ritorna anche il seriale
        product_serial = self.__products_repository.create_product(data)

    def get_max_storge(self):
        return self.__products_repository.get_max_storage()

    def get_available_storage(self):
        return self.__products_repository.get_available_storage()

    def get_used_storage(self):
        return self.__products_repository.get_used_storage()

    def sort_products(self, reverse: bool):
        self.__products_repository.sort_products_list(reverse)

