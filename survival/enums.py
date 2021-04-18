from enum import IntEnum


class Direction(IntEnum):
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3

    @staticmethod
    def rotate_left(direction):
        return Direction((direction - 1) % 4)

    @staticmethod
    def rotate_right(direction):
        return Direction((direction + 1) % 4)

    @staticmethod
    def get_vector(direction):
        if direction == Direction.UP:
            return 0, -1
        elif direction == Direction.DOWN:
            return 0, 1
        elif direction == Direction.LEFT:
            return -1, 0
        elif direction == Direction.RIGHT:
            return 1, 0
