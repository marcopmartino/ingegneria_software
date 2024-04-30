from pyrebase.pyrebase import Stream

from lib.firebaseData import firebase


class CashRegisterNetwork:

    @staticmethod
    def stream(stream_handler: callable) -> Stream:
        return firebase.database().child("transactions").stream(stream_handler)

    @staticmethod
    def get_next_id():
        return firebase.database().child("next_ids").get().val()["transaction"]

    @staticmethod
    def insert(data: dict) -> str:
        db = firebase.database()
        transaction_id: int = CashRegisterNetwork.get_next_id()
        serial_number: str = f"{transaction_id:04d}"
        db.child("transactions").child(serial_number).set(data)
        db.child("next_ids").update({"order": transaction_id + 1})
        return serial_number

    @staticmethod
    def update(order_id: str, data: dict):
        firebase.database().child("transactions").child(order_id).update(data)

    @staticmethod
    def delete(order_id: str):
        firebase.database().child("transactions").child(order_id).remove()
