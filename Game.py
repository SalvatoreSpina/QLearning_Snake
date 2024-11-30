from Board import Board
from config import DIRECTIONS


class Game:
    def __init__(self, board_size: int, agent, print_terminal=True):
        self.board_size = board_size
        self.board = Board(board_size)
        self.is_game_over = False
        self.agent = agent
        self.previous_state = None
        self.previous_action = None
        self.current_state = None
        self.is_paused = False
        self.apple_eaten = None
        self.print_terminal = print_terminal

    def start(self):
        self.board.initialize_snake()
        self.board.place_apples()
        self.board.update_board()

    def run_step(self):
        if self.is_game_over or self.is_paused:
            return
        try:
            self._update_current_state()
            valid_actions = self._get_valid_actions()
            action = self.agent.choose_action(self.current_state,
                                              valid_actions)
            self.previous_state = self.current_state
            self.previous_action = action
            self._move_snake(action)
            self._handle_collisions()
            self._check_game_over()
            self.board.update_board()
            reward = self.get_reward(self.current_state, action)
            self._learn_from_experience(reward)
            if self.print_terminal:
                self.display_state_and_action(self.current_state, action)
        except IndexError:
            self._handle_out_of_bounds()

    def _update_current_state(self):
        state = self.board.get_vision()
        self.current_state = self.agent.get_state(state)

    def _get_valid_actions(self):
        return [action for action in DIRECTIONS]

    def _move_snake(self, action):
        direction = DIRECTIONS[action]
        self.board.snake.move(direction, self.board.size)

    def _learn_from_experience(self, reward):
        if self.previous_state and self.previous_action:
            self.agent.learn(self.previous_state, self.previous_action,
                             reward, self.current_state)

    def _handle_out_of_bounds(self):
        self.is_game_over = True
        reward = -10
        self._learn_from_experience(reward)

    def get_reward(self, current_state, action):
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        action_index = directions.index(action)
        danger_state = current_state[:4]
        green_apple_state = current_state[4:8]
        red_apple_state = current_state[8:]

        if self.is_game_over:
            return -10
        if danger_state[action_index]:
            return -10
        if green_apple_state[action_index]:
            return 5
        if red_apple_state[action_index]:
            return -4
        return -1

    def _handle_collisions(self):
        head = self.board.snake.body[0]
        self.apple_eaten = None
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

    def _check_game_over(self):
        if (self.board.snake.collides_with_self() or
                self.board.snake.length == 0):
            self.is_game_over = True

    def display_state_and_action(self, state, action):
        print(f"State: {state}")
        print(f"Action Taken: {action}\n")
