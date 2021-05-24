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

if __name__ == '__main__':
    pygame.init()

    pygame.font.init()

    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Project")

    clock = pygame.time.Clock()

    game_map = GameMap(int(SCREEN_WIDTH / 32) * 2, 2 * int(SCREEN_HEIGHT / 32) + 1)
    camera = Camera(game_map.width * 32, game_map.height * 32, win)

    world = WorldGenerator().create_world(camera, game_map)
    player = PlayerGenerator().create_player(world, game_map)
    world.get_processor(DrawSystem).initialize_interface(world.component_for_entity(player, InventoryComponent))
    building = BuildingGenerator().create_home(world, game_map)

    ResourceGenerator(world, game_map).generate_resources(player)

    run = True

    while run:
        # Set the framerate
        ms = clock.tick(60)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        win.fill((0, 0, 0))
        game_map.draw(camera)
        world.process(ms)
        pygame.display.update()
