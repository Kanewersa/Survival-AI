from enum import Enum

from survival import GameMap
from survival.components.position_component import PositionComponent
from survival.enums import Direction


class Action(Enum):
    ROTATE_LEFT = 0
    ROTATE_RIGHT = 1
    MOVE = 2


class State:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction


class Node:
    def __init__(self, state: State, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action


def get_moved_position(position, direction):
    vector = Direction.get_vector(direction)
    return position[0] + vector[0], position[1] + vector[1]


def get_states(state: State, game_map: GameMap):
    states = list()

    states.append((Action.ROTATE_LEFT, State(state.position, state.direction.rotate_left(state.direction))))
    states.append((Action.ROTATE_RIGHT, State(state.position, state.direction.rotate_right(state.direction))))

    target_state = get_moved_position(state.position, state.direction)
    if not game_map.is_colliding(target_state):
        states.append((Action.MOVE, State(target_state, state.direction)))

    return states


def graph_search(game_map: GameMap, start: PositionComponent, goal: tuple):
    fringe = list()
    explored = list()

    explored_states = set()
    fringe_states = set()

    start = State(start.grid_position, start.direction)
    fringe.append(Node(start))
    fringe_states.add((tuple(start.position), start.direction))

    while True:
        # No solutions found
        if not any(fringe):
            return []

        node = fringe.pop(0)
        fringe_states.remove((tuple(node.state.position), node.state.direction))

        # Check goal
        if node.state.position == goal:
            actions = [node.action]
            parent = node.parent

            while parent is not None:
                if parent.action is not None:
                    actions.append(parent.action)
                parent = parent.parent

            actions.reverse()
            return actions

        explored.append(node)
        explored_states.add((tuple(node.state.position), node.state.direction))

        # Get all possible states
        for state in get_states(node.state, game_map):
            sub_state = (tuple(state[1].position), state[1].direction)
            if sub_state not in fringe_states and sub_state not in explored_states:
                new_node = Node(state=state[1],
                                parent=node,
                                action=state[0])
                fringe.append(new_node)
                fringe_states.add((tuple(new_node.state.position), new_node.state.direction))
