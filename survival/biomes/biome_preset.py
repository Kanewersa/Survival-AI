import random
from typing import List

from survival.tile import Tile


class BiomePreset:
    def __init__(self, name, min_height: float, min_moisture: float, min_heat: float, tiles: List[Tile]):
        self.name = name
        self.min_height = min_height
        self.min_moisture = min_moisture
        self.min_heat = min_heat
        self.tiles = tiles

    def get_new_tile(self):
        tile = random.choice(self.tiles)
        return Tile(origin=tile.origin, cost=tile.cost, biome=self)

    def get_tile_sprite(self):
        pass

    def match_conditions(self, height, moisture, heat):
        return height >= self.min_height and moisture >= self.min_moisture and heat >= self.min_heat
