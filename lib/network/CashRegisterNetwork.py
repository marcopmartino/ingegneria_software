from pyrebase.pyrebase import Stream

from lib.firebaseData import Firebase


class CashRegisterNetwork:

    @staticmethod
    def stream(stream_handler: callable) -> Stream:
        return Firebase.database.child("transactions").stream(stream_handler)

    @staticmethod
    def get_next_id():
        return Firebase.database.child("next_ids").get().val()["transaction"]

    @staticmethod
    def insert(data: dict) -> str:
        db = Firebase.database
        transaction_id: int = CashRegisterNetwork.get_next_id()
        serial_number: str = f"{transaction_id:04d}"
        db.child("transactions").child(serial_number).set(data)
        db.child("next_ids").update({"order": transaction_id + 1})
        return serial_number

    @staticmethod
    def update(order_id: str, data: dict):
        Firebase.database.child("transactions").child(order_id).update(data)

    @staticmethod
    def delete(order_id: str):
        Firebase.database.child("transactions").child(order_id).remove()
