from survival.image import Image
from survival.tile import Tile


class TileLayer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile() for x in range(self.width)] for y in range(self.height)]
        self.image = Image('atlas.png')

    def draw(self, window):
        for y in range(self.height):
            for x in range(self.width):
                self.image.pos = (x*32, y*32)
                self.image.origin = self.tiles[y][x].origin
                self.image.draw(window)
