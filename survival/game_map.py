from survival.player import Player
from survival.tile_layer import TileLayer


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player()
        self.tiles_layer = TileLayer(width, height)

    def draw(self, delta, window):
        self.tiles_layer.draw(window)
        self.player.draw(window)

    def update(self, delta, pressed_keys):
        self.player.update(delta, pressed_keys)
