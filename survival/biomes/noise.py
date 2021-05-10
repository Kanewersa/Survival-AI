from perlin_noise import PerlinNoise


def generate_noise(width: int, height: int, octaves, seed):
    noise_map = PerlinNoise(octaves=octaves, seed=seed)
    return [[noise_map([x / width, y / height]) for y in range(width)] for x in range(height)]
