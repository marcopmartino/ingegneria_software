from lib.firebaseData import Firebase
from lib.utility.ErrorHelpers import HTTPErrorHelper


class UsersNetwork:

    @staticmethod
    def stream(stream_handler: callable):
        return Firebase.database.child("users").stream(stream_handler) if Firebase.auth.currentUserRole() != "customer"\
            else Firebase.database.child("users").child(Firebase.auth.currentUserId()).stream(stream_handler)

    @staticmethod
    def register_user(data: dict[str, any], sign_in: bool) -> str:
        new_uid = HTTPErrorHelper.differentiate(
            lambda: Firebase.auth.create_user_with_email_and_password(data["mail"], data.pop("password"), sign_in)
        )
        Firebase.database.child('users').child(new_uid).set(data)
        if sign_in:
            UsersNetwork.update_current_user_role()
        return new_uid

    @staticmethod
    def update(user_id: str, data: dict):
        new_password = data.pop("password")
        if new_password:
            Firebase.auth.updateUserPasswordById(user_id, new_password)

        Firebase.database.child("users").child(user_id).update(data)

    @staticmethod
    def delete(user_id: str):
        Firebase.auth.deleteUserById(user_id)
        Firebase.database.child("users").child(user_id).remove()

    @staticmethod
    def authenticate_user(email: str, password: str):
        HTTPErrorHelper.differentiate(lambda: Firebase.auth.sign_in_with_email_and_password(email, password))
        UsersNetwork.update_current_user_role()

    @staticmethod
    def update_current_user_role():
        auth = Firebase.auth
        auth.setCurrentUserRole(Firebase.database.child('users').child(auth.currentUserId()).get().val()['role'])

    @staticmethod
    def reauthenticate_current_user(password: str):
        UsersNetwork.authenticate_user(Firebase.auth.currentUserEmail(), password)
