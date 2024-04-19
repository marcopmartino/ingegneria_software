from abc import ABC

from lib.repository.PriceCatalogRepository import PriceCatalogRepository


class OrderFormController(ABC):
    def __init__(self):
        super().__init__()
        self.__price_catalog_repository = PriceCatalogRepository()

    # Calcola il prezzo dell'ordine in base ai dati della form
    def calculate_order_price(self, data: dict[str, any]) -> float:
        return self.__price_catalog_repository.calculate_price(
            data["gender"], data["type"], data["plastic"], data["first"], data["second"], data["processing"],
            data["shoeing"], data["antineck"], data["lateral"], data["heel"], data["shoetip"], data["pivot"],
            data["quantity"]
        )
