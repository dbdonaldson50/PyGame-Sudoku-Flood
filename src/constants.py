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
HOVER_ORANGE = (255, 165, 80)  # Brighter orange for button hover
SELECTED_GLOW = (100, 150, 255)  # Glow color for selected cell
HIGHLIGHT_NUMBER = (255, 255, 200)  # Highlight for matching numbers
UNDO_COLOR = (150, 150, 150)  # Color for undo button
BUTTON_ORANGE = (255, 140, 0)  # Orange color for remaining digits button

# Font settings
# CRITICAL: Use true monospace fonts to ensure consistent character widths
# All digits and letters MUST have identical widths for proper alignment
# Testing shows Courier New provides perfect monospace consistency in Pygame
FONT_NAME = 'couriernew'          # Primary: Courier New (true monospace)
FONT_FALLBACK = 'monospace'       # Fallback: Generic monospace
# Note: ubuntumono has variable widths in Pygame (5-18px), avoid for grid display
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

# Main Menu settings
MENU_BG = (245, 245, 250)  # Light background for menu
MENU_TITLE_COLOR = PURPLE
MENU_SUBTITLE_COLOR = (100, 100, 100)
MENU_BUTTON_EASY = (100, 200, 100)  # Green for easy
MENU_BUTTON_MEDIUM = (255, 165, 0)  # Orange for medium
MENU_BUTTON_HARD = (220, 50, 50)  # Red for hard
MENU_BUTTON_HOVER_EASY = (130, 230, 130)
MENU_BUTTON_HOVER_MEDIUM = (255, 195, 50)
MENU_BUTTON_HOVER_HARD = (250, 80, 80)
MENU_BUTTON_SECONDARY = (150, 150, 150)  # Gray for secondary buttons
MENU_BUTTON_HOVER_SECONDARY = (180, 180, 180)

# Enhanced Scoring System
COMBO_MULTIPLIERS = [1.0, 1.5, 2.0, 2.5, 3.0]  # Multipliers for combo levels
COMBO_MAX_LEVEL = len(COMBO_MULTIPLIERS) - 1
COMBO_COLORS = [
    (100, 200, 100),  # 1x - Green
    (255, 215, 0),    # 1.5x - Gold
    (255, 165, 0),    # 2x - Orange
    (255, 100, 100),  # 2.5x - Red-Orange
    (255, 50, 255)    # 3x - Magenta
]

# Audio settings
AUDIO_DEFAULT_MUSIC_VOLUME = 0.5  # Default music volume (0.0 to 1.0)
AUDIO_DEFAULT_SFX_VOLUME = 0.7    # Default SFX volume (0.0 to 1.0)
AUDIO_FADE_TIME = 1000            # Fade time in milliseconds

# Visual Effect Settings
FLOATING_TEXT_SPEED = 2  # Pixels per frame
FLOATING_TEXT_DURATION = 45  # Frames (0.75 seconds at 60 FPS)
FLASH_DURATION = 20  # Frames for cell flash effect
FLASH_COLORS = {
    'correct': (100, 255, 100),   # Bright green for correct placement
    'auto_fill': (100, 200, 255),  # Blue for auto-filled cells
    'combo': (255, 215, 0),        # Gold for combo multiplier
}

# Bonus Point Settings
BONUS_ROW_COMPLETE = 50     # Bonus for completing a row
BONUS_COL_COMPLETE = 50     # Bonus for completing a column
BONUS_BOX_COMPLETE = 75     # Bonus for completing a box
BONUS_NUMBER_COMPLETE = 100 # Bonus for placing all of one number
COMBO_BONUS_BASE = 10       # Base bonus for maintaining combo
