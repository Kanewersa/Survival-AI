from pygame.rect import Rect

from survival import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self, width, height, window):
        self.camera = Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.window = window

    def draw(self, image):
        image.draw(self.window, self)

    def apply(self, pos):
        return pos[0] + self.camera.left, pos[1] + self.camera.top

    def get_visible_area(self):
        return Rect(-self.camera.left, -self.camera.top,
                    SCREEN_WIDTH - self.camera.left, SCREEN_HEIGHT - self.camera.top)

    def update(self, target):
        x = -target.pos[0] + int(SCREEN_WIDTH / 2)
        y = -target.pos[1] + int(SCREEN_HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)
        self.camera = Rect(x, y, self.width, self.height)
