from pyrebase.pyrebase import Stream

from lib.firebaseData import Firebase


class PriceCatalogNetwork:

    @staticmethod
    def stream(stream_handler: callable) -> Stream:
        return Firebase.database.child("shoe_last_factory_price_list").stream(stream_handler)

    @staticmethod
    def update(data: dict):
        Firebase.database.child("shoe_last_factory_price_list").update(data)
