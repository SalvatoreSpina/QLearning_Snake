import random
import numpy as np
from config import DIRECTIONS, CellType

class Agent:
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.2
        self.discount_factor = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.9997
        self.epsilon_min = 0.05
        self.learning = True

    def get_state(self, vision):
        # Initialize lists for danger, green apple, and red apple
        danger_state = [False, False, False, False]
        green_apple_state = [False, False, False, False]
        red_apple_state = [False, False, False, False]

        # Mapping vision directions to danger, green apple, and red apple state
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        for i, direction in enumerate(directions):
            if direction in vision:
                tiles = vision[direction]
                for j, tile in enumerate(tiles):
                    if j == 0 and (tile == 'W' or tile == 'S'):
                        danger_state[i] = True
                        break
                    elif j == 1 and (tile == 'W' or tile == 'S'):
                        danger_state[i] = True
                        break
                    elif j < 3 and tile == 'R':
                        red_apple_state[i] = True
                        break
                    elif tile == 'G':
                        green_apple_state[i] = True
                        break

        # Final state is a tuple of the three lists concatenated
        state = tuple(danger_state + green_apple_state + red_apple_state)
        # print("State:", state)
        return state

    def choose_action(self, state, valid_actions):
        if self.learning and np.random.rand() < self.epsilon:
            return random.choice(valid_actions)
        
        q_values = self.q_table.get(state, {})
        if not q_values:
            q_values = {action: 0.0 for action in DIRECTIONS.keys()}
            self.q_table[state] = q_values
        
        # Filter to valid actions
        valid_q_values = {action: q_values[action] for action in valid_actions}
        max_q = max(valid_q_values.values())
        best_actions = [a for a in valid_actions if valid_q_values[a] == max_q]
        
        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state):
        if not self.learning:
            return

        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in DIRECTIONS.keys()}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0.0 for a in DIRECTIONS.keys()}

        current_q = self.q_table[state][action]
        next_max_q = max(self.q_table[next_state].values())
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        self.q_table[state][action] = new_q

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
            print("Loaded model has a q_table of size:", len(self.q_table))
        print(f"Model loaded from {filename}")