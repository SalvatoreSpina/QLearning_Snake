import json
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
                    elif j < 2 and tile == 'R':
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
        # Even with learning off, keep a small exploration rate
        exploration_chance = self.epsilon if self.learning else 0.05
        
        if np.random.rand() < exploration_chance:
            return random.choice(valid_actions)
        
        q_values = self.q_table.get(state, {})
        if not q_values:
            # For unseen states, initialize with small random values
            # This helps prevent getting stuck in new situations
            q_values = {action: np.random.uniform(0.1, 0.2) for action in DIRECTIONS.keys()}
            self.q_table[state] = q_values
        
        # Filter to valid actions
        valid_q_values = {action: q_values[action] for action in valid_actions}
        
        # Add small random noise to break ties
        noisy_q_values = {
            action: value + np.random.normal(0, 0.05) 
            for action, value in valid_q_values.items()
        }
        
        # Get best action based on noisy Q-values
        max_q = max(noisy_q_values.values())
        best_actions = [a for a in valid_actions if noisy_q_values[a] == max_q]
        
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
        """Save Q-table to file with proper encoding and error handling"""
        try:
            # Convert tuple keys to strings for JSON serialization
            serializable_q_table = {}
            for state, actions in self.q_table.items():
                # Convert tuple state to string representation
                state_str = str(state)
                serializable_q_table[state_str] = actions
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(serializable_q_table, f, ensure_ascii=True, indent=2)
            print(f"Model saved to {filename}")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def load_model(self, filename):
        """Load Q-table from file and validate/clean the data"""
        try:
            with open(filename, 'r') as f:
                self.q_table = json.load(f)
                
            # Convert string tuple keys back to actual tuples
            cleaned_q_table = {}
            for state_str, actions in self.q_table.items():
                # Convert string state to tuple
                try:
                    # Evaluate the string representation of the state tuple
                    state = eval(state_str)
                    # Verify it's a valid state (12 boolean values)
                    if isinstance(state, tuple) and len(state) == 12 and all(isinstance(x, bool) for x in state):
                        # Verify actions are valid
                        valid_actions = {}
                        for action, value in actions.items():
                            if action in DIRECTIONS and isinstance(value, (int, float)):
                                valid_actions[action] = float(value)
                        if valid_actions:
                            cleaned_q_table[state] = valid_actions
                except:
                    continue
                    
            self.q_table = cleaned_q_table
            print(f"Loaded model has a q_table of size: {len(self.q_table)}")
            print(f"Model loaded from {filename}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.q_table = {}