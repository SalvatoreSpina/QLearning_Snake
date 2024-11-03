# Game.py

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
import random
from enum import Enum
from typing import List, Tuple
from config import *
from Agent import Agent

# CellType Enum
class CellType(Enum):
    EMPTY = '0'
    SNAKE = 'S'
    HEAD = 'H'
    GREEN_APPLE = 'G'
    RED_APPLE = 'R'
    WALL = 'W'

DIRECTIONS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}

# Mapping from direction vectors to names
DIRECTION_VECTORS_TO_NAMES = {v: k for k, v in DIRECTIONS.items()}

# Opposite directions mapping
OPPOSITE_DIRECTIONS = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT"
}

# Apple Class
class Apple:
    def __init__(self, color: str, position: Tuple[int, int]):
        self.color = color
        self.position = position

# Snake Class
class Snake:
    def __init__(self, initial_position: List[Tuple[int, int]], initial_direction: Tuple[int, int]):
        self.body = initial_position
        self.length = len(self.body)
        self.direction = initial_direction  # Store the current direction

    def move(self, direction: Tuple[int, int], board_size: int):
        self.direction = direction  # Update the direction
        new_head = (self.body[0][0] + direction[0], self.body[0][1] + direction[1])
        if 0 <= new_head[0] < board_size and 0 <= new_head[1] < board_size:
            self.body = [new_head] + self.body[:-1]
        else:
            raise IndexError("Snake moved out of bounds!")

    def grow(self):
        self.body.append(self.body[-1])
        self.length += 1

    def shrink(self):
        if self.length > 1:
            self.body.pop()
            self.length -= 1

    def collides_with_self(self) -> bool:
        return self.body[0] in self.body[1:]

# Board Class
class Board:
    def __init__(self, size: int):
        self.size = size
        self.grid = [[CellType.EMPTY for _ in range(size)] for _ in range(size)]
        self.snake = None
        self.apples = []

    def initialize_snake(self):
        while True:
            start_x, start_y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            initial_position = [(start_x, start_y)]
            for _ in range(2):
                direction = random.choice(list(DIRECTIONS.values()))
                next_x = initial_position[-1][0] + direction[0]
                next_y = initial_position[-1][1] + direction[1]
                if 0 <= next_x < self.size and 0 <= next_y < self.size:
                    initial_position.append((next_x, next_y))
                else:
                    break
            if len(initial_position) == 3:
                initial_direction = (initial_position[0][0] - initial_position[1][0],
                                     initial_position[0][1] - initial_position[1][1])
                self.snake = Snake(initial_position, initial_direction)
                break

    def place_apples(self):
        self.apples = []
        for _ in range(2):  # Two green apples
            self._place_apple("green")
        self._place_apple("red")  # One red apple

    def _place_apple(self, color: str):
        while True:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.grid[x][y] == CellType.EMPTY:
                apple = Apple(color, (x, y))
                self.apples.append(apple)
                break

    def update_board(self):
        self.grid = [[CellType.EMPTY for _ in range(self.size)] for _ in range(self.size)]
        # Place apples
        for apple in self.apples:
            apple_type = CellType.GREEN_APPLE if apple.color == "green" else CellType.RED_APPLE
            x, y = apple.position
            self.grid[x][y] = apple_type
        # Place snake
        for segment in self.snake.body[1:]:
            self.grid[segment[0]][segment[1]] = CellType.SNAKE
        head = self.snake.body[0]
        self.grid[head[0]][head[1]] = CellType.HEAD

    def get_vision(self):
        """Get the snake's vision in all four directions for display purposes."""
        head_x, head_y = self.snake.body[0]
        vision = {}
        for direction_name, (dx, dy) in DIRECTIONS.items():
            cells_in_direction = []
            x, y = head_x + dx, head_y + dy
            while 0 <= x < self.size and 0 <= y < self.size:
                cell = self.grid[x][y]
                cells_in_direction.append(cell.value)
                if cell == CellType.WALL or cell == CellType.SNAKE:
                    break
                x += dx
                y += dy
            else:
                cells_in_direction.append(CellType.WALL.value)  # Edge of the board
            vision[direction_name] = cells_in_direction
        return vision

