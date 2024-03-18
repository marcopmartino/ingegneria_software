from lib.mvc.pricecatalog.model.PriceCatalog import PriceCatalog


class PriceListController:
    def __init__(self):
        self.price_list = PriceCatalog()

    def update_price_list(self, data: dict):
        self.price_list.update(data)
