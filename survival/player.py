from random import randint

import pygame


class Player:
    def __init__(self):
        # self.pos = [1024, 512]
        # self.velocity = [0, 0]
        # self.image = Image('stevenson.png')
        # self.image.set_scale(2)
        # self.speed = 30
        # self.movement_target = [self.pos[0], self.pos[1]]
        # self.timer = 0
        pass

    def draw(self, camera):

        self.image.pos = self.pos
        camera.draw(self.image)

    def is_moving(self):
        return self.pos != self.movement_target

    def move_in_random_direction(self):
        value = randint(0, 3)
        random_movement = {
            0: self.move_up,
            1: self.move_down,
            2: self.move_left,
            3: self.move_right
        }
        random_movement[value]()

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

        self.timer += delta

        if self.timer > 1000:
            self.move_in_random_direction()
            self.timer = 0

        if pressed_keys[pygame.K_LEFT]:
            self.move_left()
        elif pressed_keys[pygame.K_RIGHT]:
            self.move_right()
        elif pressed_keys[pygame.K_DOWN]:
            self.move_down()
        elif pressed_keys[pygame.K_UP]:
            self.move_up()

    def move_left(self):
        self.velocity = [-1, 0]
        self.movement_target = [self.pos[0] - 32, self.pos[1]]

    def move_right(self):
        self.velocity = [1, 0]
        self.movement_target = [self.pos[0] + 32, self.pos[1]]

    def move_up(self):
        self.velocity = [0, -1]
        self.movement_target = [self.pos[0], self.pos[1] - 32]

    def move_down(self):
        self.velocity = [0, 1]
        self.movement_target = [self.pos[0], self.pos[1] + 32]