class Game:
    def __init__(self, board_size: int, agent, print_terminal=True):
        self.board_size = board_size
        self.board = Board(board_size)
        self.is_game_over = False
        self.agent = agent
        self.previous_state = None
        self.previous_action = None
        self.current_state = None  # Store the current state
        self.is_paused = False
        self.apple_eaten = None
        self.print_terminal = print_terminal

    def start(self):
        self.board.initialize_snake()
        self.board.place_apples()
        self.board.update_board()

    def run_step(self):
        if not self.is_game_over and not self.is_paused:
            # Get the snake's state
            state = self.board.get_vision()
            state = self.agent.get_state(state)
            self.current_state = state  # Store the current state

            # Get valid actions
            current_dir = self.board.snake.direction
            current_dir_name = DIRECTION_VECTORS_TO_NAMES[current_dir]
            opposite_dir_name = OPPOSITE_DIRECTIONS[current_dir_name]
            valid_actions = [action for action in DIRECTIONS.keys() if action != opposite_dir_name]
            # Agent makes a decision based on state
            action = self.agent.choose_action(state, valid_actions)
            self.previous_state = state
            self.previous_action = action
            direction = DIRECTIONS[action]

            try:
                self.board.snake.move(direction, self.board.size)
                self._handle_collisions()
                self.check_game_over()
                self.board.update_board()

                # Calculate reward based on previous and current state
                reward = self.get_reward(state, action)

                # Learn from the experience
                if self.previous_state is not None and self.previous_action is not None:
                    self.agent.learn(self.previous_state, self.previous_action, reward, state)

                # Display state and action
                if self.print_terminal:
                    self.display_state_and_action(state, action)
            except IndexError:
                self.is_game_over = True
                # print("Game Over: Snake moved out of bounds!")
                reward = -200  # Penalty for moving out of bounds
                # Learn from the final move
                if self.previous_state is not None and self.previous_action is not None:
                    self.agent.learn(self.previous_state, self.previous_action, reward, state)

    def get_reward(self, current_state, action):
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        action_index = directions.index(action)

        danger_state = current_state[:4]
        green_apple_state = current_state[4:8]
        red_apple_state = current_state[8:]

        if self.is_game_over:
            return -1000  # Major penalty for dying

        if danger_state[action_index]:
            return -1000  # Penalty for moving towards danger

        if green_apple_state[action_index]:
            return 100  # Big reward for moving towards green apple

        if red_apple_state[action_index]:
            return -20  # Penalty for moving towards red apple

        return -5  # Survival reward

    def get_obstacle_distances(self):
        head_x, head_y = self.board.snake.body[0]
        obstacle_distances = {}

        for direction_name, (dx, dy) in DIRECTIONS.items():
            distance = 0
            x, y = head_x + dx, head_y + dy

            while 0 <= x < self.board.size and 0 <= y < self.board.size:
                cell = self.board.grid[x][y]
                if cell == CellType.SNAKE or cell == CellType.WALL:
                    break
                x += dx
                y += dy
                distance += 1

            obstacle_distances[direction_name] = distance

        return obstacle_distances

    def _handle_collisions(self):
        head = self.board.snake.body[0]
        self.apple_eaten = None
        # Check for apple collisions
        for apple in self.board.apples:
            if apple.position == head:
                self.apple_eaten = apple.color
                if apple.color == "green":
                    self.board.snake.grow()
                elif apple.color == "red":
                    self.board.snake.shrink()
                self.board.apples.remove(apple)
                self.board._place_apple(apple.color)
                break

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def check_game_over(self):
        if self.board.snake.collides_with_self():
            self.is_game_over = True
            # print("Game Over: Snake collided with itself!")
        elif self.board.snake.length == 0:
            self.is_game_over = True
            # print("Game Over: Snake has no body!")

    def display_state_and_action(self, state, action):
        print(f"State: {state}")
        print(f"Action Taken: {action}\n")

