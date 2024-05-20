from lib.firebaseData import Firebase
from lib.model.Product import Product


class StorageNetwork:

    @staticmethod
    def stream(stream_handler: callable):
        Firebase.database.child("storage").stream(stream_handler)

    @staticmethod
    def update_product(serial_id: str, data: dict):
        Firebase.database.child("storage").child("products").child(serial_id).update(data)

    @staticmethod
    def update_material(serial_id: str, data: dict):
        Firebase.database.child("storage").child("materials").child(serial_id).update(data)

    @staticmethod
    def update_waste_amount(waste_id: str, waste_amount: str):
        Firebase.database.child("storage").child("wastes").child(waste_id).update({"amount": str(waste_amount)})

    @staticmethod
    def delete_product_by_id(product_id: str):
        Firebase.database.child("storage").child("products").child(product_id).remove()

    @staticmethod
    def delete_material_by_id(material_id: str):
        Firebase.database.child("storage").child("materials").child(material_id).remove()

    @staticmethod
    def delete_waste_by_id(waste_id: str):
        Firebase.database.child("storage").child("wastes").child(waste_id).remove()

    @staticmethod
    def get_next_product_id():
        return Firebase.database.child("next_ids").get().val()["product"]

    @staticmethod
    def get_next_material_id():
        return Firebase.database.child("next_ids").get().val()["material"]

    @staticmethod
    def get_next_waste_id():
        return Firebase.database.child("next_ids").get().val()["waste"]

    @staticmethod
    def delete_product_by_id(product_id: int):
        Firebase.database.child("storage").child("products").child(product_id).remove()

    @staticmethod
    def delete_material_by_id(material_id: int):
        Firebase.database.child("storage").child("materials").child(material_id).remove()

    @staticmethod
    def delete_waste_by_id(waste_id: int):
        Firebase.database.child("storage").child("wastes").child(waste_id).remove()

    @staticmethod
    def insert_product(data: dict) -> str:
        db = Firebase.database.child("storage")
        product_id: int = StorageNetwork.get_next_product_id()
        serial_number: str = f"{product_id:04d}"
        db.child("product").child(serial_number).set(data)
        db.child("next_ids").update({"product": product_id + 1})
        return serial_number

    @staticmethod
    def insert_material(data: dict) -> str:
        db = Firebase.database.child("storage")
        material_id: int = StorageNetwork.get_next_material_id()
        serial_number: str = f"{material_id:04d}"
        db.child("materials").child(serial_number).set(data)
        db.child("next_ids").update({"material": material_id + 1})
        return serial_number

    @staticmethod
    def insert_waste(data: dict) -> str:
        db = Firebase.database.child("storage")
        waste_id: int = StorageNetwork.get_next_waste_id()
        serial_number: str = f"{waste_id:04d}"
        db.child("wastes").child(serial_number).set(data)
        db.child("next_ids").update({"waste": waste_id + 1})
        return serial_number

    @staticmethod
    def get_max_products_storage():
        return Firebase.database.child("storage").get().val()['max_products_storage']

    @staticmethod
    def get_available_products_storage():
        return Firebase.database.child("storage").get().val()['available_products_storage']

    @staticmethod
    def get_used_products_storage():
        return Firebase.database.child("storage").get().val()['used_products_storage']

    @staticmethod
    def get_max_materials_storage():
        return Firebase.database.child("storage").get().val()['max_materials_storage']

    @staticmethod
    def get_available_materials_storage():
        return Firebase.database.child("storage").get().val()['available_materials_storage']

    @staticmethod
    def get_used_materials_storage():
        return Firebase.database.child("storage").get().val()['used_materials_storage']

    @staticmethod
    def get_max_wastes_storage():
        return Firebase.database.child("storage").get().val()['max_wastes_storage']

    @staticmethod
    def get_available_wastes_storage():
        return Firebase.database.child("storage").get().val()['available_wastes_storage']

    @staticmethod
    def get_used_wastes_storage():
        return Firebase.database.child("storage").get().val()['used_wastes_storage']

