from survival import esper
from survival.components.movement_component import MovementComponent
from survival.components.moving_component import MovingComponent
from survival.components.position_component import PositionComponent
from survival.components.sprite_component import SpriteComponent


class MovementSystem(esper.Processor):
    def __init__(self):
        self.map = None

    def process(self, dt):
        for ent, (mov, pos, moving, sprite) in self.world.get_components(MovementComponent, PositionComponent,
                                                                         MovingComponent,
                                                                         SpriteComponent):

            pos.position[0] += moving.direction_vector[0] * mov.speed * dt / 100
            pos.position[1] += moving.direction_vector[1] * mov.speed * dt / 100

            if abs(moving.target[0] * 32 - pos.position[0]) < 0.1 * mov.speed and abs(
                    pos.position[1] - moving.target[1] * 32) < 0.1 * mov.speed:
                pos.position = [moving.target[0] * 32, moving.target[1] * 32]
                self.world.remove_component(ent, MovingComponent)

            # if moving.direction[0] != 0:
            #     pos.position[0] += moving.direction[0] * mov.speed * dt / 100
            #     if abs(moving.movement_target[0] * 32 - pos.position[0]) < 0.1 * mov.speed:
            #         pos.position = [moving.movement_target[0] * 32, moving.movement_target[1] * 32]
            #         self.world.remove_component(ent, MovingComponent)
            # else:
            #     pos.position[1] += moving.direction[1] * mov.speed * dt / 100
            #     if abs(pos.position[1] - moving.movement_target[1] * 32) < 0.1 * mov.speed:
            #         pos.position = [moving.movement_target[0] * 32, moving.movement_target[1] * 32]
            #         self.world.remove_component(ent, MovingComponent)
