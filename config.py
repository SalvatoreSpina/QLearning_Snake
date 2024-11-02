from enum import Enum

# Initial Configuration
CELL_SIZE = 50
BOARD_SIZE = 10
PANEL_WIDTH = 300
BACKGROUND_COLOR = (0, 0, 0)
HEAD_COLOR = (41, 128, 185)
SNAKE_COLOR = (40, 110, 110)
GREEN_APPLE_COLOR = (0, 128, 0)
RED_APPLE_COLOR = (255, 0, 0)
GRID_COLOR = (40, 40, 40)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 150)
BUTTON_HOVER_COLOR = (70, 70, 180)

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