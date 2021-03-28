import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from survival import esper
from survival.camera import Camera
from survival.components.camera_target_component import CameraTargetComponent
from survival.components.input_component import InputComponent
from survival.components.movement_component import MovementComponent
from survival.components.position_component import PositionComponent
from survival.components.sprite_component import SpriteComponent
from survival.game_map import GameMap
from survival.systems.camera_system import CameraSystem
from survival.systems.collision_system import CollisionSystem
from survival.systems.draw_system import DrawSystem
from survival.systems.input_system import InputSystem
from survival.systems.movement_system import MovementSystem


def draw_game(delta):
    win.fill((0, 0, 0))
    game_map.draw(camera)
    world.process(delta)
    pygame.display.update()


if __name__ == '__main__':
    pygame.init()

    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Project")

    clock = pygame.time.Clock()

    game_map = GameMap(int(SCREEN_WIDTH / 32) * 2, 2 * int(SCREEN_HEIGHT / 32) + 1)
    camera = Camera(game_map.width * 32, game_map.height * 32, win)

    world = esper.World()
    world.add_processor(InputSystem())
    world.add_processor(CameraSystem(camera))
    world.add_processor(MovementSystem(), priority=1)
    world.add_processor(CollisionSystem(game_map), priority=2)
    world.add_processor(DrawSystem(win, camera))

    player = world.create_entity()
    pos = PositionComponent([0, 0], [0, 0])
    world.add_component(player, pos)
    world.add_component(player, MovementComponent())
    world.add_component(player, InputComponent())
    camera_target = CameraTargetComponent(pos)
    world.add_component(player, camera_target)
    game_map.add_entity(player, pos)
    sprite = SpriteComponent('stevenson.png')
    sprite.set_scale(1)
    world.add_component(player, sprite)

    apple = world.create_entity()
    pos = PositionComponent([96, 96], [3, 3])
    world.add_component(apple, pos)
    world.add_component(apple, SpriteComponent('apple.png'))
    game_map.add_entity(apple, pos)
    apple = world.create_entity()
    pos = PositionComponent([128, 128], [4, 4])
    world.add_component(apple, pos)
    world.add_component(apple, SpriteComponent('apple.png'))
    game_map.add_entity(apple, pos)

    run = True

    while run:
        # Set the framerate
        ms = clock.tick(60)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        draw_game(ms)
