from lib.firebaseData import firebase


class PriceCatalogNetwork:

    @staticmethod
    def get():
        return firebase.database().child("shoe_last_factory_price_list").get().val()

    @staticmethod
    def stream(stream_handler: callable):
        firebase.database().child("shoe_last_factory_price_list").stream(stream_handler)

    @staticmethod
    def update(data: dict):
        firebase.database().child("shoe_last_factory_price_list").update(data)
