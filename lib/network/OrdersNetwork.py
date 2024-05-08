from pyrebase.pyrebase import Stream

from lib.firebaseData import Firebase
from lib.model.Order import Order
from lib.utility.UtilityClasses import SerialNumberFormatter


class OrdersNetwork:

    @staticmethod
    def stream(stream_handler: callable) -> Stream:
        return Firebase.database.child("orders").stream(stream_handler)

    @staticmethod
    def get_next_id():
        return Firebase.database.child("next_ids").get().val()["order"]

    @staticmethod
    def insert(data: dict) -> str:
        db = Firebase.database
        order_id: int = OrdersNetwork.get_next_id()
        serial_number: str = SerialNumberFormatter.format(order_id)
        db.child("orders").child(serial_number).set(data)
        db.child("next_ids").update({"order": order_id + 1})
        return serial_number

    @staticmethod
    def update(order_id: str, data: dict):
        Firebase.database.child("orders").child(order_id).update(data)

    @staticmethod
    def delete(order_id: str):
        Firebase.database.child("orders").child(order_id).remove()
