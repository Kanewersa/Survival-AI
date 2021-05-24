import os

import pygame


class Image:
    def __init__(self, filename, pos=(0, 0), scale=1):
        self.texture = pygame.image.load(os.path.join('..', 'assets', filename)).convert_alpha()
        self.image = self.texture
        self.origin = (0, 0)
        self.pos = pos
        self.set_scale(scale)

    def set_scale(self, scale):
        self.image = pygame.transform.scale(self.texture,
                                            (self.texture.get_width() * scale, self.texture.get_height() * scale))
        self.scale = scale

    def draw(self, window, camera):
        window.blit(self.image, camera.apply(self.pos),
                    pygame.Rect(self.origin[0] * self.scale, self.origin[1] * self.scale, 32 * self.scale,
                                32 * self.scale))

    def draw_static(self, window):
        window.blit(self.image, self.pos,
                    pygame.Rect(self.origin[0] * self.scale, self.origin[1] * self.scale, 32 * self.scale,
                                32 * self.scale))
