
from lib.firebaseData import firebase
from lib.mvc.profile.model.CustomerDataManager import CustomerDataManager


class CustomerController:
    def __init__(self):
        super().__init__()
        self.customer_data = CustomerDataManager()
