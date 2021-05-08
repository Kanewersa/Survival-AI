from survival import esper
from survival.components.direction_component import DirectionChangeComponent
from survival.components.position_component import PositionComponent
from survival.settings import DIRECTION_CHANGE_DELAY


class DirectionSystem(esper.Processor):
    def process(self, dt):
        for ent, (pos, direction) in self.world.get_components(PositionComponent, DirectionChangeComponent):
            if pos.direction_change_timer > 0:
                pos.direction_change_timer -= dt
                continue

            dir_left = pos.rotate_left()
            dir_right = pos.rotate_right()

            pos.direction_change_timer = DIRECTION_CHANGE_DELAY

            if dir_left == direction.direction:
                pos.direction = dir_left
            elif dir_right == direction.direction:
                pos.direction = dir_right
            else:
                pos.direction = dir_left
                continue

            self.world.remove_component(ent, DirectionChangeComponent)
