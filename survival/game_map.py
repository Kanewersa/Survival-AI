from survival.components.position_component import PositionComponent
from survival.entity_layer import EntityLayer
from survival.player import Player
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

    def is_colliding(self, pos):
        return self.entity_layer.is_colliding(pos)
