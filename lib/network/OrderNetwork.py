from lib.firebaseData import firebase


class OrderNetwork:

    @staticmethod
    def get():
        return firebase.database().child("orders").get().val()

    @staticmethod
    def stream(stream_handler: callable):
        firebase.database().child("orders").stream(stream_handler)

    @staticmethod
    def update(data: dict):
        firebase.database().child("orders").update(data)

    @staticmethod
    def get_next_id():
        return firebase.database().child("next_ids").get().val()["order"]

    @staticmethod
    def create(data: dict) -> str:
        db = firebase.database()
        order_id: int = OrderNetwork.get_next_id()
        serial_number: str = f"{order_id:04d}"
        db.child("orders").child(serial_number).set(data)
        db.child("next_ids").update({"order": order_id + 1})
        return serial_number

    @staticmethod
    def get_by_id(order_id: int):
        return firebase.database().child("orders").child(order_id).get().val()

    @staticmethod
    def stream_by_id(order_id: int, stream_handler: callable):
        return firebase.database().child("orders").child(order_id).stream(stream_handler)

    @staticmethod
    def update_by_id(order_id: int, data: dict):
        firebase.database().child("orders").child(order_id).update(data)

    @staticmethod
    def delete_by_id(order_id: int):
        firebase.database().child("orders").child(order_id).remove()
