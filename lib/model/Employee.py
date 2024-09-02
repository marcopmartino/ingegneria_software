from PyQt5.QtCore import QDate

from lib.model.User import User


# noinspection PyPep8Naming,DuplicatedCode
class Employee(User):
    def __init__(self, uid: str, mail: str, phone: str, name: str, CF: str, birth_date: QDate, is_manager: bool):
        super().__init__(uid, mail, phone)
        self.__name = name
        self.__CF = CF
        self.__birth_date = birth_date
        self.__is_manager = is_manager

    def get_name(self) -> str:
        return self.__name

    def get_CF(self) -> str:
        return self.__CF

    def get_birth_date(self) -> QDate:
        return self.__birth_date

    def is_manager(self) -> bool:
        return self.__is_manager

    def set_name(self, name: str):
        self.__name = name

    def set_CF(self, CF: str):
        self.__CF = CF

    def set_birth_date(self, birth_date: str):
        self.__birth_date = birth_date
