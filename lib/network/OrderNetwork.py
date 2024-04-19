from lib.firebaseData import firebase
from lib.model.Order import Order


class OrderNetwork:

    @staticmethod
    def stream(stream_handler: callable):
        firebase.database().child("orders").stream(stream_handler)

    @staticmethod
    def get_next_id():
        return firebase.database().child("next_ids").get().val()["order"]

    @staticmethod
    def insert(data: dict) -> str:
        db = firebase.database()
        order_id: int = OrderNetwork.get_next_id()
        serial_number: str = f"{order_id:04d}"
        db.child("orders").child(serial_number).set(data)
        db.child("next_ids").update({"order": order_id + 1})
        return serial_number

    @staticmethod
    def update(order_id: str, data: dict):
        firebase.database().child("orders").child(order_id).update(data)

    @staticmethod
    def delete(order_id: str):
        firebase.database().child("orders").child(order_id).remove()
