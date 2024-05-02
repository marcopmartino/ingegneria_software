from lib.firebaseData import Firebase
from lib.utility.HTTPErrorHelper import HTTPErrorHelper


class UsersNetwork:

    @staticmethod
    def get():
        return Firebase.database.child("users").get().val()

    @staticmethod
    def stream(stream_handler: callable):
        Firebase.database.child("users").stream(stream_handler)

    @staticmethod
    def update(form_data: dict[str, any], newPassword, uid):
        print("Inizio invio dati")
        HTTPErrorHelper.differentiate(
            lambda: Firebase.database.child('users').child(uid).update(form_data))

        if newPassword is not None:
            HTTPErrorHelper.differentiate(
                lambda: Firebase.auth.updateCurrentUserPassword(newPassword))

    @staticmethod
    def create_profile(email, password):
        HTTPErrorHelper.differentiate(
            lambda: Firebase.auth.create_user_with_email_and_password(email, password))

    @staticmethod
    def create_worker_profile(email, password):
        return HTTPErrorHelper.differentiate(
            lambda: Firebase.auth.create_user_with_email_and_password(email, password))

    @staticmethod
    def create_data(form_data, user):
        HTTPErrorHelper.differentiate(
            lambda: Firebase.database.child('users').child(user['localId']).set(form_data))

    @staticmethod
    def get_by_id(order_id: int):
        return Firebase.database.child("users").child(order_id).get().val()

    @staticmethod
    def stream_by_id(user_id: str, stream_handler: callable):
        return Firebase.database.child("users").child(user_id).stream(stream_handler)

    @staticmethod
    def update_by_id(user_id: int, data: dict):
        Firebase.database.child("users").child(user_id).update(data)

    @staticmethod
    def delete_by_email(email: str):
        Firebase.database.child("users").order_by_key("mail").equal_to(email).remove()

    @staticmethod
    def checkLogin(currentEmail: str, password: str):
        HTTPErrorHelper.differentiate(
            lambda: Firebase.auth.sign_in_with_email_and_password(currentEmail, password))

    @staticmethod
    def authenticate_user(email: str, password: str):
        auth = Firebase.auth
        auth.sign_in_with_email_and_password(email, password)
        auth.current_user['role'] = Firebase.database.child('users').child(auth.currentUserId()).get().val()['role']
