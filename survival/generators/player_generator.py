from survival.components.camera_target_component import CameraTargetComponent
from survival.components.input_component import InputComponent
from survival.components.movement_component import MovementComponent
from survival.components.position_component import PositionComponent
from survival.components.sprite_component import SpriteComponent
from survival.components.time_component import TimeComponent


class PlayerGenerator:

    def create_player(self, world, game_map):
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
        world.add_component(player, TimeComponent(0, 0, 0, 0))

        return player
