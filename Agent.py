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
        self.epsilon_decay = 0.999  # Slower decay to allow more exploration
        self.epsilon_min = 0.01
        self.learning = True


 
    def get_state(self, game):
        head_x, head_y = game.board.snake.body[0]
        dir_x, dir_y = game.board.snake.direction
        current_direction = (dir_x, dir_y)

        # Define direction indices
        direction_indices = {
            (-1, 0): 0,  # Up
            (1, 0): 1,   # Down
            (0, -1): 2,  # Left
            (0, 1): 3    # Right
        }

        idx = direction_indices[current_direction]

        # Define relative directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        left_direction = directions[(idx + 2) % 4]
        straight_direction = directions[idx]
        right_direction = directions[(idx + 1) % 4]

        # Check for danger
        dangers = []
        for direction in [left_direction, straight_direction, right_direction]:
            x, y = head_x + direction[0], head_y + direction[1]
            if x < 0 or x >= game.board.size or y < 0 or y >= game.board.size:
                dangers.append(1)  # Wall
            elif game.board.grid[x][y] in [CellType.SNAKE]:
                dangers.append(1)  # Snake body
            else:
                dangers.append(0)  # Safe

        # Check for food direction
        food_direction = game.get_food_direction(current_direction)

        # Combine into state
        state = tuple(dangers + food_direction)
        return state

    def choose_action(self, state, valid_actions):
        if self.learning and np.random.rand() < self.epsilon:
            # Explore: choose a random action from valid actions
            action = random.choice(valid_actions)
        else:
            # Exploit: choose the best known action among valid actions
            q_values = self.q_table.get(state, {})
            if q_values:
                # Filter q_values to only include valid actions
                valid_q_values = {a: q_values[a] for a in valid_actions if a in q_values}
                if valid_q_values:
                    action = max(valid_q_values, key=valid_q_values.get)
                else:
                    action = random.choice(valid_actions)
            else:
                action = random.choice(valid_actions)
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
