from survival.components.OnCollisionComponent import OnCollisionComponent
from survival.components.camera_target_component import CameraTargetComponent
from survival.components.consumption_component import ConsumptionComponent
from survival.components.input_component import InputComponent
from survival.components.inventory_component import InventoryComponent
from survival.components.learning_component import LearningComponent
from survival.components.movement_component import MovementComponent
from survival.components.position_component import PositionComponent
from survival.components.sprite_component import SpriteComponent
from survival.components.time_component import TimeComponent
from survival.components.vision_component import VisionComponent
from survival.generators.resource_type import ResourceType
from survival.settings import PLAYER_START_POSITION, STARTING_RESOURCES_AMOUNT


class PlayerGenerator:
    def create_player(self, world, game_map):
        player = world.create_entity()
        pos = PositionComponent([PLAYER_START_POSITION[0] * 32, PLAYER_START_POSITION[1] * 32],
                                PLAYER_START_POSITION)
        world.add_component(player, pos)
        world.add_component(player, MovementComponent())
        world.add_component(player, InputComponent())
        world.add_component(player, OnCollisionComponent())
        inv = InventoryComponent()
        for resource in ResourceType:
            inv.add_item(resource, STARTING_RESOURCES_AMOUNT)
        world.add_component(player, ConsumptionComponent(inv.total_items_count()))
        world.add_component(player, inv)
        camera_target = CameraTargetComponent(pos)
        world.add_component(player, camera_target)
        # world.add_component(player, AutomationComponent())
        game_map.add_entity(player, pos)
        sprite = SpriteComponent('stevenson.png')
        sprite.set_scale(1)
        world.add_component(player, sprite)
        world.add_component(player, TimeComponent())
        world.add_component(player, VisionComponent())
        world.add_component(player, LearningComponent())

        return player
