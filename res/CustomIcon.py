from enum import Enum

from qfluentwidgets import getIconColor, Theme, FluentIconBase


class CustomIcon(FluentIconBase, Enum):

    ARTICLE = "article"
    CASH_REGISTER = "cash_register"
    EURO = "euro"
    MACHINERY = "machinery"
    PRICE = "price"
    PROFILE = "profile"
    WORKER = "worker"
    USER_INFO = "user_info"

    def path(self, theme=Theme.AUTO):
        return f'res/customIcon/{self.value}_black_icon.svg'
