import random
from collections import deque

import torch

from survival import esper, GameMap
from survival.components.direction_component import DirectionChangeComponent
from survival.components.inventory_component import InventoryComponent
from survival.components.moving_component import MovingComponent
from survival.components.position_component import PositionComponent
from survival.components.learning_component import LearningComponent
from survival.components.time_component import TimeComponent
from survival.graph_search import Action
from survival.learning_utils import get_state, LearningUtils
from survival.model import LinearQNetwork, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
LEARN = True


class NeuralSystem(esper.Processor):
    def __init__(self, game_map: GameMap, callback):
        self.game_map = game_map
        self.reset_game = callback
        self.n_games = 0  # number of games played
        self.starting_epsilon = 100
        self.epsilon = 0  # controlls the randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # exceeding memory removes the left elements to make more space
        self.model = LinearQNetwork.load(11, 256, 3)
        if self.model.pretrained:
            self.starting_epsilon = -1
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.utils = LearningUtils()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def get_action(self, state):
        self.epsilon = self.starting_epsilon - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state_zero = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_zero)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    def process(self, dt):
        for ent, (pos, inventory, time, learning) in self.world.get_components(PositionComponent, InventoryComponent,
                                                                               TimeComponent, LearningComponent):
            if not learning.made_step:
                learning.reset()

                # Get the closest resource | [entity, path, cost]
                resource: [int, list, int] = self.game_map.find_nearest_resource(self.world, ent, pos)

                # Get current entity state
                old_state = get_state(self, ent, resource)
                # Predict the action
                action = self.get_action(old_state)
                # Save the action
                learning.load_step(old_state, action, resource)
                # Perform the action
                act = Action.perform(self.world, ent, Action.from_array(action))
                self.utils.append_action(act, pos)
                continue

            # Wait for the action to complete
            if self.world.has_component(ent, DirectionChangeComponent) or self.world.has_component(ent,
                                                                                                   MovingComponent):
                continue

            self.utils.check_last_actions(learning)

            resource = learning.resource
            if resource is None or not self.world.entity_exists(resource[0]):
                # Find a new resource if no resource was found or the last one was consumed
                resource = self.game_map.find_nearest_resource(self.world, ent, pos)

            # Get new state
            new_state = get_state(self, ent, resource)
            # Train agent's memory
            self.train_short_memory(learning.old_state, learning.action, learning.reward, new_state, learning.done)
            self.remember(learning.old_state, learning.action, learning.reward, new_state, learning.done)

            learning.made_step = False

            if learning.done:
                self.n_games += 1
                if LEARN:
                    self.train_long_memory()
                if learning.score > learning.record:
                    learning.record = learning.score
                    if LEARN:
                        self.model.save()

                print('Game', self.n_games, 'Score', learning.score, 'Record', learning.record)
                self.utils.add_scores(learning, self.n_games)
                learning.score = 0
                self.utils.plot()

                self.reset_game()