# ConfigScreen Class
class ConfigScreen:
    def __init__(self, ui, defaults):
        import pygame  # Import here since we need Pygame for this class
        self.ui = ui
        self.font = pygame.font.Font(None, 40)
        self.options = {
            "Board Size": str(defaults.get('board_size', BOARD_SIZE)),
            "Sessions": str(defaults.get('sessions', 1)),
            "Visual": 'on' if defaults.get('visual', True) else 'off',
            "Learn": 'on' if defaults.get('learn', True) else 'off',
            "Speed": defaults.get('speed', 'Normal'),
            "Print Terminal": 'on' if defaults.get('print_terminal', True) else 'off',
            "Step-by-Step": 'on' if defaults.get('step_by_step', False) else 'off'
        }
        self.selected_option = 0
        self.option_keys = list(self.options.keys())
        self.active_input = False
        self.input_rects = {}
        self.save_button_rect = pygame.Rect(100, 600, 400, 50)
        self.total_options = len(self.option_keys) + 1  # Including the Save and Start button

    def display(self):
        if self.ui.visual:
            self.ui.screen.fill(BACKGROUND_COLOR)
            screen_width = self.ui.WINDOW_WIDTH
            screen_height = self.ui.WINDOW_HEIGHT
            y_offset = 70
            total_height = len(self.option_keys) * y_offset + self.save_button_rect.height
            y = (screen_height - total_height) // 2  # Center vertically

            for i, key in enumerate(self.option_keys):
                color = BUTTON_HOVER_COLOR if i == self.selected_option else BUTTON_COLOR
                rect = pygame.Rect(0, 0, 400, 50)
                rect.centerx = screen_width // 2  # Center horizontally
                rect.y = y
                pygame.draw.rect(self.ui.screen, color, rect, border_radius=10)
                if self.active_input and i == self.selected_option:
                    option_text = f"{key}: {self.options[key]}|"
                else:
                    option_text = f"{key}: {self.options[key]}"
                self.ui.render_text(option_text, rect.centerx, rect.centery)
                self.input_rects[key] = rect
                y += y_offset
            # Draw Save and Start button
            button_color = BUTTON_HOVER_COLOR if self.selected_option == self.total_options - 1 else BUTTON_COLOR
            self.save_button_rect.centerx = screen_width // 2
            self.save_button_rect.y = y
            pygame.draw.rect(self.ui.screen, button_color, self.save_button_rect, border_radius=10)
            self.ui.render_text("Save and Start", self.save_button_rect.centerx, self.save_button_rect.centery)
            pygame.display.flip()

    def handle_event(self, event):
        import pygame  # Import here since we need Pygame for this method
        if event.type == pygame.KEYDOWN:
            if self.active_input:
                key = self.option_keys[self.selected_option]
                if event.key == pygame.K_RETURN:
                    self.active_input = False
                elif event.key == pygame.K_BACKSPACE:
                    self.options[key] = self.options[key][:-1]
                else:
                    if key in ["Visual", "Learn", "Speed", "Print Terminal", "Step-by-Step"]:
                        # For toggle options, do not accept text input
                        pass
                    else:
                        self.options[key] += event.unicode
            else:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % self.total_options
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % self.total_options
                elif event.key == pygame.K_RETURN:
                    if self.selected_option < len(self.option_keys):
                        key = self.option_keys[self.selected_option]
                        if key in ["Visual", "Learn", "Print Terminal", "Step-by-Step"]:
                            self.options[key] = "off" if self.options[key] == "on" else "on"
                        elif key == "Speed":
                            speeds = ["Really Slow", "Slow", "Normal", "Fast"]
                            current_index = speeds.index(self.options[key])
                            self.options[key] = speeds[(current_index + 1) % len(speeds)]
                        else:
                            self.active_input = True
                    else:
                        # Save and Start button selected
                        self.apply_config()
                        return "back"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # Check if Save and Start button is clicked
            if self.save_button_rect.collidepoint(pos):
                self.apply_config()
                return "back"
            # Check if any option is clicked
            for i, key in enumerate(self.option_keys):
                rect = self.input_rects[key]
                if rect.collidepoint(pos):
                    self.selected_option = i
                    if key in ["Visual", "Learn", "Print Terminal", "Step-by-Step"]:
                        # Toggle options on click
                        self.options[key] = "off" if self.options[key] == "on" else "on"
                    elif key == "Speed":
                        speeds = ["Slow", "Normal", "Fast"]
                        current_index = speeds.index(self.options[key])
                        self.options[key] = speeds[(current_index + 1) % len(speeds)]
                    else:
                        # Activate text input
                        self.active_input = True
        return None

    def apply_config(self):
        # Update UI settings based on options
        self.ui.board_size = int(self.options["Board Size"])
        self.ui.sessions = int(self.options["Sessions"])
        self.ui.visual = self.options["Visual"] == "on"
        self.ui.learn = self.options["Learn"] == "on"
        self.ui.speed = self.options["Speed"]
        self.ui.print_terminal = self.options["Print Terminal"] == "on"
        self.ui.step_by_step = self.options["Step-by-Step"] == "on"
        # Re-initialize screen if visual setting changed
        if self.ui.visual:
            self.ui.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        else:
            self.ui.screen = None

