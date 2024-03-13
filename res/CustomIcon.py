from enum import Enum

from qfluentwidgets import getIconColor, Theme, FluentIconBase


class CustomIcon(FluentIconBase, Enum):

    PRICE = "price"
    MACHINERY = "machinery"
    WORKER = "worker"

    def path(self, theme=Theme.AUTO):
        return f'res/customIcon/{self.value}_black_icon.svg'
