class Tile:
    def __init__(self, origin: tuple = (0, 0), cost: int = 1, biome=None):
        self.origin = origin
        self.cost = cost
        self.biome = biome
        self.image = None
