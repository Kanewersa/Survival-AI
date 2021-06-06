import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from survival.camera import Camera
from survival.components.inventory_component import InventoryComponent
from survival.game_map import GameMap
from survival.generators.building_generator import BuildingGenerator
from survival.generators.player_generator import PlayerGenerator
from survival.generators.resource_generator import ResourceGenerator
from survival.generators.world_generator import WorldGenerator
from survival.systems.draw_system import DrawSystem


class Game:
    def __init__(self):
        self.world_generator = WorldGenerator(win, self.reset)
        self.game_map, self.world, self.camera = self.world_generator.create_world()
        self.run = True

    def reset(self):
        self.world_generator.reset_world()

    def update(self, ms):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.run = False
            if pygame.key.get_pressed()[pygame.K_DELETE]:
                self.reset()

        win.fill((0, 0, 0))
        self.game_map.draw(self.camera)
        self.world.process(ms)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()

    pygame.font.init()

    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Project")

    clock = pygame.time.Clock()
    game = Game()

    while game.run:
        game.update(clock.tick(60))
