from lib.mvc.order.model.Article import Article
from lib.network.ArticleNetwork import ArticleNetwork
from lib.utility.ObserverClasses import Observable
from lib.utility.Singleton import ObservableSingleton


class ArticleList(Observable, metaclass=ObservableSingleton):

    def __init__(self):
        super().__init__()
        self.__article_list: list[Article] = []
        ArticleNetwork.stream(self.__stream_handler)

    # Usato internamente per aggiungere un articolo alla lista
    def __append_article(self, serial: str, data: any):
        self.__article_list.append(Article(
            serial, data["gender"], data["size"], data["shoe_last_type"], data["plastic_type"],
            data["reinforced_compass"], data["second_compass_type"], data["processing"], data["shoeing"],
            data["numbering_antineck"], data["numbering_lateral"], data["numbering_heel"], data["iron_tip"],
            data["pivot_under_heel"], data["produced_article_shoe_lasts"]
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
                            self.__append_article(key, value)

                    # Quando viene creato un nuovo articolo
                    else:
                        self.__append_article(path.split("/")[1], data)
                case "patch":
                    pass
                case "cancel":
                    pass

        # Notifico gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
        message["notifier"] = "ArticleList"
        self.notify(message)

    # Ritorna la lista di ordini
    def get(self) -> list[Article]:
        return self.__article_list

    # Ritorna un articolo in base al suo numero
    def get_by_id(self, article_serial: str) -> Article:
        for article in self.__article_list:
            if article.article_serial == article_serial:
                return article

    # Salva il nuovo articolo nel database. Il seriale è rimosso perché viene assegnato automaticamente.
    @staticmethod
    def add(article: Article) -> str:
        # Converte l'articolo in dizionario
        article_dict = vars(article)
        # Rimuove il numero dell'articolo
        article_dict.pop("article_serial")
        # Salva l'articolo nel database e ne ritorna l'id
        return ArticleNetwork.create(article_dict)

    # Controlla se l'articolo esiste già
    def exists(self, new_article: Article) -> (bool, str):
        print(f"Nuovo articolo:{vars(new_article)}")
        for article in self.__article_list:
            print(f"Articolo:{vars(article)}")
            if (article.gender == new_article.gender
                    and article.size == new_article.size
                    and article.plastic_type == new_article.plastic_type
                    and article.shoe_last_type == new_article.shoe_last_type
                    and article.reinforced_compass == new_article.reinforced_compass
                    and article.second_compass_type == new_article.second_compass_type
                    and article.processing == new_article.processing
                    and article.shoeing == new_article.shoeing
                    and article.numbering_antineck == new_article.numbering_antineck
                    and article.numbering_lateral == new_article.numbering_lateral
                    and article.numbering_heel == new_article.numbering_heel
                    and article.iron_tip == new_article.iron_tip
                    and article.pivot_under_heel == new_article.pivot_under_heel):
                print("Trovato")
                return True, article.article_serial
        return False, -1
