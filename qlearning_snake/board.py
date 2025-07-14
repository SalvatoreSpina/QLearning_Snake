import random
from enum import Enum
from typing import List, Tuple

from .config import DIRECTIONS


# CellType Enum
class CellType(Enum):
    EMPTY = '0'
    SNAKE = 'S'
    HEAD = 'H'
    GREEN_APPLE = 'G'
    RED_APPLE = 'R'
    WALL = 'W'


# Apple Class
class Apple:
    def __init__(self, color: str, position: Tuple[int, int]):
        self.color = color
        self.position = position


# Snake Class
class Snake:
    def __init__(self, initial_position: List[Tuple[int, int]],
                 initial_direction: Tuple[int, int]):
        self.body = initial_position
        self.length = len(self.body)
        self.direction = initial_direction  # Store the current direction

    def move(self, direction: Tuple[int, int], board_size: int):
        self.direction = direction  # Update the direction
        new_head = (self.body[0][0] + direction[0],
                    self.body[0][1] + direction[1])
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
        self.grid = [
            [CellType.EMPTY for _ in range(size)]
            for _ in range(size)
        ]
        self.snake = None
        self.apples = []

    def initialize_snake(self):
        while True:
            start_x = random.randint(0, self.size - 1)
            start_y = random.randint(0, self.size - 1)
            initial_pos = [(start_x, start_y)]
            for _ in range(2):
                direction = random.choice(list(DIRECTIONS.values()))
                next_x = initial_pos[-1][0] + direction[0]
                next_y = initial_pos[-1][1] + direction[1]
                if 0 <= next_x < self.size and 0 <= next_y < self.size:
                    initial_pos.append((next_x, next_y))
                else:
                    break
            if len(initial_pos) == 3:
                initial_direction = (initial_pos[0][0] - initial_pos[1][0],
                                     initial_pos[0][1] - initial_pos[1][1])
                self.snake = Snake(initial_pos, initial_direction)
                break

    def place_apples(self):
        self.apples = []
        for _ in range(2):  # Two green apples
            self._place_apple("green")
        self._place_apple("red")  # One red apple

    def _place_apple(self, color: str):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.grid[x][y] == CellType.EMPTY:
                apple = Apple(color, (x, y))
                self.apples.append(apple)
                break

    def update_board(self):
        self.grid = [
            [CellType.EMPTY for _ in range(self.size)]
            for _ in range(self.size)
        ]
        # Place apples
        for apple in self.apples:
            apple_type = CellType.GREEN_APPLE if apple.color == "green" \
                else CellType.RED_APPLE
            x, y = apple.position
            self.grid[x][y] = apple_type
        # Place snake
        for segment in self.snake.body[1:]:
            self.grid[segment[0]][segment[1]] = CellType.SNAKE
        head = self.snake.body[0]
        self.grid[head[0]][head[1]] = CellType.HEAD

    def get_vision(self):
        """Get the snake's vision in all four directions for display."""
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
                cells_in_direction.append(CellType.WALL.value)
            vision[direction_name] = cells_in_direction
        return vision
