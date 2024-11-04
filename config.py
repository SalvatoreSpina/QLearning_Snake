from enum import Enum

# Initial Configuration
CELL_SIZE = 50
BOARD_SIZE = 10
PANEL_WIDTH = 300

# Colors
BACKGROUND_COLOR = (0, 0, 0)
HEAD_COLOR = (41, 128, 185)
SNAKE_COLOR = (40, 110, 110)
GREEN_APPLE_COLOR = (0, 128, 0)
RED_APPLE_COLOR = (255, 0, 0)
GRID_COLOR = (40, 40, 40)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 150)
BUTTON_HOVER_COLOR = (70, 70, 180)


# Directions
class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


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
