from enum import Enum

from lib.model.Article import Article
from lib.model.ShoeLastVariety import ShoeLastVariety, Gender, ShoeLastType, PlasticType, CompassType, Processing, \
    Shoeing
from lib.network.ArticlesNetwork import ArticlesNetwork
from lib.repository.Repository import Repository
from lib.utility.ObserverClasses import Message
from lib.utility.Singleton import RepositoryMeta
from lib.utility.UtilityClasses import DatetimeUtils


class ArticlesRepository(Repository, metaclass=RepositoryMeta):
    class Event(Enum):
        ARTICLES_INITIALIZED = 0
        ARTICLE_CREATED = 1
        ARTICLE_PRODUCED_SHOE_LASTS_UPDATED = 2

    def __init__(self):
        self.__article_list: list[Article] = []
        self.__articles_network: ArticlesNetwork = ArticlesNetwork()
        super().__init__(self.__articles_network.stream)

    def clear(self):
        self.__article_list = []

    # Usato internamente per istanziare e aggiungere un articolo alla lista
    def __instantiate_and_append_article(self, serial: str, data: any) -> Article:
        shoe_last_variety = ShoeLastVariety(
            Gender(data["gender"]), ShoeLastType(data["shoe_last_type"]), PlasticType(data["plastic_type"]),
            data["size"], Processing(data["processing"]), CompassType(data["first_compass_type"]),
            CompassType(data["second_compass_type"]), data["pivot_under_heel"], Shoeing(data["shoeing"]),
            data["iron_tip"], data["numbering_antineck"], data["numbering_lateral"], data["numbering_heel"],
        )

        article = Article(serial, shoe_last_variety, data["creation_date"], data["produced_article_shoe_lasts"])
        self.__article_list.append(article)
        return article

    # Stream handler che aggiorna automaticamente la lista degli articoli
    def _stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorno la lista degli articoli così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        if data is not None:
            path = message["path"]
            match message["event"]:
                case "put":

                    # All'avvio del programma, quando viene caricata l'intera lista di articoli
                    if path == "/":
                        if data is not None:
                            for key, value in data.items():
                                self.__instantiate_and_append_article(key, value)

                        # Notifica gli osservatori che la repository ha concluso l'inizializzazione
                        self.notify(Message(ArticlesRepository.Event.ARTICLES_INITIALIZED, self.__article_list))

                    # Quando viene creato un nuovo articolo
                    else:
                        new_article = self.__instantiate_and_append_article(path.split("/")[1], data)

                        # Notifica gli osservatori che un articolo è stato creato
                        self.notify(Message(ArticlesRepository.Event.ARTICLE_CREATED, new_article))

                # Quando viene aggiornato il numero di paia di forme di un articolo prodotte
                case "patch":

                    # Estrae il seriale dell'articolo dal percorso
                    article_serial: str = path.split("/")[1]

                    # Prende l'articolo corrispondente
                    article = self.get_article_by_id(article_serial)

                    # Aggiorna l'articolo
                    article.set_produced_article_shoe_lasts(data["produced_article_shoe_lasts"])

                    # Prepara il messaggio per notificare gli osservatori della lista degli articoli
                    message = Message(ArticlesRepository.Event.ARTICLE_PRODUCED_SHOE_LASTS_UPDATED)
                    article.notify(message)  # Notifica eventuali osservatori del singolo articolo
                    message.setData(article)
                    self.notify(message)  # Notifica gli osservatori della repository

                case "cancel":
                    pass

    # Ritorna la lista degli articoli
    def get_article_list(self) -> list[Article]:
        return self.__article_list.copy()

    # Ritorna un articolo in base al suo numero
    def get_article_by_id(self, article_serial: str) -> Article:
        for article in self.__article_list:
            if article.get_article_serial() == article_serial:
                return article

    # Aggiorna il numero di paia di forme prodotte
    def update_article_production_counter_by_id(self, article_serial: str, total_produced_shoe_lasts: int):
        self.__articles_network.update_production_counter(
            article_serial, total_produced_shoe_lasts
        )

    # Se l'articolo esiste già, ne ritorna il seriale. Altrimenti lo crea e ritorna il nuovo seriale
    def create_article(self, new_article_data: dict[str, any]) -> str:
        print(f"Nuovo articolo:{new_article_data}")
        # Controlla se l'articolo esiste
        for article in self.__article_list:
            shoe_last_variety = article.get_shoe_last_variety()
            print(f"Articolo:{vars(article)}")
            if (shoe_last_variety.get_gender() == new_article_data.get("gender")
                    and shoe_last_variety.get_size() == new_article_data.get("size")
                    and shoe_last_variety.get_plastic_type() == new_article_data.get("plastic")
                    and shoe_last_variety.get_shoe_last_type() == new_article_data.get("type")
                    and shoe_last_variety.get_first_compass_type() == new_article_data.get("first")
                    and shoe_last_variety.get_second_compass_type() == new_article_data.get("second")
                    and shoe_last_variety.get_processing() == new_article_data.get("processing")
                    and shoe_last_variety.get_shoeing() == new_article_data.get("shoeing")
                    and shoe_last_variety.get_numbering_antineck() == new_article_data.get("antineck")
                    and shoe_last_variety.get_numbering_lateral() == new_article_data.get("lateral")
                    and shoe_last_variety.get_numbering_heel() == new_article_data.get("heel")
                    and shoe_last_variety.get_iron_tip() == new_article_data.get("shoetip")
                    and shoe_last_variety.get_pivot_under_heel() == new_article_data.get("pivot")):
                # Se l'articolo esiste, ne viene ritornato il seriale
                print("Trovato")
                return article.get_article_serial()

        # Se l'articolo non esiste, ne crea uno nuovo
        article_data = dict(
            gender=new_article_data.get("gender").value,
            size=new_article_data.get("size"),
            shoe_last_type=new_article_data.get("type").value,
            plastic_type=new_article_data.get("plastic").value,
            first_compass_type=new_article_data.get("first").value,
            second_compass_type=new_article_data.get("second").value,
            processing=new_article_data.get("processing").value,
            shoeing=new_article_data.get("shoeing").value,
            numbering_antineck=new_article_data.get("antineck"),
            numbering_lateral=new_article_data.get("lateral"),
            numbering_heel=new_article_data.get("heel"),
            iron_tip=new_article_data.get("shoetip"),
            pivot_under_heel=new_article_data.get("pivot"),
            creation_date=DatetimeUtils.current_date(),
            produced_article_shoe_lasts=0
        )

        # Salva l'articolo nel database e ritorna il nuovo seriale
        return self.__articles_network.insert(article_data)
