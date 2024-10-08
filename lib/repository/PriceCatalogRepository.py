from enum import Enum

from lib.model.ShoeLastVariety import Gender, ShoeLastType, PlasticType, CompassType, Processing, Shoeing, \
    ShoeLastVariety
from lib.network.PriceCatalogNetwork import PriceCatalogNetwork
from lib.repository.Repository import Repository
from lib.utility.ObserverClasses import Message
from lib.utility.Singleton import RepositoryMeta


class PriceCatalogRepository(Repository, metaclass=RepositoryMeta):

    class Event(Enum):
        PRICE_CATALOG_INITIALIZED = 0
        PRICE_UPDATED = 1

    def __init__(self):
        self.__price_catalog: dict[str, float] = {}  # Inizializzo il model
        self.__price_catalog_network: PriceCatalogNetwork = PriceCatalogNetwork()
        super().__init__(self.__price_catalog_network.stream)

    def clear(self):
        self.__price_catalog = {}

    # Stream handler che aggiorna automaticamente il listino
    def _stream_handler(self, message):

        # Aggiorna i prezzi del listino così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        event: str = message["event"]
        data: dict = message["data"]
        match event:
            # All'apertura dello Stream, quando viene caricato l'intero listino
            case "put":
                # Aggiorna il listino prezzi
                self.__price_catalog.update(data)

                # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                self.notify(Message(PriceCatalogRepository.Event.PRICE_CATALOG_INITIALIZED, self.__price_catalog))

            # Modifica di un importo del listino
            case "patch":
                # Aggiorna il listino prezzi
                self.__price_catalog.update(data)

                # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                self.notify(Message(PriceCatalogRepository.Event.PRICE_UPDATED, data))

            # Se per qualche motivo il collegamento fallisce
            case "cancel":
                pass

    # Ritorna il listino prezzi
    def get_price_catalog(self) -> dict[str, float]:
        return self.__price_catalog

    # Aggiorna il listino prezzi
    def update_price_catalog(self, data: dict):
        self.__price_catalog_network.update(data)

    # Calcola il prezzo di un certo numero di paia con determinate caratteristiche in base agli attuali prezzi di
    # listino
    def calculate_price(self, shoe_last_variety: ShoeLastVariety, quantity: int = 1):

        # Inizializza alcune variabili
        price_list = self.__price_catalog
        article_price: float = 0.00

        gender = shoe_last_variety.get_gender()
        plastic_type = shoe_last_variety.get_plastic_type()
        shoe_last_type = shoe_last_variety.get_shoe_last_type()
        processing = shoe_last_variety.get_processing()
        shoeing = shoe_last_variety.get_shoeing()

        # Prezzo base
        article_price += price_list[f"standard_tipo{str(plastic_type.value)}_{gender.value}_{shoe_last_type.value}"]

        # Lavorazione
        if processing != Processing.NESSUNA:
            article_price += price_list[f"lavorazione_{processing.value}_{gender.value}_{shoe_last_type.value}"]

        # Ferratura
        if shoeing != Shoeing.NESSUNA:
            article_price += price_list[f"ferratura_{shoeing.value}_{gender.value}_{shoe_last_type.value}"]

        # Prima bussola rinforzata
        if shoe_last_variety.get_first_compass_type() == CompassType.RINFORZATA:
            article_price += price_list["bussola_prima_rinforzata"]

        # Seconda bussola
        if shoe_last_variety.get_second_compass_type() != CompassType.NESSUNA:
            article_price += price_list[f"bussola_seconda_{shoe_last_variety.get_second_compass_type().value}"]

        # Segni e linee
        if shoe_last_variety.get_numbering_antineck():
            article_price += price_list[f"numeratura_anticollo"]

        if shoe_last_variety.get_numbering_lateral():
            article_price += price_list[f"numeratura_laterali"]

        if shoe_last_variety.get_numbering_heel():
            article_price += price_list[f"numeratura_tallone"]

        # Accessori
        if shoe_last_variety.get_iron_tip():
            article_price += price_list["punta_ferrata"]

        if shoe_last_variety.get_pivot_under_heel():
            article_price += price_list["perno_sotto_tallone"]

        return article_price * quantity
