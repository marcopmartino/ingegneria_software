from pyrebase.pyrebase import Stream

from lib.firebaseData import Firebase
from lib.utility.UtilityClasses import SerialNumberFormatter


class StorageNetwork:

    @staticmethod
    def stream(stream_handler: callable) -> Stream:
        return Firebase.database.child("storage").stream(stream_handler)

    @staticmethod
    def update_product_amount(serial_id: str, product_amount: int):
        Firebase.database.child("storage").child("products").child(serial_id).update({"amount": product_amount})

    @staticmethod
    def update_material_amount(serial_id: str, material_amount: int):
        Firebase.database.child("storage").child("materials").child(serial_id).update({"amount": material_amount})

    @staticmethod
    def update_waste_amount(waste_id: str, waste_amount: int):
        Firebase.database.child("storage").child("waste").child(waste_id).update({"amount": waste_amount})

    @staticmethod
    def get_next_product_id():
        return Firebase.database.child("next_ids").get().val()["product"]

    @staticmethod
    def insert_product(data: dict) -> str:
        db = Firebase.database
        product_id: int = StorageNetwork.get_next_product_id()
        serial_number: str = SerialNumberFormatter.format(product_id)
        db.child("storage").child("products").child(serial_number).set(data)
        db.child("next_ids").update({"product": product_id + 1})
        return serial_number

    @staticmethod
    def delete_product(product_id: str) -> None:
        Firebase.database.child("storage").child("products").child(product_id).remove()

