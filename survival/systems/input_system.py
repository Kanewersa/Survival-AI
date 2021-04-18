import pygame

from survival import esper
from survival.components.input_component import InputComponent
from survival.components.moving_component import MovingComponent
from survival.components.position_component import PositionComponent
from survival.enums import Direction


class InputSystem(esper.Processor):
    def __init__(self):
        self.map = None

    def process(self, dt):
        for ent, (inp, pos) in self.world.get_components(InputComponent, PositionComponent):
            keys = pygame.key.get_pressed()

            if self.world.has_component(ent, MovingComponent):
                continue
            if keys[pygame.K_LEFT]:
                pos.direction = Direction.rotate_left(pos.direction)
            elif keys[pygame.K_RIGHT]:
                pos.direction = Direction.rotate_right(pos.direction)
            elif keys[pygame.K_UP]:
                self.world.add_component(ent, MovingComponent())
