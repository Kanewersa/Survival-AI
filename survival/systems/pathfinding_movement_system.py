from survival import esper
from survival.components.direction_component import DirectionChangeComponent
from survival.components.movement_component import MovementComponent
from survival.components.moving_component import MovingComponent
from survival.components.position_component import PositionComponent
from survival.enums import Direction
from survival.graph_search import graph_search, Action
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
                pathfinding.path = graph_search(self.game_map, pos, pathfinding.target_grid_pos)

            if len(pathfinding.path) < 1:
                self.world.remove_component(ent, PathfindingComponent)
                continue

            if self.world.has_component(ent, MovingComponent) or self.world.has_component(ent, DirectionChangeComponent):
                continue

            action = pathfinding.path.pop(0)

            if action == Action.ROTATE_LEFT:
                self.world.add_component(ent, DirectionChangeComponent(Direction.rotate_left(pos.direction)))
            elif action == Action.ROTATE_RIGHT:
                self.world.add_component(ent, DirectionChangeComponent(Direction.rotate_right(pos.direction)))
            else:
                self.world.add_component(ent, MovingComponent())

            # if pathfinding.path is None:
            #     pathfinding.path = breadth_first_search(self.game_map, pos.grid_position, pathfinding.target_grid_pos)
            #
            # if len(pathfinding.path) < 1 and pathfinding.current_target is None:
            #     self.world.remove_component(ent, PathfindingComponent)
            #     continue
            #
            # if self.world.has_component(ent, MovingComponent):
            #     continue
            #
            # if pathfinding.current_target is None:
            #     target = pathfinding.path.pop(0)
            # else:
            #     target = pathfinding.current_target
            #
            # vector = (target[0] - pos.grid_position[0], target[1] - pos.grid_position[1])
            # direction = Direction.from_vector(vector)
            # if direction != pos.direction:
            #     pathfinding.current_target = target
            #     self.world.add_component(ent, DirectionChangeComponent(direction))
            #     continue
            #
            # pathfinding.current_target = None
            # self.world.add_component(ent, MovingComponent())
