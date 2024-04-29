from lib.firebaseData import firebase
from lib.network.HTTPErrorHelper import HTTPErrorHelper


class UserNetwork:

    @staticmethod
    def get():
        return firebase.database().child("users").get_price_catalog().val()

    @staticmethod
    def stream(stream_handler: callable):
        firebase.database().child("users").stream(stream_handler)

    @staticmethod
    def update(form_data: dict[str, any], newPassword, uid):
        print("Inizio invio dati")
        HTTPErrorHelper.differentiate(
            lambda: firebase.database.child('users').child(uid).update_price_catalog(form_data))

        if newPassword is not None:
            HTTPErrorHelper.differentiate(
                lambda: firebase.update_user(uid, password=newPassword))

    @staticmethod
    def create_profile(email, password):
        HTTPErrorHelper.differentiate(
            lambda: firebase.auth().create_user_with_email_and_password(email, password))

    @staticmethod
    def create_data(form_data, user):
        HTTPErrorHelper.differentiate(
            lambda: firebase.database().child('users').child(user['localId']).set(form_data))

    @staticmethod
    def get_by_id(order_id: int):
        return firebase.database().child("users").child(order_id).get_price_catalog().val()

    @staticmethod
    def stream_by_id(user_id: str, stream_handler: callable):
        return firebase.database().child("users").child(user_id).stream(stream_handler)

    @staticmethod
    def update_by_id(user_id: int, data: dict):
        firebase.database().child("users").child(user_id).update_price_catalog(data)

    @staticmethod
    def delete_by_email(email: str):
        firebase.database().child("users").order_by_key("mail").equal_to(email).remove()

    @staticmethod
    def checkLogin(currentEmail: str, password: str):
        HTTPErrorHelper.differentiate(
            lambda: firebase.auth().sign_in_with_email_and_password(currentEmail, password))
