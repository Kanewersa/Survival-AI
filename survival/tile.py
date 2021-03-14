import random


class Tile:
    origins = [(0, 0), (32, 0), (64, 0), (96, 0)]

    def __init__(self, origin=(0, 0)):
        self.origin = random.choice(Tile.origins)
        self.image = None
