class MovingComponent:
    def __init__(self, direction, target):
        self.direction = direction
        self.movement_target = target
        self.checked_collision = False
