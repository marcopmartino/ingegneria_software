from lib.firebaseData import firebase


class UserNetwork:

    @staticmethod
    def get():
        return firebase.database().child("users").get().val()

    @staticmethod
    def stream(stream_handler: callable):
        firebase.database().child("users").stream(stream_handler)

    @staticmethod
    def update(data: dict):
        firebase.database().child("users").update(data)

    @staticmethod
    def create(data: dict) -> str:
        pass

    @staticmethod
    def get_by_id(order_id: int):
        return firebase.database().child("users").child(order_id).get().val()

    @staticmethod
    def stream_by_id(user_id: str, stream_handler: callable):
        return firebase.database().child("users").child(user_id).stream(stream_handler)

    @staticmethod
    def update_by_id(user_id: int, data: dict):
        firebase.database().child("users").child(user_id).update(data)

    @staticmethod
    def delete_by_email(email: str):
        firebase.database().child("users").order_by_key("mail").equal_to(email).remove()
