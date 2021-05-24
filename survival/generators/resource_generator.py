import random

from survival import GameMap
from survival.components.OnCollisionComponent import OnCollisionComponent
from survival.components.inventory_component import InventoryComponent
from survival.components.position_component import PositionComponent
from survival.components.resource_component import ResourceComponent
from survival.components.sprite_component import SpriteComponent
from survival.decision_tree import DecisionTree
from survival.esper import World
from survival.generators.resource_type import ResourceType
from survival.settings import RESOURCES_AMOUNT


class ResourceGenerator:
    def __init__(self, world, game_map):
        self.world = world
        self.map = game_map
        self.decision_tree = DecisionTree()
        self.built_tree = self.decision_tree.build(10)

    def generate_resources(self, player: int):
        for x in range(RESOURCES_AMOUNT):
            obj = self.world.create_entity()
            sprites = {
                ResourceType.FOOD: 'apple.png',
                ResourceType.WATER: 'water.png',
                ResourceType.WOOD: 'wood.png'
            }

            empty_grid_pos = self.get_empty_grid_position()
            empty_pos = [empty_grid_pos[0] * 32, empty_grid_pos[1] * 32]
            pos = PositionComponent(empty_pos, empty_grid_pos)
            resource_type = random.choice(list(ResourceType))
            sprite = SpriteComponent(sprites[resource_type])
            col = OnCollisionComponent()
            col.addCallback(self.remove_resource, world=self.world, game_map=self.map, resource_ent=obj, player=player, decision_tree=self.decision_tree)
            self.world.add_component(obj, pos)
            self.world.add_component(obj, sprite)
            self.world.add_component(obj, col)
            self.world.add_component(obj, ResourceComponent(resource_type))
            self.map.add_entity(obj, pos)

    def get_empty_grid_position(self):
        free_pos = [random.randrange(self.map.width), random.randrange(self.map.height)]
        while self.map.is_colliding(free_pos):
            free_pos = [random.randrange(self.map.width), random.randrange(self.map.height)]
        return free_pos

    @staticmethod
    def remove_resource(world: World, game_map: GameMap, resource_ent: int, player: int, decision_tree: DecisionTree):
        pos = world.component_for_entity(resource_ent, PositionComponent)
        resource = world.component_for_entity(resource_ent, ResourceComponent)
        inventory = world.component_for_entity(player, InventoryComponent)
        answer = decision_tree.predict_answer(resource)
        # print(answer)
        inventory.add_item(ResourceType.get_from_string(answer), 1)
        game_map.remove_entity(pos.grid_position)
        world.delete_entity(resource_ent, immediate=True)
