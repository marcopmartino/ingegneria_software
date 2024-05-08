from lib.model.Article import Article
from lib.repository.ArticlesRepository import ArticlesRepository
from lib.repository.OrdersRepository import OrdersRepository

from lib.utility.ObserverClasses import AnonymousObserver, Observer


class ArticleController:
    def __init__(self, article: Article):
        super().__init__()

        # Repositories
        self.__orders_repository: OrdersRepository = OrdersRepository()
        self.__articles_repository: ArticlesRepository = ArticlesRepository()

        # Models
        self.__article: Article = article

    def get_article(self):
        return self.__article

    def get_article_serial(self):
        return self.__article.get_article_serial()

    def get_article_creation_date(self):
        return self.__article.get_creation_date()

    def get_produced_article_shoe_lasts(self):
        return self.__article.get_produced_article_shoe_lasts()

    def get_article_orders(self):
        return self.__orders_repository.get_order_list_by_article_id(self.__article.get_article_serial())

    def observe_article(self, callback: callable) -> Observer:
        observer = AnonymousObserver(callback)
        self.__article.attach(observer)
        return observer

    def detach_article_observer(self, observer: Observer):
        self.__article.detach(observer)
