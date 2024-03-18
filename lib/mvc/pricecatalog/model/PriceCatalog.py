from lib.utility.ObserverClasses import Observable
from lib.utility.Singleton import singleton
from lib.network.PriceCatalogNetwork import PriceCatalogNetwork


@singleton
class PriceCatalog(Observable):

    def __init__(self):
        super().__init__()
        self.__price_catalog: dict[str, float] = {}  # Inizializzo
        PriceCatalogNetwork.stream(self.__stream_handler)

    # Stream handler che aggiorna automaticamente il listino
    def __stream_handler(self, message):

        # Aggiorno i prezzi del listino così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        self.__price_catalog.update(message["data"])

        # Notifico gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
        message["notifier"] = "PriceList"
        self.notify(message)

        for key in message.keys():
            print(f"{key}: {message[key]}")

    # Ritorna il listino prezzi
    def get(self) -> dict[str, float]:
        return self.__price_catalog

    # Aggiorna il listino prezzi
    @staticmethod
    def update(data: dict):
        PriceCatalogNetwork.update(data)

    # Converte il prezzo in una stringa con due cifre nella parte decimale
    @staticmethod
    def price_format(value: float) -> str:
        return f"{value:.2f}"
