from survival import esper
from survival.components.moving_component import MovingComponent
from survival.components.position_component import PositionComponent


class CollisionSystem(esper.Processor):
    def __init__(self, game_map):
        self.map = game_map

    def process(self, dt):
        for ent, (pos, moving) in self.world.get_components(PositionComponent, MovingComponent):
            if moving.checked_collision:
                continue

            moving.checked_collision = True

            if self.check_collision(moving.movement_target):
                self.world.remove_component(ent, MovingComponent)

            else:
                self.map.move_entity(pos.grid_position, moving.movement_target)
                pos.grid_position = moving.movement_target

    def check_collision(self, pos):
        return self.map.is_colliding(pos)
