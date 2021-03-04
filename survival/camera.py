from pygame.rect import Rect


class Camera:
    def __init__(self, width, height):
        self.camera = Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, game_object):
        return game_object.get_rect().move(self.camera.topleft)

    def update(self, target_object):
        x = -target_object.get_rect().x + int(self.width / 2)
        y = -target_object.get_rect().y + int(self.height / 2)
        self.camera = Rect(x, y, self.width, self.height)
