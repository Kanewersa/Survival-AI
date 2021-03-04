import pygame
from random import randrange


class Tile:
    def __init__(self):
        self.background_id = randrange(4)
