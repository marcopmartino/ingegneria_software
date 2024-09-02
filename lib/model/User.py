from abc import ABC

from lib.utility.ObserverClasses import Observable


class User(Observable, ABC):

    def __init__(self, uid: str, mail: str, phone: str):
        super(User, self).__init__()
        self.__uid = uid
        self.__mail = mail
        self.__phone = phone

    def get_uid(self):
        return self.__uid

    def get_phone(self):
        return self.__phone

    def get_email(self):
        return self.__mail

    def set_email(self, email: str):
        self.__mail = email

    def set_phone(self, phone: str):
        self.__phone = phone


