from pygame.rect import Rect

from survival.player import Player
from survival.quad_tree import QuadTree
from survival.stone import Stone
from survival.tile_layer import TileLayer


class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.game_objects = []
        self.player = Player()
        self.game_objects.append(self.player)
        self.tiles_layer = TileLayer(width, height)
        self.game_objects.append(Stone([100, 200]))
        self.quad_tree = QuadTree(0, Rect(0, 0, width * 32, height * 32))

    def draw(self, window):
        self.tiles_layer.draw(window)

        for game_object in self.game_objects:
            game_object.draw(window)

    def update(self, pressed_keys):
        self.quad_tree.clear()

        for game_object in self.game_objects:
            self.quad_tree.insert(game_object)

        self.player.update(pressed_keys)

        for game_object in self.game_objects:
            possible_colliders = []
            self.quad_tree.retrieve(possible_colliders, game_object)
            for collider in possible_colliders:
                if game_object.get_rect().colliderect(collider.get_rect()) and game_object != collider:
                    game_object.velocity = [0, 0]
                    game_object.pos = game_object.last_pos
