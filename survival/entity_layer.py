class EntityLayer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[None for x in range(self.width)] for y in range(self.height)]

    def draw(self, camera, visible_area):
        pass

    def add_entity(self, entity, pos):
        self.tiles[pos[1]][pos[0]] = entity

    def move_entity(self, from_pos, to_pos):
        ent = self.tiles[from_pos[1]][from_pos[0]]
        self.tiles[from_pos[1]][from_pos[0]] = None
        self.tiles[to_pos[1]][to_pos[0]] = ent

    def remove_entity(self, pos):
        self.tiles[pos[1]][pos[0]] = None

    def is_colliding(self, pos):
        return self.tiles[pos[1]][pos[0]] is not None
