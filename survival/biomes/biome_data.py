from survival.biomes.biome_preset import BiomePreset


class BiomeData:
    def __init__(self, preset: BiomePreset):
        self.biome = preset

    def get_diff_value(self, height: float, moisture: float, heat: float):
        return (height - self.biome.min_height) + (moisture - self.biome.min_moisture) + (heat - self.biome.min_heat)
