from survival.image import Image
from survival.generators.tile_generator import TileGenerator
from survival.tile import Tile


class TileLayer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles: list[list[Tile]] = TileGenerator.generate_biome_tiles(width, height)
        # self.tiles: list[list[Tile]] = TileGenerator.generate_random_tiles(width, height)
        self.image = Image('atlas.png')

    def draw(self, camera, visible_area):
        for y in range(int(visible_area.top / 32), int(visible_area.height / 32) + 1):
            for x in range(int(visible_area.left / 32), int(visible_area.width / 32) + 1):
                if y >= self.height or x >= self.width:
                    continue

                self.image.pos = (x * 32, y * 32)
                self.image.origin = self.tiles[y][x].origin
                camera.draw(self.image)

    def get_cost(self, pos):
        return self.tiles[pos[1]][pos[0]].cost
