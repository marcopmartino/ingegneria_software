from lib.repository.ArticlesRepository import ArticlesRepository
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.repository.MachinesRepository import MachinesRepository
from lib.repository.OrdersRepository import OrdersRepository
from lib.repository.PriceCatalogRepository import PriceCatalogRepository
from lib.repository.Repository import Repository
from lib.repository.UsersRepository import UsersRepository


class MainController:
    def __init__(self):

        # Inizializzo la mappa delle repository
        self.__repositories: dict[type(Repository), Repository] = dict()

        # Lista delle repository presenti nell'applicazione
        repository_classes = [
            ArticlesRepository,
            CashRegisterRepository,
            MachinesRepository,
            OrdersRepository,
            PriceCatalogRepository,
            UsersRepository
        ]

        # Popolo la mappa delle repository
        for repository_class in repository_classes:
            self.__repositories[repository_class] = repository_class()

    # Apro tutti gli stream
    def open_streams(self):
        for repository in self.__repositories.values():
            repository.open_stream()

    # Chiudo tutti gli stream e rimuovo tutti gli osservatori dalle repository
    def close_streams(self):
        for repository in self.__repositories.values():
            repository.close_stream()
            repository.detachAll()

    # Imposta un osservatore per la repository del registro di cassa
    def observe_cash_register(self, callback: callable):
        self.__repositories[CashRegisterRepository].observe(callback)
