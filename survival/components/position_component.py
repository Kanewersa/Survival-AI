from survival.enums import Direction


class PositionComponent:
    def __init__(self, pos, grid_pos):
        self.position = pos
        self.grid_position = grid_pos
        self.direction = Direction.DOWN
