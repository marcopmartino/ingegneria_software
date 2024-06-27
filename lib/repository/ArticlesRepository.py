from enum import Enum

from lib.model.Article import Article
from lib.model.ShoeLastVariety import ShoeLastVariety, Gender, ShoeLastType, PlasticType, CompassType, Processing, \
    Shoeing, ProductType
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
            ProductType.FORMA_NUMERATA,
            Gender(data["gender"]), ShoeLastType(data["shoe_last_type"]), PlasticType(data["plastic_type"]),
            data["size"], Processing(data["processing"]), CompassType(data["first_compass_type"]),
            CompassType(data["second_compass_type"]), data["pivot_under_heel"], Shoeing(data["shoeing"]),
            data["iron_tip"], data["numbering_antineck"], data["numbering_lateral"], data["numbering_heel"],
        )

        article = Article(serial, shoe_last_variety, DatetimeUtils.format_date(data["creation_date"]),
                          data["produced_article_shoe_lasts"])
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

    # Ritorna un articolo in base alla sua varietà di forma
    def get_article_by_shoe_last_variety(self, shoe_last_variety: ShoeLastVariety) -> Article:
        for article in self.__article_list:
            if article.get_shoe_last_variety().equals(shoe_last_variety):
                return article

    # Aggiorna il numero di paia di forme prodotte
    def update_article_production_counter_by_id(self, article_serial: str, total_produced_shoe_lasts: int):
        self.__articles_network.update_production_counter(
            article_serial, total_produced_shoe_lasts
        )

    # Crea un articolo e ritorna il nuovo seriale
    def create_article(self, shoe_last_variety: ShoeLastVariety) -> str:
        # Prepara i dati del nuovo articolo
        article_data = dict(
            gender=shoe_last_variety.get_gender().value,
            size=shoe_last_variety.get_size(),
            shoe_last_type=shoe_last_variety.get_shoe_last_type().value,
            plastic_type=shoe_last_variety.get_plastic_type().value,
            first_compass_type=shoe_last_variety.get_first_compass_type().value,
            second_compass_type=shoe_last_variety.get_second_compass_type().value,
            processing=shoe_last_variety.get_processing().value,
            shoeing=shoe_last_variety.get_shoeing().value,
            numbering_antineck=shoe_last_variety.get_numbering_antineck(),
            numbering_lateral=shoe_last_variety.get_numbering_lateral(),
            numbering_heel=shoe_last_variety.get_numbering_heel(),
            iron_tip=shoe_last_variety.get_iron_tip(),
            pivot_under_heel=shoe_last_variety.get_pivot_under_heel(),
            creation_date=DatetimeUtils.current_date(),
            produced_article_shoe_lasts=0
        )

        # Salva l'articolo nel database e ritorna il nuovo seriale
        return self.__articles_network.insert(article_data)
