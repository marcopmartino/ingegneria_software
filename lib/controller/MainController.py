from lib.repository.ArticlesRepository import ArticlesRepository
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.repository.MachinesRepository import MachinesRepository
from lib.repository.OrdersRepository import OrdersRepository
from lib.repository.PriceCatalogRepository import PriceCatalogRepository
from lib.repository.Repository import Repository
from lib.repository.UsersRepository import UsersRepository


class MainController:
    def __init__(self):
        self.__repositories: list[Repository] = [
            ArticlesRepository(),
            CashRegisterRepository(),
            MachinesRepository(),
            OrdersRepository(),
            PriceCatalogRepository(),
            UsersRepository()
        ]

    def open_streams(self):
        for repository in self.__repositories:
            repository.open_stream()

    def close_streams(self):
        for repository in self.__repositories:
            repository.close_stream()
            repository.detachAll()
