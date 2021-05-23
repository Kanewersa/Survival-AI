import random

from survival.biomes.biome_data import BiomeData
from survival.biomes.biome_preset import BiomePreset
from survival.biomes.noise import generate_noise
from survival.tile import Tile


class TileGenerator:
    Tiles = {
        "Grass1": Tile(origin=(0, 0), cost=1),
        "Grass2": Tile(origin=(32, 0), cost=1),
        "Grass3": Tile(origin=(64, 0), cost=1),
        "Grass4": Tile(origin=(96, 0), cost=1),
        "Sand": Tile(origin=(64, 64), cost=4),
        "Puddle": Tile(origin=(96, 64), cost=5),
    }

    TilesValues = list(Tiles.values())

    Biomes = [
        BiomePreset("Desert", min_height=0.2, min_moisture=0, min_heat=0.5, tiles=[Tiles["Grass1"], Tiles["Grass2"],
                                                                                   Tiles["Grass3"], Tiles["Grass4"]]),
        BiomePreset("Forest", min_height=0.2, min_moisture=0.4, min_heat=0.4, tiles=[Tiles["Sand"]]),
        BiomePreset("Grassland", min_height=0.2, min_moisture=0.5, min_heat=0.3, tiles=[Tiles["Sand"]]),
        BiomePreset("Marsh", min_height=0.3, min_moisture=0.5, min_heat=0.62, tiles=[Tiles["Puddle"]]),
        BiomePreset("Ocean", min_height=0, min_moisture=0, min_heat=0, tiles=[Tiles["Sand"]]),
        BiomePreset("Tundra", min_height=0.2, min_moisture=0, min_heat=0, tiles=[Tiles["Puddle"]])
    ]

    @staticmethod
    def get_random_tile():
        tile = random.choice(TileGenerator.TilesValues)
        return Tile(origin=tile.origin, cost=tile.cost)

    @staticmethod
    def generate_random_tiles(width: int, height: int) -> list[list[Tile]]:
        return [[TileGenerator.get_random_tile() for _ in range(width)] for _ in range(height)]

    @staticmethod
    def generate_biome_tiles(width: int, height: int):
        seed = random.randint(0, 9999999)
        octaves = 10
        height_map = generate_noise(width, height, octaves, seed)
        moisture_map = generate_noise(width, height, octaves, seed)
        heat_map = generate_noise(width, height, octaves, seed)

        return [[TileGenerator.get_biome(height_map[y][x], moisture_map[y][x], heat_map[y][x]).get_new_tile() for x in
                 range(width)] for y in range(height)]

    @staticmethod
    def get_biome(height, moisture, heat) -> BiomePreset:
        matching_biomes = list()

        for biome in TileGenerator.Biomes:
            if biome.match_conditions(height, moisture, heat):
                matching_biomes.append(BiomeData(biome))

        current_value = 0
        found_biome = None

        for biome in matching_biomes:
            if found_biome is None:
                found_biome = biome.biome
                current_value = biome.get_diff_value(height, moisture, heat)
            elif biome.get_diff_value(height, moisture, heat) < current_value:
                found_biome = biome.biome
                current_value = biome.get_diff_value(height, moisture, heat)

        if found_biome is None:
            found_biome = TileGenerator.Biomes[0]

        return found_biome
