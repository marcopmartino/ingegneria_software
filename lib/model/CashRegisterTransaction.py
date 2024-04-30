class CashRegisterTransaction:
    def __init__(self, transaction_id: str, description: str, payment_date: str, amount: float,
                 is_revenue: bool):
        self.__transaction_id = transaction_id
        self.__description = description
        self.__payment_date = payment_date
        self.__amount = amount
        self.__is_revenue = is_revenue

    def get_transaction_id(self) -> str:
        return self.__transaction_id

    def get_description(self) -> str:
        return self.__description

    def get_payment_date(self) -> str:
        return self.__payment_date

    def get_amount(self) -> float:
        return self.__amount

    def is_revenue(self) -> bool:
        return self.__is_revenue

    def set_description(self, description: str):
        self.__description = description

    def set_payment_date(self, payment_date: str):
        self.__payment_date = payment_date

    def set_amount(self, amount: float):
        self.__amount = amount

    def set_transaction_type(self, is_revenue: bool):
        self.__is_revenue = is_revenue
