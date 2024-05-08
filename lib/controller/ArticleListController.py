from lib.model.Article import Article
from lib.repository.ArticlesRepository import ArticlesRepository


class ArticleListController:

    def __init__(self):
        super().__init__()
        self.__articles_repository = ArticlesRepository()

    # Imposta un osservatore per la repository
    def observe_article_list(self, callback: callable):
        self.__articles_repository.observe(callback)

    # Ritorna un articolo in base all'id
    def get_article_by_id(self, article_id: str) -> Article:
        return self.__articles_repository.get_article_by_id(article_id)

    # Ritorna la lista di articoli filtrata
    def get_article_list(self, filters: dict[str, any]) -> list[Article]:
        return self.filter_articles(filters, *self.__articles_repository.get_article_list())

    # Filtra una lista degli articoli
    # noinspection PyMethodMayBeStatic
    def filter_articles(self, filters: dict[str, any], *articles: Article) -> list[Article]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio degli articoli

        # Parametri di filtro scelti dall'utente
        search_text: str = filters["searchbox"]  # Valore del campo dell'articolo sulla base di cui filtrare
        allowed_types: list[bool] = []  # Tipi transazione da mostrare

        # In base ai parametri di filtro, determina se un tipo di transazione è ammesso a meno
        def append_type_if_allowed(filter_key: str, type_value: bool):
            if filters[filter_key]:
                allowed_types.append(type_value)

        # Eseguo la funzione per tutti gli stati possibili
        append_type_if_allowed("with", True)
        append_type_if_allowed("without", False)

        # Numero di tipi ammessi
        allowed_types_count: int = len(allowed_types)

        # Inizializzo la lista degli elementi da ritornare
        filtered_article_list: list[Article] = []

        # Filtra la lista degli ordini
        for article in articles:

            # Se il testo di ricerca è vuoto viene saltato il filtro sul campo
            if search_text:
                if search_text not in article.get_article_serial():
                    continue

            # Se tutti i tipi sono ammessi viene saltato il filtro sul tipo
            if allowed_types_count != 2:
                if (article.get_produced_article_shoe_lasts() > 0) not in allowed_types:
                    continue

            filtered_article_list.append(article)

        return filtered_article_list
