import random

from survival.tile import Tile


class TileGenerator:
    templates = [
        [(0, 0), 1],  # Grass 1
        [(32, 0), 1],  # Grass 2
        [(64, 0), 1],  # Grass 3
        [(96, 0), 1],  # Grass 4
        [(64, 64), 2],  # Sand
        [(96, 64), 2],  # Poddle
    ]

    @staticmethod
    def get_random_tile():
        template = random.choice(TileGenerator.templates)
        return Tile(template[0], template[1])
