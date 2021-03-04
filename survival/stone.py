import os

from survival.game_object import GameObject


class Stone(GameObject):

    def __init__(self, pos):
        super().__init__(pos, os.path.join('..', 'assets', 'stone.png'))
