from lib.firebaseData import firebase
from lib.model.Product import Product
from lib.repository.StorageRepository import StorageRepository


class WastesListController:

    def __init__(self):
        super().__init__()
        self.__wastes_repository = StorageRepository()
        self.__database = firebase.database()

    def observe_wastes_list(self, callback: callable):
        self.__wastes_repository.observe(callback)

    # Ritorna uno scarto in base all'id
    def get_waste_by_id(self, waste_id: str) -> Product:
        return self.__wastes_repository.get_waste_by_id(waste_id)

    # Ritorna la lista di scarti
    def get_wastes_list(self) -> list[Product]:
        return self.__wastes_repository.get_wastes_list()

    # Ritorna la lista di scarti filtrata
    def get_filtered_wastes_list(self, filters: dict[str, any]) -> list[Product]:
        return self.filter_wastes_list(self.__wastes_repository.get_wastes_list().copy(), filters)

    # Filtra una lista degli scarti
    @staticmethod
    def filter_wastes_list(wastes_list: list[Product], filters: dict[str, any]) -> list[Product]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio degli scarti

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

        # Se nessuno stato è ammesso, la lista degli scarti da mostrare è quella vuota
        if allowed_types_count:

            # Dato un prodotto, ne ritorna i dettagli
            def waste_details(product_: Product) -> str:
                return product_.get_details()

            filter_field = waste_details

            # Filtra la lista degli scarti
            for waste in reversed(wastes_list):

                # Se il testo di ricerca è vuoto viene saltato il filtro sul campo
                if search_text:
                    if search_text not in filter_field(waste):
                        wastes_list.remove(waste)
                        continue

                # Se tutti gli stati sono ammessi viene saltato il filtro sullo stato
                if allowed_types_count != 3:
                    if waste.get_type() not in allowed_types:
                        wastes_list.remove(waste)

        else:
            wastes_list = []

        return wastes_list

    # Crea uno scarto a partire dai dati della form
    def create_waste(self, data: dict[str, any]):
        # Controlla se uno scarto esiste e in caso affermativo ne ritorna anche il seriale
        waste_serial = self.__wastes_repository.create_waste(data)

    def get_max_storge(self):
        return self.__wastes_repository.get_max_storage("waste")

    def get_available_storage(self):
        return self.__wastes_repository.get_available_storage("waste")

    def get_used_storage(self):
        return self.__wastes_repository.get_used_storage("waste")

    def sort_wastes(self, reverse: bool):
        self.__wastes_repository.sort_list("waste", reverse)

