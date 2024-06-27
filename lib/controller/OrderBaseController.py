from abc import ABC

from lib.model.ShoeLastVariety import ShoeLastVariety, ProductType
from lib.repository.ArticlesRepository import ArticlesRepository
from lib.repository.OrdersRepository import OrdersRepository
from lib.repository.PriceCatalogRepository import PriceCatalogRepository


class OrderBaseController(ABC):
    def __init__(self):
        super().__init__()
        self._orders_repository: OrdersRepository = OrdersRepository()
        self._articles_repository: ArticlesRepository = ArticlesRepository()
        self.__price_catalog_repository = PriceCatalogRepository()

    # Determina la varietà di forma e il prezzo dell'ordine in base ai dati della form
    def get_shoe_last_variety_and_price(self, data: dict[str, any]) -> (float, ShoeLastVariety):
        shoe_last_variety = ShoeLastVariety(
            ProductType.FORMA_NUMERATA, data["gender"], data["type"], data["plastic"], data["size"],
            data["processing"], data["first"], data["second"], data["pivot"], data["shoeing"], data["shoetip"],
            data["antineck"], data["lateral"], data["heel"]
        )

        return shoe_last_variety, self.__price_catalog_repository.calculate_price(shoe_last_variety, data["quantity"])
