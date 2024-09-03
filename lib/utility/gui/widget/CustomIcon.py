from enum import Enum

from qfluentwidgets import Theme, FluentIconBase

from lib.utility.ResourceManager import ResourceManager
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
        return ResourceManager.svg_icon_path(f'{self.value}_black_icon.svg')
