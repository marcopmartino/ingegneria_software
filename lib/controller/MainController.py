from lib.repository.ArticlesRepository import ArticlesRepository
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.repository.MachinesRepository import MachinesRepository
from lib.repository.OrdersRepository import OrdersRepository
from lib.repository.PriceCatalogRepository import PriceCatalogRepository
from lib.repository.Repository import Repository
from lib.repository.UsersRepository import UsersRepository
from lib.utility.ObserverClasses import Observer


class MainController:
    def __init__(self):

        # Inizializzo la mappa delle repository
        self.__repositories: dict[type(Repository), Repository] = dict()

        # Inizializzo la mappa degli osservatori delle repository
        self.__repository_observers: dict[type(Repository), Observer] = dict()

        # Lista delle repository presenti nell'applicazione
        repository_classes = (
            ArticlesRepository,
            CashRegisterRepository,
            MachinesRepository,
            OrdersRepository,
            PriceCatalogRepository,
            UsersRepository
        )

        # Popolo la mappa delle repository
        for repository_class in repository_classes:
            self.__repositories[repository_class] = repository_class()

    def __open_repository_streams(self, repository_classes: list[type(Repository)]):
        for repository_class in repository_classes:
            self.__repositories[repository_class].open_stream()

    # Apro gli stream nel caso di app in uno da un cliente
    def open_customer_streams(self):
        self.__open_repository_streams([
            ArticlesRepository,
            OrdersRepository,
            PriceCatalogRepository,
            UsersRepository
        ])

    # Apro gli stream nel caso di app in uno da un operaio
    def open_worker_streams(self):
        self.__open_repository_streams([
            ArticlesRepository,
            MachinesRepository,
            OrdersRepository,
            PriceCatalogRepository,
            UsersRepository
        ])

    # Apro gli stream nel caso di app in uno da un manager
    def open_manager_streams(self):
        for repository in self.__repositories.values():
            repository.open_stream()

    # Chiudo gli stream, rimuovo gli osservatori e svuoto le repository
    def reset_repositories(self):
        for repository in self.__repositories.values():
            repository.close_stream()
            repository.detachAll()
            repository.clear()

    # Imposta un osservatore per la repository del registro di cassa
    def observe_cash_register(self, callback: callable):
        self.__repositories[CashRegisterRepository].observe(callback)
