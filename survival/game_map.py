from survival.player import Player
from survival.tile_layer import TileLayer


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player()
        self.layers = []
        self.layers.append(TileLayer(width, height))

    def draw(self, camera):
        visible_area = camera.get_visible_area()
        for layer in self.layers:
            layer.draw(camera, visible_area)
        self.player.draw(camera)

    def update(self, camera, delta, pressed_keys):
        self.player.update(delta, pressed_keys)
        camera.update(self.player)
