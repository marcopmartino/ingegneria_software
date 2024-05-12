from abc import ABC

from lib.utility.ObserverClasses import Observable


class User(Observable, ABC):

    def __init__(self, uid: str, mail: str, phone: str):
        super(User, self).__init__()
        self._uid = uid
        self._mail = mail
        self._phone = phone

    def get_uid(self):
        return self._uid

    def get_phone(self):
        return self._phone

    def get_email(self):
        return self._mail

    def set_email(self, email: str):
        self._mail = email

    def set_phone(self, phone: str):
        self._phone = phone


