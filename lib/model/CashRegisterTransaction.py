from PyQt5.QtCore import QDate


class CashRegisterTransaction:
    def __init__(self, transaction_id: str, description: str, payment_date: QDate, amount: float):
        self.__transaction_id = transaction_id
        self.__description = description
        self.__payment_date = payment_date
        self.__amount = amount

    def get_transaction_id(self) -> str:
        return self.__transaction_id

    def get_description(self) -> str:
        return self.__description

    def get_payment_date(self) -> QDate:
        return self.__payment_date

    def get_amount(self) -> float:
        return self.__amount

    def set_description(self, description: str):
        self.__description = description

    def set_payment_date(self, payment_date: QDate):
        self.__payment_date = payment_date

    def set_amount(self, amount: float):
        self.__amount = amount
