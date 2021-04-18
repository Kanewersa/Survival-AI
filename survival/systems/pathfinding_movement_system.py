from survival import esper
from survival.components.movement_component import MovementComponent
from survival.components.moving_component import MovingComponent
from survival.components.position_component import PositionComponent
from survival.enums import Direction
from survival.pathfinding import breadth_first_search
from survival.systems.input_system import PathfindingComponent


class PathfindingMovementSystem(esper.Processor):
    def __init__(self, game_map):
        self.game_map = game_map
        pass

    def process(self, dt):
        for ent, (pos, pathfinding, movement) in self.world.get_components(PositionComponent, PathfindingComponent,
                                                                           MovementComponent):
            if pathfinding.path is None:
                pathfinding.path = breadth_first_search(self.game_map, pos.grid_position, pathfinding.target_grid_pos)

            if len(pathfinding.path) < 1:
                self.world.remove_component(ent, PathfindingComponent)
                continue

            if self.world.has_component(ent, MovingComponent):
                continue

            target = pathfinding.path.pop(0)
            vector = (target[0] - pos.grid_position[0], target[1] - pos.grid_position[1])
            direction = Direction.from_vector(vector)
            if direction != pos.direction:
                pos.direction = direction

            self.world.add_component(ent, MovingComponent())
