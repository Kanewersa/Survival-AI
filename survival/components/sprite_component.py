from survival.image import Image


class SpriteComponent:
    def __init__(self, path):
        self.image = Image(path)

    def set_scale(self, scale):
        self.image.set_scale(scale)
