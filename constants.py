"""
Sudoku Game Constants
Author: Red Donaldson
Date: March 13, 2026
"""

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1000
BOARD_Y = 180

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
BLUE = (187, 222, 251)
DARK_BLUE = (102, 126, 234)
GREEN = (200, 230, 201)
RED = (255, 205, 210)
PURPLE = (118, 75, 162)
DARK_GREEN = (46, 125, 50)
DARK_RED = (198, 40, 40)
YELLOW = (255, 255, 200)
CYAN = (0, 255, 255)

# Font settings
FONT_NAME = 'ubuntumono'
FONT_FALLBACK = 'monospace'
FONT_SIZES = {
    'title': 52,
    'large': 38,
    'medium': 28,
    'small': 22,
    'button': 20
}

# Difficulty settings
DIFFICULTY_SETTINGS = {
    'easy': {
        'grid_size': 9,
        'box_size': 3,
        'symbols': list('123456789'),
        'cells_to_remove': 50,
        'lives': 3,
        'points_per_cell': 5
    },
    'medium': {
        'grid_size': 16,
        'box_size': 4,
        'symbols': list('0123456789ABCDEF'),
        'cells_to_remove': 190,
        'lives': 4,
        'points_per_cell': 10
    },
    'hard': {
        'grid_size': 25,
        'box_size': 5,
        'symbols': [chr(i) for i in range(ord('A'), ord('Z') + 1) if chr(i) != 'X'],
        'cells_to_remove': 520,
        'lives': 5,
        'points_per_cell': 15
    }
}

# Animation settings
ANIMATION_SPEED = 10  # frames per cell transition
FPS = 60
