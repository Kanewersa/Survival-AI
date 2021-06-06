from survival.components.position_component import PositionComponent
from survival.components.resource_component import ResourceComponent
from survival.entity_layer import EntityLayer
from survival.esper import World
from survival.graph_search import graph_search
from survival.settings import AGENT_VISION_RANGE
from survival.tile_layer import TileLayer


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_layer = TileLayer(width, height)
        self.entity_layer = EntityLayer(width, height)

    def draw(self, camera):
        visible_area = camera.get_visible_area()
        self.tile_layer.draw(camera, visible_area)

    def add_entity(self, entity, pos):
        self.entity_layer.add_entity(entity, pos.grid_position)

    def move_entity(self, from_pos, to_pos):
        self.entity_layer.move_entity(from_pos, to_pos)

    def remove_entity(self, pos):
        self.entity_layer.remove_entity(pos)

    def get_entity(self, pos) -> int:
        if not self.in_bounds(pos):
            return None
        return self.entity_layer.get_entity(pos)

    def is_colliding(self, pos):
        return not self.in_bounds(pos) or self.entity_layer.is_colliding(pos)

    def in_bounds(self, pos):
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def get_cost(self, pos):
        return self.tile_layer.get_cost(pos)

    def find_nearby_resources(self, world: World, player: int, position: PositionComponent, search_range: int = 5):
        entity_position = position.grid_position

        x_range = [entity_position[0] - search_range, entity_position[0] + search_range]
        y_range = [entity_position[1] - search_range, entity_position[1] + search_range]

        # Check if range is not out of map bounds
        if x_range[0] < 0:
            x_range[0] = 0
        if x_range[1] >= self.width:
            x_range[1] = self.width - 1
        if y_range[0] < 0:
            y_range[0] = 0
        if y_range[1] >= self.height:
            y_range[1] = self.height - 1

        found_resources = []

        for y in range(y_range[0], y_range[1]):
            for x in range(x_range[0], x_range[1]):
                ent = self.get_entity([x, y])
                if ent == player:
                    continue
                if ent is not None and world.has_component(ent, ResourceComponent):
                    res_position = world.component_for_entity(ent, PositionComponent).grid_position
                    path, cost = graph_search(self, position, tuple(res_position), world)
                    found_resources.append([ent, path, cost])

        return found_resources

    def find_nearest_resource(self, world: World, player: int, position: PositionComponent):
        resources = self.find_nearby_resources(world, player, position, AGENT_VISION_RANGE)

        nearest = None
        for resource in resources:
            if nearest is None or resource[2] < nearest[2]:
                nearest = resource

        return nearest
