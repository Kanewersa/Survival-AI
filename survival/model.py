import os

import torch
from torch import nn, optim
import torch.nn.functional as functional


class LinearQNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, pretrained=False):
        super().__init__()
        self.linear_one = nn.Linear(input_size, hidden_size)
        self.linear_two = nn.Linear(hidden_size, output_size)
        self.pretrained = pretrained

    def forward(self, x):
        x = functional.relu(self.linear_one(x))
        x = self.linear_two(x)

        return x

    def save(self, file_name='model.pth'):
        model_directory = 'model'
        if not os.path.exists(model_directory):
            os.makedirs(model_directory)

        file_path = os.path.join(model_directory, file_name)
        torch.save(self.state_dict(), file_path)

    @staticmethod
    def load(input_size, hidden_size, output_size, file_name='model.pth'):
        model_directory = 'model'
        file_path = os.path.join(model_directory, file_name)
        if os.path.isfile(file_path):
            model = LinearQNetwork(input_size, hidden_size, output_size, True)
            model.load_state_dict(torch.load(file_path))
            model.eval()
            return model
        return LinearQNetwork(11, 256, 3)


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss() # Mean squared error

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            # reshape the state to make its values an (n, x) tuple
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # Prediction based on simplified Bellman's equation
        # Predict Q values for current state
        prediction = self.model(state)
        target = prediction.clone()
        for idx in range(len(done)):
            Q = reward[idx]
            if not done[idx]:
                Q = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            # set the target of the maximum value of the action to Q
            target[idx][torch.argmax(action).item()] = Q
        # Apply the loss function
        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction)
        loss.backward()

        self.optimizer.step()
