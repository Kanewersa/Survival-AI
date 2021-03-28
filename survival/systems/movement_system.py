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
            if moving.direction[0] != 0:
                pos.position[0] += moving.direction[0] * mov.speed * dt / 100
                if abs(moving.movement_target[0] * 32 - pos.position[0]) < 0.1 * mov.speed:
                    pos.position = [moving.movement_target[0] * 32, moving.movement_target[1] * 32]
                    self.world.remove_component(ent, MovingComponent)
            else:
                pos.position[1] += moving.direction[1] * mov.speed * dt / 100
                if abs(pos.position[1] - moving.movement_target[1] * 32) < 0.1 * mov.speed:
                    pos.position = [moving.movement_target[0] * 32, moving.movement_target[1] * 32]
                    self.world.remove_component(ent, MovingComponent)

            if moving.direction[0] == 1:
                sprite.image.origin = (96, 0)
            elif moving.direction[0] == -1:
                sprite.image.origin = (64, 0)
            elif moving.direction[1] == 1:
                sprite.image.origin = (0, 0)
            else:
                sprite.image.origin = (32, 0)

