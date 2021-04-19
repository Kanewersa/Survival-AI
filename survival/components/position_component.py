from survival.enums import Direction
from survival.settings import DIRECTION_CHANGE_DELAY


class PositionComponent:
    def __init__(self, pos, grid_pos):
        self.position = pos
        self.grid_position = grid_pos
        self.direction = Direction.DOWN
        self.direction_change_timer = DIRECTION_CHANGE_DELAY

    def rotate_left(self):
        return Direction.rotate_left(self.direction)

    def rotate_right(self):
        return Direction.rotate_right(self.direction)
