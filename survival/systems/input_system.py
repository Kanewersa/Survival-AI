import pygame

from survival import esper
from survival.components.direction_component import DirectionChangeComponent
from survival.components.input_component import InputComponent
from survival.components.moving_component import MovingComponent
from survival.components.pathfinding_component import PathfindingComponent
from survival.components.position_component import PositionComponent


class InputSystem(esper.Processor):
    def __init__(self, camera):
        self.camera = camera

    def process(self, dt):
        for ent, (inp, pos) in self.world.get_components(InputComponent, PositionComponent):
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed(3)
            if mouse[0] == 1:
                pos = pygame.mouse.get_pos()
                pos = (pos[0] - self.camera.camera.left, pos[1] - self.camera.camera.top)
                if not self.world.has_component(ent, PathfindingComponent):
                    self.world.add_component(ent, PathfindingComponent(pos))

            if self.world.has_component(ent, MovingComponent):
                continue
            if keys[pygame.K_LEFT]:
                if not self.world.has_component(ent, DirectionChangeComponent):
                    self.world.add_component(ent, DirectionChangeComponent(pos.rotate_left()))
            elif keys[pygame.K_RIGHT]:
                if not self.world.has_component(ent, DirectionChangeComponent):
                    self.world.add_component(ent, DirectionChangeComponent(pos.rotate_right()))
            elif keys[pygame.K_UP]:
                self.world.add_component(ent, MovingComponent())
