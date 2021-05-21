from survival.components.collision_component import CollisionComponent
from survival.components.inventory_component import InventoryComponent
from survival.components.position_component import PositionComponent
from survival.components.sprite_component import SpriteComponent


class BuildingGenerator:
    def create_home(self, world, game_map):
        home = world.create_entity()
        pos = PositionComponent([32, 32], [32, 32])
        world.add_component(home, pos)
        world.add_component(home, InventoryComponent())

        game_map.add_entity(home, pos)
        sprite = SpriteComponent('tree.png')
        sprite.set_scale(2)
        world.add_component(home, sprite)
        world.add_component(home, CollisionComponent())
