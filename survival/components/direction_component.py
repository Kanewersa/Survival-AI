from survival.enums import Direction


class DirectionChangeComponent:
    def __init__(self, direction):
        self.direction = direction

    def rotate_left(self):
        self.direction = Direction.rotate_left(self.direction)

    def rotate_right(self):
        self.direction = Direction.rotate_right(self.direction)
