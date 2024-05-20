from lib.firebaseData import Firebase
from lib.model.Product import Product
from lib.repository.StorageRepository import StorageRepository


class MaterialsListController:

    def __init__(self):
        super().__init__()
        self.__materials_repository = StorageRepository()

    def observe_materials_list(self, callback: callable):
        self.__materials_repository.observe(callback)

    # Ritorna un materiale in base all'id
    def get_material_by_id(self, material_id: str) -> Product:
        return self.__materials_repository.get_material_by_id(material_id)

    # Ritorna la lista dei materiali
    def get_materials_list(self) -> list[Product]:
        return self.__materials_repository.get_materials_list()

    # Ritorna la lista dei materiali filtrata
    def get_filtered_materials_list(self, filters: dict[str, any]) -> list[Product]:
        return self.filter_materials_list(self.__materials_repository.get_materials_list().copy(), filters)

    # Filtra una lista dei materiali
    @staticmethod
    def filter_materials_list(materials_list: list[Product], filters: dict[str, any]) -> list[Product]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio dei materiali

        # Parametri di filtro scelti dall'utente
        search_text: str = filters["searchbox"]  # Valore del campo del materiale sulla base di cui filtrare
        allowed_types: list[str] = []  # Tipi di materiale da mostrare

        # In base ai parametri di filtro, determina se un tipo è ammesso a meno
        def append_types_if_allowed(filter_key: str, type_name: str):
            if filters[filter_key]:
                allowed_types.append(type_name)

        # Eseguo la funzione per tutti i tipi possibili
        append_types_if_allowed("compass", "Bussola")
        append_types_if_allowed("ironparts", "Parti per ferratura")
        append_types_if_allowed("other", "Altro")

        # Numero di campi ammessi
        allowed_types_count: int = len(allowed_types)

        filtered_materials_list: list[Product] = []

        # Se nessuno stato è ammesso, la lista dei materiali da mostrare è quella vuota
        if allowed_types_count:

            # Dato un materiale ne ritorna i dettagli
            def material_details(product_: Product) -> str:
                return product_.get_details()

            filter_field = material_details

            # Filtra la lista dei materiali
            for material in materials_list:

                # Se il testo di ricerca è vuoto viene saltato il filtro sul campo
                if search_text:
                    if search_text.lower() not in filter_field(material).lower():
                        continue

                # Se tutti i tipi sono ammessi viene saltato il filtro sul tipo
                if allowed_types_count != 3:
                    if material.get_type() not in allowed_types:
                        continue

                filtered_materials_list.append(material)

        return filtered_materials_list

    # Crea un materiale a partire dai dati della form
    def create_material(self, data: dict[str, any]):
        # Controlla se il materiale esiste e in caso affermativo ne ritorna anche il seriale
        material_serial = self.__materials_repository.create_material(data)

    def get_max_storge(self):
        return self.__materials_repository.get_max_storage("material")

    def get_available_storage(self):
        return self.__materials_repository.get_available_storage("material")

    def get_used_storage(self):
        return self.__materials_repository.get_used_storage("material")

    def sort_materials(self, reverse: bool):
        self.__materials_repository.sort_list("material", reverse)

