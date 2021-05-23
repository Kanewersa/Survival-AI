import random

from survival import GameMap
from survival.components.OnCollisionComponent import OnCollisionComponent
from survival.components.position_component import PositionComponent
from survival.components.sprite_component import SpriteComponent
from survival.esper import World
from survival.settings import RESOURCES_AMOUNT


class ResourceGenerator:
    def __init__(self, world, game_map):
        self.world = world
        self.map = game_map

    def generate_resources(self):
        for x in range(RESOURCES_AMOUNT):
            obj = self.world.create_entity()
            sprites = ['apple.png', 'water.png', 'wood.png']

            empty_grid_pos = self.get_empty_grid_position()
            empty_pos = [empty_grid_pos[0] * 32, empty_grid_pos[1] * 32]

            pos = PositionComponent(empty_pos, empty_grid_pos)
            sprite = SpriteComponent(random.choice(sprites))
            col = OnCollisionComponent()
            col.addCallback(self.remove_resource, world=self.world, game_map=self.map, entity=obj)
            self.world.add_component(obj, pos)
            self.world.add_component(obj, sprite)
            self.world.add_component(obj, col)
            self.map.add_entity(obj, pos)

    def get_empty_grid_position(self):
        free_pos = [random.randrange(self.map.width), random.randrange(self.map.height)]
        while self.map.is_colliding(free_pos):
            free_pos = [random.randrange(self.map.width), random.randrange(self.map.height)]
        return free_pos

    @staticmethod
    def remove_resource(world: World, game_map: GameMap, entity: int):
        pos = world.component_for_entity(entity, PositionComponent)
        game_map.remove_entity(pos.grid_position)
        world.delete_entity(entity, immediate=True)
