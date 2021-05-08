import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from survival.camera import Camera
from survival.game_map import GameMap
from survival.player_generator import PlayerGenerator
from survival.resource_generator import ResourceGenerator
from survival.world_generator import WorldGenerator

if __name__ == '__main__':
    pygame.init()

    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Project")

    clock = pygame.time.Clock()

    game_map = GameMap(int(SCREEN_WIDTH / 32) * 2, 2 * int(SCREEN_HEIGHT / 32) + 1)
    camera = Camera(game_map.width * 32, game_map.height * 32, win)

    world = WorldGenerator().create_world(camera, game_map)
    player = PlayerGenerator().create_player(world, game_map)

    ResourceGenerator(world, game_map).generate_resources()

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
