from lib.model.User import User


# noinspection PyPep8Naming
class Customer(User):

    def __init__(self, uid: str, mail: str, phone: str, company: str, delivery: str, IVA: str):
        super().__init__(uid, mail, phone)
        self.__company = company
        self.__delivery = delivery
        self.__IVA = IVA

    def get_company_name(self) -> str:
        return self.__company

    def get_delivery_address(self) -> str:
        return self.__delivery

    def get_IVA(self) -> str:
        return self.__IVA

    def set_company_name(self, company_name: str):
        self.__company = company_name

    def set_delivery_address(self, delivery_address: str):
        self.__delivery = delivery_address

    def set_IVA(self, IVA: str):
        self.__IVA = IVA
