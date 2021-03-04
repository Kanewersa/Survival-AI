import pygame
from pygame.rect import Rect


class QuadTree:
    """
    How to use:

    1) Create new quadtree: QuadTree(0, Rect(0, 0, width, height))
    2) Every frame clear the quadtree and insert all objects into it.
    3) Get the possible colliders for each objects and check if they collide.

    for object in objects:
        possible_colliders = []
        possible_colliders = quad_tree.retrieve(possible_colliders, object)

        for collider in possible_colliders:
            # Check collision here

    """
    MAX_OBJECTS = 10
    MAX_LEVELS = 5

    def __init__(self, level, bounds):
        self.level = level
        self.bounds = bounds
        self.objects = []
        self.nodes = []

    def clear(self):
        """
        Clears the quadtree recursively.
        """
        self.objects.clear()

        for node in self.nodes:
            if node is not None:
                node.clear()

    def split(self):
        """
        Splits the node into 4 sub nodes.
        """
        sub_width = int(self.bounds.width / 2)
        sub_height = int(self.bounds.height / 2)
        x = int(self.bounds.x)
        y = int(self.bounds.y)

        self.nodes.append(QuadTree(self.level + 1, Rect(x + sub_width, y, sub_width, sub_height)))
        self.nodes.append(QuadTree(self.level + 1, Rect(x, y, sub_width, sub_height)))
        self.nodes.append(QuadTree(self.level + 1, Rect(x, y + sub_height, sub_width, sub_height)))
        self.nodes.append(QuadTree(self.level + 1, Rect(x + sub_width, y + sub_height, sub_width, sub_height)))

    def get_index(self, rect):
        """
        Checks which node the object belongs to.
        """
        index = -1
        vertical_point = self.bounds.x + (self.bounds.width / 2)
        horizontal_point = self.bounds.y + (self.bounds.height / 2)

        top_quadrant = rect.y < horizontal_point and rect.y + rect.height < horizontal_point
        bot_quadrant = rect.y > horizontal_point

        if rect.x < vertical_point and rect.x + rect.width < vertical_point:
            if top_quadrant:
                index = 1
            elif bot_quadrant:
                index = 2
        elif rect.x > vertical_point:
            if top_quadrant:
                index = 0
            elif bot_quadrant:
                index = 3

        return index

    def insert(self, game_object):
        """
        Inserts given game object into the quadtree.
        If objects count exceeds the limit the node is split and
        all objects are added to their corresponding nodes.
        """
        rect = Rect(game_object.pos[0], game_object.pos[1], game_object.width, game_object.height)
        if len(self.nodes) > 0:
            index = self.get_index(rect)

            if index != -1:
                self.nodes[index].insert(rect)
                return

        self.objects.append(game_object)

        if len(self.objects) > self.MAX_OBJECTS and self.level < self.MAX_LEVELS:
            if len(self.nodes) == 0:
                self.split()

            i = 0
            while i < len(self.objects):
                index = self.get_index(self.objects[i])
                if index == -1:
                    i += 1
                else:
                    self.nodes[index].insert(self.objects.remove(i))

    def retrieve(self, objects, game_object):
        """
        Returns all objects that collide with given rectangle.
        """
        rect = game_object.get_rect()
        index = self.get_index(rect)

        if index != -1 and len(self.nodes) > 0:
            self.nodes[index].retrieve(objects, rect)

        objects.extend(self.objects)
