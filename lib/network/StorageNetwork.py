from lib.firebaseData import firebase


class StorageNetwork:

    @staticmethod
    def get_products():
        return firebase.database().child("storage").child("products").get().val()

    @staticmethod
    def get_materials():
        return firebase.database().child("storage").child("materials").get().val()

    @staticmethod
    def get_wastes():
        return firebase.database().child("storage").child("wastes").get().val()

    @staticmethod
    def products_stream(stream_handler: callable):
        firebase.database().child("storage").child("products").stream(stream_handler)

    @staticmethod
    def materials_stream(stream_handler: callable):
        firebase.database().child("storage").child("materials").stream(stream_handler)

    @staticmethod
    def wastes_stream(stream_handler: callable):
        firebase.database().child("storage").child("wastes").stream(stream_handler)

    @staticmethod
    def update_product(serial_id: str, data: dict):
        firebase.database().child("storage").child("products").child(serial_id).update(data)

    @staticmethod
    def update_material(serial_id: str, data: dict):
        firebase.database().child("storage").child("materials").child(serial_id).update(data)

    @staticmethod
    def update_waste(serial_id: str, data: dict):
        firebase.database().child("storage").child("wastes").child(serial_id).update(data)

    @staticmethod
    def get_next_product_id():
        return firebase.database().child("next_ids").get().val()["product"]

    @staticmethod
    def get_next_material_id():
        return firebase.database().child("next_ids").get().val()["material"]

    @staticmethod
    def get_next_waste_id():
        return firebase.database().child("next_ids").get().val()["waste"]

    @staticmethod
    def get_product_by_id(product_id: int):
        return firebase.database().child("storage").child("products").child(product_id).get().val()

    @staticmethod
    def get_material_by_id(material_id: int):
        return firebase.database().child("storage").child("materials").child(material_id).get().val()

    @staticmethod
    def get_waste_by_id(waste_id: int):
        return firebase.database().child("storage").child("wastes").child(waste_id).get().val()

    @staticmethod
    def stream_product_by_id(product_id: int, stream_handler: callable):
        return firebase.database().child("storage").child("products").child(product_id).stream(stream_handler)

    @staticmethod
    def stream_material_by_id(material_id: int, stream_handler: callable):
        return firebase.database().child("storage").child("materials").child(material_id).stream(stream_handler)

    @staticmethod
    def stream_waste_by_id(waste_id: int, stream_handler: callable):
        return firebase.database().child("storage").child("wastes").child(waste_id).stream(stream_handler)

    @staticmethod
    def update_product_by_id(product_id: int, data: dict):
        firebase.database().child("storage").child("products").child(product_id).update(data)

    @staticmethod
    def update_material_by_id(material_id: int, data: dict):
        firebase.database().child("storage").child("materials").child(material_id).update(data)

    @staticmethod
    def update_waste_by_id(waste_id: int, data: dict):
        firebase.database().child("storage").child("wastes").child(waste_id).update(data)

    @staticmethod
    def delete_product_by_id(product_id: int):
        firebase.database().child("storage").child("products").child(product_id).remove()

    @staticmethod
    def delete_material_by_id(material_id: int):
        firebase.database().child("storage").child("materials").child(material_id).remove()

    @staticmethod
    def delete_waste_by_id(waste_id: int):
        firebase.database().child("storage").child("wastes").child(waste_id).remove()

    @staticmethod
    def insert_product(data: dict) -> str:
        db = firebase.database().child("storage")
        product_id: int = ProductNetwork.get_next_product_id()
        serial_number: str = f"{product_id:04d}"
        db.child("product").child(serial_number).set(data)
        db.child("next_ids").update({"product": product_id + 1})
        return serial_number

    @staticmethod
    def insert_material(data: dict) -> str:
        db = firebase.database().child("storage")
        material_id: int = ProductNetwork.get_next_material_id()
        serial_number: str = f"{material_id:04d}"
        db.child("materials").child(serial_number).set(data)
        db.child("next_ids").update({"material": material_id + 1})
        return serial_number

    @staticmethod
    def insert_waste(data: dict) -> str:
        db = firebase.database().child("storage")
        waste_id: int = ProductNetwork.get_next_waste_id()
        serial_number: str = f"{waste_id:04d}"
        db.child("wastes").child(serial_number).set(data)
        db.child("next_ids").update({"waste": waste_id + 1})
        return serial_number

    @staticmethod
    def get_max_products_storage():
        return firebase.database().child("storage").get().val()['max_products_storage']

    @staticmethod
    def get_available_products_storage():
        return firebase.database().child("storage").get().val()['available_products_storage']

    @staticmethod
    def get_used_products_storage():
        return firebase.database().child("storage").get().val()['used_products_storage']

    @staticmethod
    def get_max_materials_storage():
        return firebase.database().child("storage").get().val()['max_materials_storage']

    @staticmethod
    def get_available_materials_storage():
        return firebase.database().child("storage").get().val()['available_materials_storage']

    @staticmethod
    def get_used_materials_storage():
        return firebase.database().child("storage").get().val()['used_materials_storage']

    @staticmethod
    def get_max_wastes_storage():
        return firebase.database().child("storage").get().val()['max_wastes_storage']

    @staticmethod
    def get_available_wastes_storage():
        return firebase.database().child("storage").get().val()['available_wastes_storage']

    @staticmethod
    def get_used_wastes_storage():
        return firebase.database().child("storage").get().val()['used_wastes_storage']

