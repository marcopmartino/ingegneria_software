
from lib.firebaseData import firebase
from lib.mvc.profile.model.StaffDataManager import StaffDataManager


class StaffController:
    def __init__(self):
        super().__init__()
        self.staff_data = StaffDataManager()

        self.auth = firebase.auth()
        self.database = firebase.database()



