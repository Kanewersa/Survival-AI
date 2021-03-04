import os

import pygame

from game.game_object import GameObject


class Player(GameObject):
    def __init__(self):
        super().__init__([0, 0], os.path.join('..', 'assets', 'player.png'))

    def draw(self, window):
        super().draw(window)

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            self.velocity[0] = -1
        elif pressed_keys[pygame.K_RIGHT]:
            self.velocity[0] = 1
        else:
            self.velocity[0] = 0

        if pressed_keys[pygame.K_DOWN]:
            self.velocity[1] = 1
        elif pressed_keys[pygame.K_UP]:
            self.velocity[1] = -1
        else:
            self.velocity[1] = 0

        self.last_pos = [self.pos[0], self.pos[1]]

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

