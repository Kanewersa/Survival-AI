import operator

from survival import esper
from survival.components.OnCollisionComponent import OnCollisionComponent
from survival.components.moving_component import MovingComponent
from survival.components.position_component import PositionComponent
from survival.enums import Direction


class CollisionSystem(esper.Processor):
    def __init__(self, game_map):
        self.map = game_map

    def process(self, dt):
        for ent, (pos, moving, onCol) in self.world.get_components(PositionComponent, MovingComponent, OnCollisionComponent):
            if moving.target is not None:
                continue

            moving.checked_collision = True

            vector = Direction.get_vector(pos.direction)
            moving.target = tuple(map(operator.add, vector, pos.grid_position))
            moving.direction_vector = vector
            if self.check_collision(moving.target):
                self.world.remove_component(ent, MovingComponent)
                onCol.callAll()
                colliding_object : int = self.map.get_entity(moving.target)
                if self.world.has_component(colliding_object, OnCollisionComponent):
                    self.world.component_for_entity(colliding_object, OnCollisionComponent).callAll()

            else:
                self.map.move_entity(pos.grid_position, moving.target)
                pos.grid_position = moving.target

    def check_collision(self, pos):
        return self.map.is_colliding(pos)
