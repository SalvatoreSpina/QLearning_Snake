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

    def get_state(self, game):
        """
        Get state as binary features based on first visible object in each direction:
        - 4 danger features (up, right, down, left) for wall or snake
        - 4 green apple features (up, right, down, left)
        - 4 red apple features (up, right, down, left)
        Returns a tuple of 12 binary values (0 or 1)
        """
        head_x, head_y = game.board.snake.body[0]
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # UP, RIGHT, DOWN, LEFT
        
        danger_state = []
        green_apple_state = []
        red_apple_state = []

        # Look in each direction
        for dx, dy in directions:
            x, y = head_x, head_y
            found_object = False
            
            # Look until we find something or hit a wall
            while 0 <= x + dx < game.board.size and 0 <= y + dy < game.board.size:
                x += dx
                y += dy
                cell = game.board.grid[x][y]
                
                if cell != CellType.EMPTY:
                    found_object = True
                    # Record what we found (only the first object)
                    danger_state.append(1 if cell == CellType.SNAKE or 
                                     x + dx < 0 or x + dx >= game.board.size or 
                                     y + dy < 0 or y + dy >= game.board.size else 0)
                    green_apple_state.append(1 if cell == CellType.GREEN_APPLE else 0)
                    red_apple_state.append(1 if cell == CellType.RED_APPLE else 0)
                    break
            
            # If we found nothing in this direction
            if not found_object:
                # Wall is the first thing we'll hit
                danger_state.append(1)
                green_apple_state.append(0)
                red_apple_state.append(0)

        # Combine all states into one tuple
        state = tuple(danger_state + green_apple_state + red_apple_state)
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
        print(f"Model loaded from {filename}")