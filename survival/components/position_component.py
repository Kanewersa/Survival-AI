from survival.enums import Direction


class PositionComponent:
    def __init__(self, pos, grid_pos, direction=Direction.DOWN):
        self.position = pos
        self.grid_position = grid_pos
        self.direction = direction
        self.direction_change_timer = 0

    def rotate_left(self):
        return Direction.rotate_left(self.direction)

    def rotate_right(self):
        return Direction.rotate_right(self.direction)
