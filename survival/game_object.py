import pygame
from pygame.rect import Rect


class GameObject:

    def __init__(self, pos, texture):
        self.pos = pos
        self.last_pos = pos
        self.texture = pygame.image.load(texture)
        self.texture = pygame.transform.scale(self.texture, (64, 64))
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        self.velocity = [0, 0]

    def draw(self, window):
        window.blit(self.texture, self.pos)

    def get_rect(self):
        return Rect(self.pos[0], self.pos[1], self.width, self.height)
