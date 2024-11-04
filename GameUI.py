import os
import pygame

from Game import Game
from Agent import Agent
from Board import CellType
from ConfigScreen import ConfigScreen
from config import (
    BOARD_SIZE, PANEL_WIDTH, BACKGROUND_COLOR, TEXT_COLOR,
    SNAKE_COLOR, HEAD_COLOR, GREEN_APPLE_COLOR, RED_APPLE_COLOR, GRID_COLOR,
    DIRECTIONS
)


class GameUI:
    def __init__(self, board_size=BOARD_SIZE, sessions=1, save_file='',
                 load_file='', visual=True, learn=True, speed='Normal',
                 print_terminal=True, step_by_step=False):
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
            self._initialize_pygame()
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

    def _initialize_pygame(self):
        self.WINDOW_WIDTH = pygame.display.Info().current_w
        self.WINDOW_HEIGHT = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH,
                                               self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)

    def render_text(self, text, x, y, center=True):
        """Render text on the screen."""
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
                running = self._handle_config_state(running)
            elif self.state == "training":
                running = self._handle_training_state(running)
            else:
                # Default state handling
                pass
            if self.visual:
                self.clock.tick(60)
        if self.visual:
            pygame.quit()

        print(f"Training completed. Max length: {self.max_length},\
            Max duration: {self.max_duration}")

    def _handle_config_state(self, running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            else:
                result = self.config.handle_event(event)
                if result == "back":
                    # Apply config and start sessions
                    self.agent.learning = self.learn
                    if self.load_file:
                        self.agent.load_model(self.load_file)
                    self.state = "training"
        self.config.display()
        return running

    def _handle_training_state(self, running):
        self.max_length = 0
        self.max_duration = 0
        self.wait_for_step = True  # Initialize wait state
        for session in range(1, self.sessions + 1):
            self.current_session = session
            self.game = Game(self.board_size, self.agent,
                             print_terminal=self.print_terminal)
            self.game.start()
            steps = 0
            self.wait_for_step = self.step_by_step
            while not self.game.is_game_over and running:
                running = self._handle_events(running)
                if not running:
                    break
                if not self.wait_for_step:
                    self.game.run_step()
                    steps += 1
                    if self.step_by_step:
                        self.wait_for_step = True  # Wait for spacebar

                if self.visual:
                    self.draw_game()
                    pygame.display.flip()

                self._control_speed()
            if not running:
                break
            self._update_statistics(steps)
            if self.print_terminal:
                print(f"Session {session}/{self.sessions} completed.\
                    Length: {self.game.board.snake.length}, Steps: {steps}")
        if self.print_terminal:
            print(f"Training completed. Max length: {self.max_length}, \
                Max duration: {self.max_duration}")
        if self.save_file:
            self.agent.save_model(self.save_file)
        # After training, return to config or exit
        if self.visual:
            self.state = "config"
        else:
            running = False
        return running

    def _handle_events(self, running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.wait_for_step = not self.wait_for_step
        return running

    def _control_speed(self):
        if self.visual:
            speeds = {
                "Really Slow": 5,
                "Slow": 10,
                "Normal": 20,
                "Fast": 60
            }
            self.clock.tick(speeds.get(self.speed, 20))

    def _update_statistics(self, steps):
        snake_length = self.game.board.snake.length
        self.max_length = max(self.max_length, snake_length)
        self.max_duration = max(self.max_duration, steps)

    def draw_game(self):
        """Draw the game elements on the screen."""
        if not self.visual or self.screen is None:
            return
        self.screen.fill(BACKGROUND_COLOR)
        cell_size = min(
            (self.WINDOW_HEIGHT - 100) // self.game.board_size,
            (self.WINDOW_WIDTH - PANEL_WIDTH - 100) // self.game.board_size
        )
        board_origin = (PANEL_WIDTH + 50, 20)
        self._draw_board(cell_size, board_origin)
        # Draw agent's decision info
        self._display_agent_info()
        # Display runtime information
        self._display_runtime_info()
        pygame.display.flip()

    def _draw_board(self, cell_size, board_origin):
        for x in range(self.game.board.size):
            for y in range(self.game.board.size):
                cell = self.game.board.grid[x][y]
                rect = pygame.Rect(
                    board_origin[0] + y * cell_size,
                    board_origin[1] + x * cell_size,
                    cell_size,
                    cell_size
                )
                color = self._get_cell_color(cell)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

    def _get_cell_color(self, cell):
        if cell == CellType.EMPTY:
            return BACKGROUND_COLOR
        elif cell == CellType.SNAKE:
            return SNAKE_COLOR
        elif cell == CellType.HEAD:
            return HEAD_COLOR
        elif cell == CellType.GREEN_APPLE:
            return GREEN_APPLE_COLOR
        elif cell == CellType.RED_APPLE:
            return RED_APPLE_COLOR
        else:
            return BACKGROUND_COLOR

    def _display_agent_info(self):
        vision = self.game.board.get_vision()
        action = self.game.previous_action
        if not self.visual or self.screen is None:
            return
        x, y = 20, 50

        # Display raw vision data
        y = self._render_section_title("Raw Vision:", x, y)
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
        y = self._display_state_breakdown(x, y)

        # Display Q-values
        y += 20
        y = self._display_q_values(x, y)

        # Display Q-table size
        y += 20
        q_table_size = len(self.game.agent.q_table)
        self.render_text(f"Q-Table Entries: {q_table_size}",
                         x, y, center=False)

    def _render_section_title(self, title, x, y):
        self.render_text(title, x, y, center=False)
        return y + 30

    def _display_state_breakdown(self, x, y):
        self.render_text("State Breakdown:", x, y, center=False)
        y += 30
        if self.game.current_state:
            y = self._display_state_section("Danger",
                                            self.game.current_state[:4], x, y)
            y += 10
            y = self._display_state_section("Green Apple",
                                            self.game.current_state[4:8], x, y)
            y += 10
            y = self._display_state_section("Red Apple",
                                            self.game.current_state[8:12],
                                            x, y)
        return y

    def _display_state_section(self, title, state_slice, x, y):
        self.render_text(f"{title}:", x, y, center=False)
        y += 25
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        for i, direction in enumerate(directions):
            value = "True" if state_slice[i] else "False"
            self.render_text(f"  {direction}: {value}", x, y, center=False)
            y += 20
        return y

    def _display_q_values(self, x, y):
        self.render_text("Q-values:", x, y, center=False)
        y += 30
        current_state = self.game.current_state
        q_values = self.game.agent.q_table.get(current_state, {})
        for action_name in DIRECTIONS.keys():
            value = q_values.get(action_name, 0)
            text = f"{action_name}: {value:.2f}"
            self.render_text(text, x, y, center=False)
            y += 30
        return y

    def _display_runtime_info(self):
        if not self.visual or self.screen is None:
            return
        x, y = self.WINDOW_WIDTH - PANEL_WIDTH + 20, 50
        self.render_text("Runtime Information:", x, y, center=False)
        y += 30
        if self.save_file:
            model_name = os.path.basename(self.save_file)
        elif self.load_file:
            model_name = os.path.basename(self.load_file)
        else:
            model_name = "None"
        self.render_text(f"Model Name: {model_name}", x, y, center=False)
        y += 30
        # Display current session
        self.render_text(f"Session: {self.current_session}/{self.sessions}",
                         x, y, center=False)
        y += 30
        # Display max length
        self.render_text(f"Max Length: {self.max_length}", x, y, center=False)
        y += 30
        # Display max duration
        self.render_text(f"Max Duration: {self.max_duration}",
                         x, y, center=False)
        y += 30
