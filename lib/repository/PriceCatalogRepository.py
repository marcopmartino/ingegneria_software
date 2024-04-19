from lib.utility.ObserverClasses import Observable
from lib.utility.Singleton import ObservableSingleton
from lib.network.PriceCatalogNetwork import PriceCatalogNetwork


class PriceCatalogRepository(Observable, metaclass=ObservableSingleton):

    def __init__(self):
        super().__init__()
        self.__price_catalog: dict[str, float] = {}  # Inizializzo
        self.__price_catalog_network: PriceCatalogNetwork = PriceCatalogNetwork()
        self.__price_catalog_network.stream(self.__stream_handler)

    # Stream handler che aggiorna automaticamente il listino
    def __stream_handler(self, message):

        # Aggiorna i prezzi del listino così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        event: str = message["event"]
        data: dict = message["data"]
        match event:
            # Durante l'inizializzazione (put) e ad ogni modifica di un importo del listino (patch)
            case "put" | "patch":
                # Aggiorna il listino prezzi
                self.__price_catalog.update(data)

                # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                self.notify(message)
            # Se per qualche motivo il collegamento fallisce
            case "cancel":
                pass
                ''' Da gestire in qualche modo '''

        '''for key in message.keys():
            print(f"{key}: {message[key]}")'''

    # Ritorna il listino prezzi
    def get_price_catalog(self) -> dict[str, float]:
        return self.__price_catalog

    # Aggiorna il listino prezzi
    def update_price_catalog(self, data: dict):
        self.__price_catalog_network.update(data)

    # Calcola il prezzo di un certo numero di paia con determinate caratteristiche in base agli attuali prezzi di
    # listino
    def calculate_price(self, gender: str, shoe_last_type: str, plastic_type: int,
                        reinforced_compass: bool, second_compass_type: str, processing: str,
                        shoeing: str, numbering_antineck: bool, numbering_lateral: bool, numbering_heel: bool,
                        iron_tip: bool, pivot_under_heel: bool, quantity: int = 1):

        price_list = self.__price_catalog
        article_price: float = 0.00

        # Prezzo base
        article_price += price_list[f"standard_tipo{str(plastic_type)}_{gender}_{shoe_last_type}"]

        # Lavorazione
        if processing != "nessuna":
            article_price += price_list[f"lavorazione_{processing}_{gender}_{shoe_last_type}"]

        # Ferratura
        if shoeing != "nessuna":
            article_price += price_list[f"ferratura_{shoeing}_{gender}_{shoe_last_type}"]

        # Prima bussola rinforzata
        if reinforced_compass:
            article_price += price_list["bussola_prima_rinforzata"]

        # Seconda bussola
        if second_compass_type != "nessuna":
            article_price += price_list[f"bussola_seconda_{second_compass_type}"]

        # Segni e linee
        if numbering_antineck:
            article_price += price_list[f"numeratura_anticollo"]

        if numbering_lateral:
            article_price += price_list[f"numeratura_laterali"]

        if numbering_heel:
            article_price += price_list[f"numeratura_tallone"]

        # Accessori
        if iron_tip:
            article_price += price_list["punta_ferrata"]

        if pivot_under_heel:
            article_price += price_list["perno_sotto_tallone"]

        return article_price * quantity
