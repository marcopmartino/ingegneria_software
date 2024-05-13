from pyrebase.pyrebase import Stream

from lib.firebaseData import Firebase
from lib.utility.UtilityClasses import SerialNumberFormatter


class ArticlesNetwork:

    @staticmethod
    def stream(stream_handler: callable) -> Stream:
        return Firebase.database.child("articles").stream(stream_handler)

    @staticmethod
    def get_next_id():
        return Firebase.database.child("next_ids").get().val()["article"]

    @staticmethod
    def insert(data: dict) -> str:
        db = Firebase.database
        article_id: int = ArticlesNetwork.get_next_id()
        serial_number: str = SerialNumberFormatter.format(article_id)
        db.child("articles").child(serial_number).set(data)
        db.child("next_ids").update({"article": article_id + 1})
        return serial_number

    @staticmethod
    def update_production_counter(article_id: str, new_value: int):
        Firebase.database.child("articles").child(article_id).update({"produced_article_shoe_lasts": new_value})
