import random
import numpy as np
from config import DIRECTIONS, CellType

class Agent:
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.2  # Increased to learn faster
        self.discount_factor = 0.95  # Increased to value future rewards more
        self.epsilon = 1.0
        self.epsilon_decay = 0.9997  # Slower decay for better exploration
        self.epsilon_min = 0.05  # Increased minimum exploration rate
        self.learning = True
        self.last_distance = None
        self.moves_without_apple = 0

    def get_state(self, game):
        """
        Get state based on what the snake can see in four directions (UP, RIGHT, DOWN, LEFT).
        For each direction, returns:
        - 0 if empty
        - Negative number for distance to first obstacle
        - Positive number for distance to first green apple
        - Half positive number for distance to first red apple
        This creates a clearer distinction between good and bad paths.
        """
        head_x, head_y = game.board.snake.body[0]
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # UP, RIGHT, DOWN, LEFT
        
        state = []
        for dx, dy in directions:
            x, y = head_x, head_y
            distance = 0
            found_something = False
            
            while 0 <= x + dx < game.board.size and 0 <= y + dy < game.board.size:
                x += dx
                y += dy
                distance += 1
                cell = game.board.grid[x][y]
                
                if cell == CellType.SNAKE or x + dx < 0 or x + dx >= game.board.size or y + dy < 0 or y + dy >= game.board.size:
                    state.append(-distance)  # Negative for obstacles
                    found_something = True
                    break
                elif cell == CellType.GREEN_APPLE:
                    state.append(distance)  # Positive for green apple
                    found_something = True
                    break
                elif cell == CellType.RED_APPLE:
                    state.append(distance/2)  # Half positive for red apple
                    found_something = True
                    break
                
            if not found_something:
                state.append(0)  # Empty path
                
        return tuple(state)

    def choose_action(self, state, valid_actions):
        # Ensure exploration in early stages
        if self.learning and (np.random.rand() < self.epsilon or len(self.q_table) < 1000):
            return random.choice(valid_actions)
        
        q_values = self.q_table.get(state, {})
        if not q_values:
            q_values = {action: 0.0 for action in DIRECTIONS.keys()}
            self.q_table[state] = q_values
        
        # Filter to valid actions and add exploration bonus for less-visited states
        valid_q_values = {}
        for action in valid_actions:
            base_value = q_values[action]
            exploration_bonus = 1.0 / (1.0 + self.q_table[state].get(action, 0))
            valid_q_values[action] = base_value + exploration_bonus * self.epsilon
        
        max_q = max(valid_q_values.values())
        best_actions = [a for a in valid_actions if valid_q_values[a] >= max_q - 0.1]  # Allow near-optimal actions
        
        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state):
        if not self.learning:
            return

        # Initialize Q-values if needed
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in DIRECTIONS.keys()}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0.0 for a in DIRECTIONS.keys()}

        # Check if moving towards visible green apple
        current_apple_dist = max([d for d in next_state if d > 0], default=0)
        if self.last_distance is not None and current_apple_dist > 0:
            if current_apple_dist < self.last_distance:
                reward += 5  # Bonus for moving towards apple
            elif current_apple_dist > self.last_distance:
                reward -= 2  # Small penalty for moving away
        self.last_distance = current_apple_dist

        # Punish more for dying when apple is visible
        if reward == -100 and any(d > 0 for d in state):
            reward = -150

        # Q-learning update with eligibility trace-like mechanism
        current_q = self.q_table[state][action]
        next_max_q = max(self.q_table[next_state].values())
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        
        # Add momentum to learning
        momentum = 0.9
        self.q_table[state][action] = momentum * current_q + (1 - momentum) * new_q

        # Decay epsilon with adaptive rate
        if self.epsilon > self.epsilon_min:
            # Decay slower when finding apples, faster when dying
            if reward >= 50:  # Found apple
                self.epsilon *= 0.9999
            elif reward <= -100:  # Died
                self.epsilon *= 0.999
            else:
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