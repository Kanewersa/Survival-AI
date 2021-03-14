import os

from survival.textureatlas import TextureAtlas
from survival.tile import Tile


class TileLayer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile() for x in range(self.width)] for y in range(self.height)]
        self.atlas = TextureAtlas(os.path.join('..', 'assets', 'atlas.png'))
        self.loadTiles()

    def loadTiles(self):
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x].image = self.atlas.image_at(self.tiles[y][x].origin, (32, 32))

    def draw(self, window):
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x] is not None:
                    window.blit(self.tiles[y][x].image, (x * 32, y * 32))
