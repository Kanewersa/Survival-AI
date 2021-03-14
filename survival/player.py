import os

import pygame

from survival.game_object import GameObject


class Player(GameObject):
    def __init__(self):
        super().__init__([0, 0], os.path.join('..', 'assets', 'player.png'))
        self.speed = 3
        self.movement_target = [self.pos[0], self.pos[1]]

    def draw(self, window):
        super().draw(window)

    def is_moving(self):
        return self.pos != self.movement_target

    def update(self, delta, pressed_keys):
        if self.is_moving():
            if self.velocity[0] != 0:
                self.pos[0] += self.velocity[0] * self.speed * delta / 100
                if abs(self.movement_target[0] - self.pos[0]) < 0.1 * self.speed:
                    self.velocity = [0, 0]
                    self.pos = self.movement_target
            else:
                self.pos[1] += self.velocity[1] * self.speed * delta / 100
                if abs(self.pos[1] - self.movement_target[1]) < 0.1 * self.speed:
                    self.velocity = [0, 0]
                    self.pos = self.movement_target
            return

        if pressed_keys[pygame.K_LEFT]:
            self.velocity = [-1, 0]
            self.movement_target = [self.pos[0] - 32, self.pos[1]]
        elif pressed_keys[pygame.K_RIGHT]:
            self.velocity = [1, 0]
            self.movement_target = [self.pos[0] + 32, self.pos[1]]
        elif pressed_keys[pygame.K_DOWN]:
            self.velocity = [0, 1]
            self.movement_target = [self.pos[0], self.pos[1] + 32]
        elif pressed_keys[pygame.K_UP]:
            self.velocity = [0, -1]
            self.movement_target = [self.pos[0], self.pos[1] - 32]

