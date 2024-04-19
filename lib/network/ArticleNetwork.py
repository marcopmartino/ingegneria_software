from lib.firebaseData import firebase


class ArticleNetwork:

    @staticmethod
    def stream(stream_handler: callable):
        firebase.database().child("articles").stream(stream_handler)

    @staticmethod
    def get_next_id():
        return firebase.database().child("next_ids").get().val()["article"]

    @staticmethod
    def insert(data: dict) -> str:
        db = firebase.database()
        article_id: int = ArticleNetwork.get_next_id()
        serial_number: str = f"{article_id:04d}"
        db.child("articles").child(serial_number).set(data)
        db.child("next_ids").update({"article": article_id + 1})
        return serial_number

    @staticmethod
    def update(article_id: str, data: dict):
        firebase.database().child("articles").child(article_id).update(data)
