from survival.components.collision_component import CollisionComponent
from survival.components.inventory_component import InventoryComponent
from survival.components.position_component import PositionComponent
from survival.components.sprite_component import SpriteComponent


class BuildingGenerator:
    def create_home(self, world, game_map, position = [10,10]):
        home = world.create_entity()
        home_pos = PositionComponent([position[0]*32, position[1]*32], position)
        world.add_component(home, home_pos)
        game_map.add_entity(home, home_pos)
        world.add_component(home, InventoryComponent())
        sprite = SpriteComponent('home.png')
        world.add_component(home, sprite)
        world.add_component(home, CollisionComponent())

        for x_pos in [-1, 1]:
            chest = world.create_entity()
            chest_pos = PositionComponent(
                [(position[0]+x_pos)*32, position[1]*32],
                [position[0]+x_pos, position[1]]
            )
            world.add_component(chest, chest_pos)
            game_map.add_entity(chest, chest_pos)
            world.add_component(chest, InventoryComponent())
            sprite = SpriteComponent('chest.png')
            world.add_component(chest, sprite)
            world.add_component(chest, CollisionComponent())
