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

# Enhanced UI colors
HOVER_BLUE = (140, 180, 255)  # Brighter blue for button hover
HOVER_GREEN = (100, 180, 100)  # Brighter green for button hover
HOVER_PURPLE = (150, 100, 200)  # Brighter purple for button hover
HOVER_RED = (230, 100, 100)  # Brighter red for button hover
SELECTED_GLOW = (100, 150, 255)  # Glow color for selected cell
HIGHLIGHT_NUMBER = (255, 255, 200)  # Highlight for matching numbers
UNDO_COLOR = (150, 150, 150)  # Color for undo button

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

# UI Enhancement settings
MAX_UNDO_HISTORY = 50  # Maximum number of moves to track for undo
GLOW_INTENSITY = 3  # Border width for selected cell glow
