# Agent.py

import random
import numpy as np
from config import DIRECTIONS, CellType

class Agent:
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 1.0
        self.epsilon_decay = 0.9995  # Slower decay
        self.epsilon_min = 0.01
        self.learning = True

    def get_state(self, vision):
        state = []
        for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            cells = vision[direction]
            obstacle_distance = None
            green_apple_distance = None
            red_apple_distance = None
            for i, cell in enumerate(cells):
                if cell == CellType.WALL.value or cell == CellType.SNAKE.value:
                    obstacle_distance = i + 1
                    break
                elif cell == CellType.GREEN_APPLE.value and green_apple_distance is None:
                    green_apple_distance = i + 1
                elif cell == CellType.RED_APPLE.value and red_apple_distance is None:
                    red_apple_distance = i + 1
            if obstacle_distance is None:
                obstacle_distance = len(cells) + 1  # If no obstacle is seen, set distance beyond visible range
            state.extend([
                obstacle_distance,
                green_apple_distance if green_apple_distance is not None else 0,
                red_apple_distance if red_apple_distance is not None else 0
            ])
        return tuple(state)

    def choose_action(self, state):
        if self.learning and np.random.rand() < self.epsilon:
            # Explore: choose a random action
            action = random.choice(list(DIRECTIONS.keys()))
        else:
            # Exploit: choose the best known action
            q_values = self.q_table.get(state, {})
            if q_values:
                action = max(q_values, key=q_values.get)
            else:
                action = random.choice(list(DIRECTIONS.keys()))
        return action

    def learn(self, state, action, reward, next_state):
        if not self.learning:
            return
        # Initialize Q-values if state-action pair is unseen
        self.q_table.setdefault(state, {a: 0 for a in DIRECTIONS.keys()})
        self.q_table.setdefault(next_state, {a: 0 for a in DIRECTIONS.keys()})
        q_predict = self.q_table[state][action]
        q_target = reward + self.discount_factor * max(self.q_table[next_state].values())
        self.q_table[state][action] += self.learning_rate * (q_target - q_predict)
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_model(self, filename):
        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"Model saved to {filename}")

    def load_model(self, filename):
        import pickle
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
        print(f"Model loaded from {filename}")
