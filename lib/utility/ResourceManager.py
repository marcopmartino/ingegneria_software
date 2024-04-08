from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from qfluentwidgets import ImageLabel

from res.Strings import Config


class ResourceManager:

    @staticmethod
    def image_path(filename: str) -> str:
        return Config.IMAGES_PATH + filename

    @staticmethod
    def icon_path(filename: str) -> str:
        return Config.ICONS_PATH + filename

    @staticmethod
    def image(filename: str) -> QImage:
        return QImage(ResourceManager.image_path(filename))

    @staticmethod
    def icon(filename: str, width: int = 24, height: int = 24,
             aspect_ratio_mode: Qt.AspectRatioMode = Qt.KeepAspectRatio,
             transformation_mode: Qt.TransformationMode = Qt.SmoothTransformation) -> QImage:
        return QImage(ResourceManager.icon_path(filename)).scaled(
            width, height, aspect_ratio_mode, transformation_mode)

    @staticmethod
    def image_label(filename: str) -> ImageLabel:
        return ImageLabel(ResourceManager.image(filename))

    @staticmethod
    def icon_label(filename: str, width: int = 24, height: int = 24,
                   aspect_ratio_mode: Qt.AspectRatioMode = Qt.KeepAspectRatio,
                   transformation_mode: Qt.TransformationMode = Qt.SmoothTransformation) -> ImageLabel:
        return ImageLabel(ResourceManager.icon(filename, width, height, aspect_ratio_mode, transformation_mode))
