import pygame


class TextureAtlas(object):
    def __init__(self, filename):
        self.atlas = pygame.image.load(filename).convert()

    def image_at(self, rectangle, color_key=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.atlas, (0, 0), rect)
        if color_key is not None:
            if color_key is -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)
        return image

    def images_at(self, rects, color_key=None):
        return [self.image_at(rect, color_key) for rect in rects]

    def load_row(self, rect, image_count, color_key=None):
        images = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                  for x in range(image_count)]
        return self.images_at(images, color_key)
