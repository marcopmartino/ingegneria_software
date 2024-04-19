from lib.repository.PriceCatalogRepository import PriceCatalogRepository


class PriceCatalogController:
    def __init__(self):
        self.__price_catalog_repository = PriceCatalogRepository()

    # Ritorna il listino prezzi
    def get_price_catalog(self):
        return self.__price_catalog_repository.get_price_catalog()

    # Imposta un osservatore per la repository
    def observe_price_catalog(self, callback: callable):
        self.__price_catalog_repository.observe(callback)

    # Aggiorna il listino prezzi
    def update_price_list(self, data: dict):
        self.__price_catalog_repository.update_price_catalog(data)
