import numpy as np
from IPython import display
from matplotlib import pyplot as plt

from survival.components.learning_component import LearningComponent
from survival.components.position_component import PositionComponent
from survival.enums import Direction
from survival.graph_search import Action


class LearningUtils:
    def __init__(self):
        self.plot_scores = []
        self.plot_mean_scores = []
        self.total_score = 0
        self.last_actions: [Action, [int, int]] = []

    def add_scores(self, learning: LearningComponent, games_count: int):
        self.plot_scores.append(learning.score)
        self.total_score += learning.score
        mean_score = self.total_score / games_count
        self.plot_mean_scores.append(mean_score)

    def plot(self):
        display.clear_output(wait=True)
        display.display(plt.gcf())
        plt.clf()
        plt.title('Training...')
        plt.xlabel('Number of Games')
        plt.ylabel('Score')
        plt.plot(self.plot_scores)
        # plt.plot(self.plot_mean_scores)
        plt.ylim(ymin=0)
        plt.text(len(self.plot_scores) - 1, self.plot_scores[-1], str(self.plot_scores[-1]))
        # plt.text(len(self.plot_mean_scores) - 1, self.plot_mean_scores[-1], str(self.plot_mean_scores[-1]))
        plt.show(block=False)
        plt.pause(.1)

    def append_action(self, action: Action, pos: PositionComponent):
        self.last_actions.append([action, pos.grid_position])

    def check_last_actions(self, learning):
        """
        Checks if all the last five actions were repeated and imposes the potential penalty.
        :param learning:
        """
        if len(self.last_actions) > 5:
            self.last_actions.pop(0)

        last_action: [Action, [int, int]] = self.last_actions[0]
        last_grid_pos: [int, int] = last_action[1]

        rotations = 0
        collisions = 0
        for action in self.last_actions:
            if action != Action.MOVE:
                rotations += 1
            else:
                current_grid_pos = action[1]
                if current_grid_pos[0] == last_grid_pos[0] and current_grid_pos[1] == last_grid_pos[1]:
                    collisions += 1

        if rotations > 4 or collisions > 4:
            learning.reward -= 2


def get_state(system, player, resource):
    pos: PositionComponent = system.world.component_for_entity(player, PositionComponent)
    if resource is None or resource[0] is None:
        res_l = False
        res_r = False
        res_u = False
        res_d = False
    else:
        resource_pos: PositionComponent = system.world.component_for_entity(resource[0], PositionComponent)
        res_l = resource_pos.grid_position[0] < pos.grid_position[0]
        res_r = resource_pos.grid_position[0] > pos.grid_position[0]
        res_u = resource_pos.grid_position[1] < pos.grid_position[1]
        res_d = resource_pos.grid_position[1] > pos.grid_position[1]

    dir_l = pos.direction == Direction.LEFT
    dir_r = pos.direction == Direction.RIGHT
    dir_u = pos.direction == Direction.UP
    dir_d = pos.direction == Direction.DOWN

    pos_l = [pos.grid_position[0] - 1, pos.grid_position[1]]
    pos_r = [pos.grid_position[0] + 1, pos.grid_position[1]]
    pos_u = [pos.grid_position[0], pos.grid_position[1] - 1]
    pos_d = [pos.grid_position[0], pos.grid_position[1] + 1]
    col_l = system.game_map.in_bounds(
        pos_l)  # self.game_map.is_colliding(pos_l) and self.game_map.get_entity(pos_l) is None
    col_r = system.game_map.in_bounds(
        pos_r)  # self.game_map.is_colliding(pos_r) and self.game_map.get_entity(pos_r) is None
    col_u = system.game_map.in_bounds(
        pos_u)  # self.game_map.is_colliding(pos_u) and self.game_map.get_entity(pos_u) is None
    col_d = system.game_map.in_bounds(
        pos_d)  # self.game_map.is_colliding(pos_d) and self.game_map.get_entity(pos_d) is None

    state = [
        # Collision ahead
        (dir_r and col_r) or (dir_l and col_l) or (dir_u and col_u) or (dir_d and col_d),
        # Collision on the right
        (dir_u and col_r) or (dir_r and col_d) or (dir_d and col_l) or (dir_l and col_u),
        # Collision on the left
        (dir_u and col_l) or (dir_l and col_d) or (dir_d and col_r) or (dir_r and col_u),
        # Movement direction
        dir_l, dir_r, dir_u, dir_d,
        # Resource location
        res_l, res_r, res_u, res_d
    ]

    return np.array(state, dtype=int)
