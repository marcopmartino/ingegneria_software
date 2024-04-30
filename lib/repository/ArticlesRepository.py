from lib.model.Article import Article
from lib.network.ArticleNetwork import ArticleNetwork
from lib.utility.ObserverClasses import Observable
from lib.utility.Singleton import ObservableSingleton
from lib.utility.UtilityClasses import DatetimeUtils


class ArticlesRepository(Observable, metaclass=ObservableSingleton):

    def __init__(self):
        super().__init__()
        self.__article_list: list[Article] = []
        self.__article_newtork: ArticleNetwork = ArticleNetwork()
        self.__article_newtork.stream(self.__stream_handler)

    # Usato internamente per istanziare e aggiungere un articolo alla lista
    def __instantiate_and_append_article(self, serial: str, data: any):
        self.__article_list.append(Article(
            serial, data["gender"], data["size"], data["shoe_last_type"], data["plastic_type"],
            data["reinforced_compass"], data["second_compass_type"], data["processing"], data["shoeing"],
            data["numbering_antineck"], data["numbering_lateral"], data["numbering_heel"], data["iron_tip"],
            data["pivot_under_heel"], data["creation_date"], data["produced_article_shoe_lasts"]
        ))

    # Stream handler che aggiorna automaticamente la lista degli articoli
    def __stream_handler(self, message):
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
                        for key, value in data.items():
                            self.__instantiate_and_append_article(key, value)

                    # Quando viene creato un nuovo articolo
                    else:
                        self.__instantiate_and_append_article(path.split("/")[1], data)
                case "patch":
                    pass
                case "cancel":
                    pass

        # Notifico gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
        self.notify(message)

    # Ritorna la lista degli articoli
    def get_article_list(self) -> list[Article]:
        return self.__article_list.copy()

    # Ritorna un articolo in base al suo numero
    def get_article_by_id(self, article_serial: str) -> Article:
        for article in self.__article_list:
            if article.get_article_serial() == article_serial:
                return article

    # Se l'articolo esiste già, ne ritorna il seriale. Altrimenti lo crea e ritorna il nuovo seriale
    def create_article(self, new_article_data: dict[str, any]) -> str:
        print(f"Nuovo articolo:{new_article_data}")
        # Controlla se l'articolo esiste
        for article in self.__article_list:
            print(f"Articolo:{vars(article)}")
            if (article.get_gender() == new_article_data.get("gender")
                    and article.get_size() == new_article_data.get("size")
                    and article.get_plastic_type() == new_article_data.get("plastic")
                    and article.get_shoe_last_type() == new_article_data.get("type")
                    and article.get_reinforced_compass() == new_article_data.get("first")
                    and article.get_second_compass_type() == new_article_data.get("second")
                    and article.get_processing() == new_article_data.get("processing")
                    and article.get_shoeing() == new_article_data.get("shoeing")
                    and article.get_numbering_antineck() == new_article_data.get("antineck")
                    and article.get_numbering_lateral() == new_article_data.get("lateral")
                    and article.get_numbering_heel() == new_article_data.get("heel")
                    and article.get_iron_tip() == new_article_data.get("shoetip")
                    and article.get_pivot_under_heel() == new_article_data.get("pivot")):
                # Se l'articolo esiste, ne viene ritornato il seriale
                print("Trovato")
                return article.get_article_serial()

        # Se l'articolo non esiste, ne crea uno nuovo
        article_data = dict(
            gender=new_article_data.get("gender"),
            size=new_article_data.get("size"),
            shoe_last_type=new_article_data.get("type"),
            plastic_type=new_article_data.get("plastic"),
            reinforced_compass=new_article_data.get("first"),
            second_compass_type=new_article_data.get("second"),
            processing=new_article_data.get("processing"),
            shoeing=new_article_data.get("shoeing"),
            numbering_antineck=new_article_data.get("antineck"),
            numbering_lateral=new_article_data.get("lateral"),
            numbering_heel=new_article_data.get("heel"),
            iron_tip=new_article_data.get("shoetip"),
            pivot_under_heel=new_article_data.get("pivot"),
            creation_date=DatetimeUtils.current_date(),
            produced_article_shoe_lasts=0
        )

        # Salva l'articolo nel database e ritorna il nuovo seriale
        return self.__article_newtork.insert(article_data)
