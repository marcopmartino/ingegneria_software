from enum import Enum

from lib.utility.ObserverClasses import Observable
from res.Strings import OrderStateStrings


class OrderState(Enum):
    NOT_STARTED = OrderStateStrings.NOT_STARTED
    PROCESSING = OrderStateStrings.PROCESSING
    COMPLETED = OrderStateStrings.COMPLETED
    DELIVERED = OrderStateStrings.DELIVERED


class Order(Observable):

    def __init__(self, order_serial: str, article_serial: str, state: OrderState, customer_id: str, quantity: int,
                 price: float, first_product_serial: int, creation_date: str):
        super(Order, self).__init__()
        self.__order_serial = order_serial
        self.__article_serial = article_serial
        self.__state = state
        self.__customer_id = customer_id
        self.__quantity = quantity
        self.__price = price
        self.__first_product_serial = first_product_serial
        self.__creation_date = creation_date

    def get_order_serial(self) -> str:
        return self.__order_serial

    def get_article_serial(self) -> str:
        return self.__article_serial

    def get_state(self) -> OrderState:
        return self.__state

    def get_customer_id(self) -> str:
        return self.__customer_id

    def get_quantity(self) -> int:
        return self.__quantity

    def get_price(self) -> float:
        return self.__price

    def get_first_product_serial(self) -> int:
        return self.__first_product_serial

    def get_creation_date(self) -> str:
        return self.__creation_date

    def set_article_serial(self, article_serial: str) -> None:
        self.__article_serial = article_serial

    def set_state(self, state: OrderState) -> None:
        self.__state = state

    def set_quantity(self, quantity: int) -> None:
        self.__quantity = quantity

    def set_price(self, price: float) -> None:
        self.__price = price

    def set_first_product_serial(self, first_product_serial: int) -> None:
        self.__first_product_serial = first_product_serial
