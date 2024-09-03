import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from qfluentwidgets import ImageLabel

from res.Strings import Config


class ResourceManager:

    @staticmethod
    def file_path(relative_path: str = '') -> str:
        return os.path.join(getattr(sys, '_MEIPASS', os.getcwd()), relative_path).replace('\\', '/')

    @staticmethod
    def image_path(filename: str) -> str:
        return ResourceManager.file_path(Config.IMAGES_PATH + filename)

    @staticmethod
    def icon_path(filename: str) -> str:
        return ResourceManager.file_path(Config.ICONS_PATH + filename)

    @staticmethod
    def svg_icon_path(filename: str) -> str:
        return ResourceManager.file_path(Config.SVG_ICONS_PATH + filename)

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

