from enum import Enum

from qfluentwidgets import Theme, FluentIconBase

from res.Strings import Config


class CustomIcon(FluentIconBase, Enum):

    ARTICLE = "article"
    CASH_REGISTER = "cash_register"
    EURO = "euro"
    MACHINERY = "machinery"
    PRICE = "price"
    PROFILE = "profile"
    STORAGE = "storage"
    WORKER = "worker"
    USER_INFO = "user_info"

    def path(self, theme=Theme.AUTO):
        return f'{Config.SVG_ICONS_PATH}{self.value}_black_icon.svg'
