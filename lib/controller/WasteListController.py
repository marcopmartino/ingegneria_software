from lib.model.StoredItems import StoredWaste
from lib.repository.StorageRepository import StorageRepository


class WasteListController:

    def __init__(self):
        super().__init__()
        self.__waste_repository = StorageRepository()

    def observe_waste_list(self, callback: callable):
        self.__waste_repository.observe(callback)

    # Ritorna uno scarto in base all'id
    def get_waste_by_id(self, waste_id: str) -> StoredWaste:
        return self.__waste_repository.get_waste_by_id(waste_id)

    # Ritorna la lista di scarti
    def get_waste_list(self) -> list[StoredWaste]:
        return self.__waste_repository.get_waste_list()

    # Ritorna la lista di scarti filtrata
    def get_filtered_waste_list(self, filters: dict[str, any]) -> list[StoredWaste]:
        return self.filter_waste_list(filters, *self.__waste_repository.get_waste_list())

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

    def get_max_storge(self):
        return self.__waste_repository.get_max_storage()

    def update_waste_quantity(self, waste_id: str, new_quantity: int):
        self.__waste_repository.update_and_sell_waste(waste_id, new_quantity)
