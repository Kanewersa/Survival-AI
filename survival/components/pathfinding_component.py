class PathfindingComponent:
    def __init__(self, target_pos, searching_for_resource=False):
        self.target_grid_pos = (int(target_pos[0] / 32), int(target_pos[1] / 32))
        self.searching_for_resource = False
        self.current_target = None
        self.path = None
