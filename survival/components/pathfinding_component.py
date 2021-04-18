class PathfindingComponent:
    def __init__(self, target_pos):
        self.target_grid_pos = (int(target_pos[0] / 32), int(target_pos[1] / 32))
        self.path = None
