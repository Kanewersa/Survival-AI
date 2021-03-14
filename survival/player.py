import os

import pygame

from survival.image import Image


class Player:
    def __init__(self):
        self.pos = [0, 0]
        self.velocity = [0, 0]
        self.image = Image('stevenson.png')
        self.image.set_scale(2)
        self.origin = (0, 0)
        self.speed = 3
        self.movement_target = [self.pos[0], self.pos[1]]

    def draw(self, window):
        if self.is_moving():
            if self.velocity[0] == 1:
                self.image.origin = (96, 0)
            elif self.velocity[0] == -1:
                self.image.origin = (64, 0)
            elif self.velocity[1] == 1:
                self.image.origin = (0, 0)
            else:
                self.image.origin = (32, 0)
        self.image.pos = self.pos
        self.image.draw(window)

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

