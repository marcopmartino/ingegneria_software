from res.Strings import Config


class ResourceManager:

    @staticmethod
    def image(filename):
        return Config.IMAGES_PATH + filename

    @staticmethod
    def icon(filename):
        return Config.ICONS_PATH + filename
