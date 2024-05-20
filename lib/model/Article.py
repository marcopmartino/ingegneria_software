from lib.model.ShoeLastVariety import ShoeLastVariety
from lib.utility.ObserverClasses import Observable


# Classe rappresentante un articolo del formificio. Un articolo riguarda una varietà di forma ed è creato solo quando
# quella varietà deve entrare per la prima volta in produzione poiché un cliente l'ha richiesta con un ordine. Il
# seriale dell'articolo ("article_serial") è generato automaticamente ed è stampato sulla forma in fase di numeratura
# insieme al seriale di produzione. Per esempio, la 32° forma prodotta dell'articolo 15 avrà il codice: "0015-0032".
# La proprietà "produced_article_shoe_lasts" indica il numero totale di forme prodotte dell'articolo in questione,
# ed è usata per determinare il seriale di produzione delle prossime.
class Article(Observable):
    def __init__(self, article_serial: str, shoe_last_variety: ShoeLastVariety, creation_date: str,
                 produced_article_shoe_lasts: int):
        super(Article, self).__init__()
        self.__article_serial = article_serial
        self.__shoe_last_variety = shoe_last_variety
        self.__creation_date = creation_date
        self.__produced_article_shoe_lasts = produced_article_shoe_lasts

    def get_article_serial(self):
        return self.__article_serial

    def get_shoe_last_variety(self):
        return self.__shoe_last_variety

    def get_creation_date(self):
        return self.__creation_date

    def get_produced_article_shoe_lasts(self):
        return self.__produced_article_shoe_lasts

    def set_produced_article_shoe_lasts(self, produced_article_shoe_lasts: int):
        self.__produced_article_shoe_lasts = produced_article_shoe_lasts
