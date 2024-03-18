from res.Strings import Config


class ResourceManager:

    @staticmethod
    def image(filename):
        return f"url({Config.IMAGES_PATH + filename})"

    @staticmethod
    def icon(filename):
        return f"url({Config.ICONS_PATH + filename})"
