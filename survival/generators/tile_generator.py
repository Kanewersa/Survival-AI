import json
import random
from pathlib import Path
from typing import List

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
        "Sand": Tile(origin=(64, 64), cost=20),
        "Puddle": Tile(origin=(96, 64), cost=20),
        "DarkGrass": Tile(origin=(64, 96), cost=2),
        "Water": Tile(origin=(96, 96), cost=3),
        "Ice": Tile(origin=(0, 96), cost=2),
        "Ice2": Tile(origin=(32, 96), cost=2),
    }

    TilesValues = list(Tiles.values())

    Biomes = [
        BiomePreset("Desert", min_height=0.2, min_moisture=0, min_heat=0.5, tiles=[Tiles["Grass1"], Tiles["Grass2"],
                                                                                   Tiles["Grass3"], Tiles["Grass4"]]),
        BiomePreset("Forest", min_height=0.2, min_moisture=0.4, min_heat=0.4, tiles=[Tiles["DarkGrass"]]),
        BiomePreset("Grassland", min_height=0.2, min_moisture=0.5, min_heat=0.3, tiles=[Tiles["Sand"]]),
        BiomePreset("Marsh", min_height=0.3, min_moisture=0.5, min_heat=0.62, tiles=[Tiles["Puddle"]]),
        BiomePreset("Ocean", min_height=0, min_moisture=0, min_heat=0, tiles=[Tiles["Water"]]),
        BiomePreset("Tundra", min_height=0.2, min_moisture=0, min_heat=0, tiles=[Tiles["Ice"], Tiles["Ice2"]])
    ]

    @staticmethod
    def get_random_tile():
        tile = random.choice(TileGenerator.TilesValues)
        return Tile(origin=tile.origin, cost=tile.cost)

    @staticmethod
    def generate_random_tiles(width: int, height: int) -> List[List[Tile]]:
        return [[TileGenerator.get_random_tile() for _ in range(width)] for _ in range(height)]

    @staticmethod
    def generate_biome_tiles(width: int, height: int):
        seed = random.randint(1, 10)
        octaves = 10
        file_name = f'seeds/{seed}.bin'
        biomes_file = Path(file_name)
        if biomes_file.is_file():
            with open(file_name, 'r') as f:
                data = json.load(f)
                height_map = data[0]
                moisture_map = data[1]
                heat_map = data[2]
        else:
            height_map = generate_noise(width, height, octaves, seed)
            moisture_map = generate_noise(width, height, octaves, seed)
            heat_map = generate_noise(width, height, octaves, seed)
            data = [height_map, moisture_map, heat_map]
            Path('seeds').mkdir(exist_ok=True)
            with open(file_name, 'w') as f:
                json.dump(data, f)

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
