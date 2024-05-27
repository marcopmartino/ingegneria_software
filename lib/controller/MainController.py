from lib.repository.ArticlesRepository import ArticlesRepository
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.repository.MachinesRepository import MachinesRepository
from lib.repository.OrdersRepository import OrdersRepository
from lib.repository.PriceCatalogRepository import PriceCatalogRepository
from lib.repository.Repository import Repository
from lib.repository.StorageRepository import StorageRepository
from lib.repository.UsersRepository import UsersRepository


class MainController:
    def __init__(self):

        # Inizializzo la mappa delle repository
        self.__repositories: list[Repository] = list()

    # Ritorna una repository
    def get_repository(self, repository_class: type(Repository)) -> Repository:
        if repository_class() in self.__repositories:
            return repository_class()

    # Inizializza le repository usate in caso di cliente autenticato
    def init_customer_repositories(self):
        self.__repositories = [
            ArticlesRepository(),
            OrdersRepository(),
            PriceCatalogRepository(),
            UsersRepository()
        ]

    # Inizializza le repository usate in caso di operaio autenticato
    def init_worker_repositories(self):
        self.__repositories = [
            ArticlesRepository(),
            StorageRepository(),
            MachinesRepository(),
            OrdersRepository(),
            UsersRepository()
        ]

    # Inizializza le repository usate in caso di manager autenticato
    def init_manager_repositories(self):
        self.__repositories = [
            ArticlesRepository(),
            CashRegisterRepository(),
            StorageRepository(),
            MachinesRepository(),
            OrdersRepository(),
            PriceCatalogRepository(),
            UsersRepository()
        ]

    # Chiudo gli stream, rimuovo gli osservatori e svuoto le repository
    def reset_repositories(self):
        for repository in self.__repositories:
            repository.close_stream()
            repository.detachAll()
            repository.clear()

    # Imposta un osservatore per CashRegisterRepository
    def observe_cash_register(self, callback: callable):
        for repository in self.__repositories:
            if isinstance(repository, CashRegisterRepository):
                repository.observe(callback)

    # Apre gli stream
    def open_streams(self):
        for repository in self.__repositories:
            repository.open_stream()
