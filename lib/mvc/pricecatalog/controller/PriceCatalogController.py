from lib.mvc.pricecatalog.model.PriceCatalog import PriceCatalog


class PriceListController:
    def __init__(self):
        self.price_catalog = PriceCatalog()

    def get_price_catalog(self):
        return self.price_catalog.get()

    def update_price_list(self, data: dict):
        self.price_catalog.update(data)