class GameUI:
    def __init__(self, board_size=BOARD_SIZE, sessions=1, save_file='', load_file='', visual=True, learn=True, speed='Normal', print_terminal=True, step_by_step=False):
        self.visual = visual  # Default to visual on
        self.board_size = board_size
        self.sessions = sessions
        self.save_file = save_file
        self.load_file = load_file
        self.learn = learn
        self.speed = speed
        self.print_terminal = print_terminal
        self.step_by_step = step_by_step
        self.current_session = 0
        self.max_length = 0
        self.max_duration = 0
        self.game = None
        self.agent = Agent()
        self.wait_for_step = False  # Used to control step-by-step execution
        if self.visual:
            import pygame
            pygame.init()
            self.WINDOW_WIDTH, self.WINDOW_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
            self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 30)
            self.state = "config"
            # Pass defaults to ConfigScreen
            defaults = {
                'board_size': self.board_size,
                'sessions': self.sessions,
                'save_file': self.save_file,
                'load_file': self.load_file,
                'visual': self.visual,
                'learn': self.learn,
                'speed': self.speed,
                'print_terminal': self.print_terminal,
                'step_by_step': self.step_by_step
            }
            self.config = ConfigScreen(self, defaults)
        else:
            self.screen = None
            self.clock = None
            self.font = None
            self.state = "training"  # Skip config when visual is off
            self.config = None
            # Load model if specified
            if self.load_file:
                self.agent.load_model(self.load_file)
            self.agent.learning = self.learn

    def render_text(self, text, x, y, center=True):
        """Render text on the screen."""
        import pygame
        if self.visual and self.screen:
            label = self.font.render(text, True, TEXT_COLOR)
            if center:
                label_rect = label.get_rect(center=(x, y))
            else:
                label_rect = label.get_rect(topleft=(x, y))
            self.screen.blit(label, label_rect)

    def run(self):
        running = True

        while running:
            if self.state == "config":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    else:
                        result = self.config.handle_event(event)
                        if result == "back":
                            # Apply config and start sessions
                            self.agent.learning = self.learn
                            if self.load_file:
                                self.agent.load_model(self.load_file)
                            self.state = "training"
                self.config.display()
            elif self.state == "training":
                self.max_length = 0
                self.max_duration = 0
                self.wait_for_step = True  # Initialize wait state
                for session in range(1, self.sessions + 1):
                    self.current_session = session
                    self.game = Game(self.board_size, self.agent, print_terminal=self.print_terminal)
                    self.game.start()
                    steps = 0
                    self.wait_for_step = self.step_by_step
                    while not self.game.is_game_over and running:
                        # Handle events
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                break
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    self.wait_for_step = not self.wait_for_step
                        if not running:
                            break
                        if not self.wait_for_step:
                            self.game.run_step()
                            steps += 1
                            if self.step_by_step:
                                self.wait_for_step = True  # Wait for the next spacebar press

                        if self.visual:
                            self.draw_game()
                            pygame.display.flip()

                        if self.visual:
                            if self.speed == "Really Slow":
                                self.clock.tick(5)
                            elif self.speed == "Slow":
                                self.clock.tick(10)
                            elif self.speed == "Normal":
                                self.clock.tick(20)
                            elif self.speed == "Fast":
                                self.clock.tick(60)
                    if not running:
                        break
                    snake_length = self.game.board.snake.length
                    self.max_length = max(self.max_length, snake_length)
                    self.max_duration = max(self.max_duration, steps)
                    if self.print_terminal:
                        print(f"Session {session}/{self.sessions} completed. Length: {snake_length}, Steps: {steps}")
                if self.print_terminal:
                    print(f"Training completed. Max length: {self.max_length}, Max duration: {self.max_duration}")
                if self.save_file:
                    self.agent.save_model(self.save_file)
                # After training, return to config or exit
                if self.visual:
                    self.state = "config"
                else:
                    running = False
            else:
                # Default state handling
                pass
            if self.visual:
                self.clock.tick(60)
        if self.visual:
            pygame.quit()


        print(f"Training completed. Max length: {self.max_length}, Max duration: {self.max_duration}")

    def draw_game(self):
        """Draw the game elements on the screen."""
        import pygame
        if not self.visual or self.screen is None:
            return
        self.screen.fill(BACKGROUND_COLOR)
        cell_size = min(
            (self.WINDOW_HEIGHT - 100) // self.game.board_size,
            (self.WINDOW_WIDTH - PANEL_WIDTH - 100) // self.game.board_size
        )
        board_origin = (PANEL_WIDTH + 50, 20)
        # Draw the game board
        for x in range(self.game.board.size):
            for y in range(self.game.board.size):
                cell = self.game.board.grid[x][y]
                rect = pygame.Rect(
                    board_origin[0] + y * cell_size,
                    board_origin[1] + x * cell_size,
                    cell_size,
                    cell_size
                )
                if cell == CellType.EMPTY:
                    color = BACKGROUND_COLOR
                elif cell == CellType.SNAKE:
                    color = SNAKE_COLOR
                elif cell == CellType.HEAD:
                    color = HEAD_COLOR
                elif cell == CellType.GREEN_APPLE:
                    color = GREEN_APPLE_COLOR
                elif cell == CellType.RED_APPLE:
                    color = RED_APPLE_COLOR
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)
        # Draw agent's decision info
        vision = self.game.board.get_vision()
        action = self.game.previous_action
        self.display_agent_info(vision, action)
        # Display runtime information
        self.display_runtime_info()
        pygame.display.flip()


    def display_agent_info(self, vision, action):
        import pygame
        if not self.visual or self.screen is None:
            return
        x, y = 20, 50
        
        # Display raw vision data
        self.render_text("Raw Vision:", x, y, center=False)
        y += 30
        for direction, cells in vision.items():
            text = f"{direction}: {''.join(cells)}"
            self.render_text(text, x, y, center=False)
            y += 30
        
        # Display current action
        if action:
            self.render_text(f"Action Taken: {action}", x, y, center=False)
            y += 30
        
        # Display state breakdown
        y += 20
        self.render_text("State Breakdown:", x, y, center=False)
        y += 30
        
        if self.game.current_state:
            directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            
            # Display danger state
            self.render_text("Danger:", x, y, center=False)
            y += 25
            for i, direction in enumerate(directions):
                value = "True" if self.game.current_state[i] else "False"
                self.render_text(f"  {direction}: {value}", x, y, center=False)
                y += 20
                
            # Display green apple state
            y += 10
            self.render_text("Green Apple:", x, y, center=False)
            y += 25
            for i, direction in enumerate(directions):
                value = "True" if self.game.current_state[i + 4] else "False"
                self.render_text(f"  {direction}: {value}", x, y, center=False)
                y += 20
                
            # Display red apple state
            y += 10
            self.render_text("Red Apple:", x, y, center=False)
            y += 25
            for i, direction in enumerate(directions):
                value = "True" if self.game.current_state[i + 8] else "False"
                self.render_text(f"  {direction}: {value}", x, y, center=False)
                y += 20

        # Display Q-values
        y += 20
        self.render_text("Q-values:", x, y, center=False)
        y += 30
        current_state = self.game.current_state
        q_values = self.game.agent.q_table.get(current_state, {})
        for action_name in DIRECTIONS.keys():
            value = q_values.get(action_name, 0)
            text = f"{action_name}: {value:.2f}"
            self.render_text(text, x, y, center=False)
            y += 30
            
        # Display Q-table size
        y += 20
        q_table_size = len(self.game.agent.q_table)
        self.render_text(f"Q-Table Entries: {q_table_size}", x, y, center=False)

    def display_runtime_info(self):
        import pygame
        if not self.visual or self.screen is None:
            return
        x, y = self.WINDOW_WIDTH - PANEL_WIDTH + 20, 50
        self.render_text("Runtime Information:", x, y, center=False)
        y += 30
        # Display model name
        import os
        model_name = os.path.basename(self.save_file) if self.save_file else "N/A"
        self.render_text(f"Model Name: {model_name}", x, y, center=False)
        y += 30
        # Display current session
        self.render_text(f"Session: {self.current_session}/{self.sessions}", x, y, center=False)
        y += 30
        # Display max length
        self.render_text(f"Max Length: {self.max_length}", x, y, center=False)
        y += 30
        # Display max duration
        self.render_text(f"Max Duration: {self.max_duration}", x, y, center=False)
        y += 30
