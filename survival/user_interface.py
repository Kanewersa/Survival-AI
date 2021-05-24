import pygame.font

from survival import settings
from survival.components.inventory_component import InventoryComponent
from survival.generators.resource_type import ResourceType
from survival.image import Image


class UserInterface:
    def __init__(self, window, inventory: InventoryComponent):
        self.width = settings.SCREEN_WIDTH
        self.height = settings.SCREEN_HEIGHT
        self.window = window
        self.pos = (self.width - 240, 50)
        self.scale = 2
        self.inventory = inventory
        self.images = {
            ResourceType.FOOD: Image('apple.png', self.pos, self.scale),
            ResourceType.WATER: Image('water.png', self.pos, self.scale),
            ResourceType.WOOD: Image('wood.png', self.pos, self.scale)
        }
        i = 0
        for key, value in self.images.items():
            self.images[key].pos = (self.pos[0] + i * 32 * self.scale + 8 * i, self.pos[1])
            i += 1
        self.slot_image = Image('ui.png', self.pos, scale=2)
        self.font = pygame.font.SysFont('Comic Sans MS', 20)

    def update(self):
        pass

    def draw(self):
        for key, image in self.images.items():
            items_count = self.inventory.items[key] if self.inventory.has_item(key) else 0

            self.slot_image.pos = image.pos
            self.slot_image.draw_static(self.window)
            image.draw_static(self.window)

            textsurface = self.font.render(str(items_count), False, (255, 255, 255))
            self.window.blit(textsurface, (image.pos[0] + 48, image.pos[1] + 36))

