from enum import Enum
from queue import PriorityQueue

from survival import GameMap
from survival.components.position_component import PositionComponent
from survival.enums import Direction


class Action(Enum):
    ROTATE_LEFT = 0
    ROTATE_RIGHT = 1
    MOVE = 2


class State:
    def __init__(self, position: tuple[int, int], direction: Direction):
        self.position = position
        self.direction = direction


class Node:
    def __init__(self, state: State, parent=None, action=None, cost=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.cost == other.cost


def get_moved_position(position: tuple[int, int], direction: Direction):
    vector = Direction.get_vector(direction)
    return position[0] + vector[0], position[1] + vector[1]


def get_states(state: State, game_map: GameMap) -> list[tuple[Action, State, int]]:
    states = list()

    states.append((Action.ROTATE_LEFT, State(state.position, state.direction.rotate_left(state.direction)), 1))
    states.append((Action.ROTATE_RIGHT, State(state.position, state.direction.rotate_right(state.direction)), 1))

    target_position = get_moved_position(state.position, state.direction)
    if not game_map.is_colliding(target_position):
        states.append((Action.MOVE, State(target_position, state.direction), game_map.get_cost(target_position)))

    return states


def build_path(node: Node):
    actions = [node.action]
    parent = node.parent

    while parent is not None:
        if parent.action is not None:
            actions.append(parent.action)
        parent = parent.parent

    actions.reverse()
    return actions


def heuristic(new_node: Node, goal: tuple[int, int]):
    return abs(new_node.state.position[0] - goal[0]) + abs(new_node.state.position[1] - goal[1])


def graph_search(game_map: GameMap, start: PositionComponent, goal: tuple):
    fringe = PriorityQueue()
    explored = list()

    explored_states = set()
    fringe_states = set()  # Stores positions and directions of states

    start = State(start.grid_position, start.direction)
    fringe.put((0, Node(start, cost=0)))
    fringe_states.add((tuple(start.position), start.direction))

    while True:
        # No solutions found
        if fringe.empty():
            return []

        node = fringe.get()
        node_priority = node[0]
        node = node[1]
        fringe_states.remove((tuple(node.state.position), node.state.direction))

        # Check goal
        if node.state.position == goal:
            return build_path(node)

        explored.append(node)
        explored_states.add((tuple(node.state.position), node.state.direction))

        # Get all possible states
        for state in get_states(node.state, game_map):
            sub_state = (tuple(state[1].position), state[1].direction)
            new_node = Node(state=state[1],
                            parent=node,
                            action=state[0],
                            cost=(state[2] + node.cost))
            
            priority = new_node.cost + heuristic(new_node, goal)
            if sub_state not in fringe_states and sub_state not in explored_states:
                fringe.put((priority, new_node))
                fringe_states.add((tuple(new_node.state.position), new_node.state.direction))
            elif sub_state in fringe_states and node.cost > new_node.cost:
                fringe.get(node)
                fringe.put((priority, new_node))
                fringe_states.add((tuple(new_node.state.position), new_node.state.direction))
