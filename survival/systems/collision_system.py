import operator

from survival import esper
from survival.components.moving_component import MovingComponent
from survival.components.position_component import PositionComponent
from survival.enums import Direction


class CollisionSystem(esper.Processor):
    def __init__(self, game_map):
        self.map = game_map

    def process(self, dt):
        for ent, (pos, moving) in self.world.get_components(PositionComponent, MovingComponent):
            if moving.target is not None:
                continue

            moving.checked_collision = True

            vector = Direction.get_vector(pos.direction)
            moving.target = tuple(map(operator.add, vector, pos.grid_position))
            moving.direction_vector = vector
            if self.check_collision(moving.target):
                self.world.remove_component(ent, MovingComponent)
            else:
                self.map.move_entity(pos.grid_position, moving.target)
                pos.grid_position = moving.target

    def check_collision(self, pos):
        return self.map.is_colliding(pos)
