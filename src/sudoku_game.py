#!/usr/bin/env python3
"""
Sudoku Game with Points and Lives System
Author: Red Donaldson
Date: March 13, 2026
"""

import pygame
import random
import copy
import sys

# Increase recursion limit for large grid generation
sys.setrecursionlimit(10000)

# Import game modules (handle both package and direct imports)
try:
    from .constants import *
    from . import game_logic
    from .ui_renderer import draw_game_screen, draw_main_menu
    from .audio_manager import AudioManager
except ImportError:
    from constants import *
    import game_logic
    from ui_renderer import draw_game_screen, draw_main_menu
    from audio_manager import AudioManager


class SudokuGame:
    def __init__(self):
        pygame.init()
        
        # Window settings
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Sudoku Flash")
        
        # Colors
        self.WHITE = WHITE
        self.BLACK = BLACK
        self.GRAY = GRAY
        self.LIGHT_GRAY = LIGHT_GRAY
        self.BLUE = BLUE
        self.DARK_BLUE = DARK_BLUE
        self.GREEN = GREEN
        self.RED = RED
        self.PURPLE = PURPLE
        self.DARK_GREEN = DARK_GREEN
        self.DARK_RED = DARK_RED
        self.YELLOW = YELLOW
        
        # Try to load Ubuntu Mono font, fallback to monospace
        # All fonts without bold and explicitly monospaced for consistent character sizing
        # Using bold=False and italic=False to ensure uniform rendering
        try:
            self.title_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['title'], bold=False, italic=False)
            self.large_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['large'], bold=False, italic=False)
            self.medium_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['medium'], bold=False, italic=False)
            self.small_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['small'], bold=False, italic=False)
            self.button_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['button'], bold=False, italic=False)
        except:
            # Fallback to monospace with same explicit settings
            self.title_font = pygame.font.SysFont(FONT_FALLBACK, FONT_SIZES['title'], bold=False, italic=False)
            self.large_font = pygame.font.SysFont(FONT_FALLBACK, FONT_SIZES['large'], bold=False, italic=False)
            self.medium_font = pygame.font.SysFont(FONT_FALLBACK, FONT_SIZES['medium'], bold=False, italic=False)
            self.small_font = pygame.font.SysFont(FONT_FALLBACK, FONT_SIZES['small'], bold=False, italic=False)
            self.button_font = pygame.font.SysFont(FONT_FALLBACK, FONT_SIZES['button'], bold=False, italic=False)
        
        # Board settings (will be updated per difficulty)
        self.BOARD_SIZE = 720
        self.BOARD_X = (self.WINDOW_WIDTH - self.BOARD_SIZE) // 2
        self.BOARD_Y = BOARD_Y
        
        # Game state
        self.board = []
        self.solution = []
        self.initial_board = []
        self.pencil_marks = []  # 2D array of sets for pencil marks
        self.undo_history = []  # List of (board_state, pencil_marks_state, score) tuples
        self.lives = 3
        self.max_lives = 3
        self.score = 0
        self.selected_cell = None
        self.pencil_mode = False  # Toggle for pencil vs pen mode
        self.admin_mode = False  # Toggle for admin mode (auto-shows correct values)
        self.difficulty = 'easy'
        self.grid_size = 9
        self.box_size = 3
        self.symbols = []
        self.cell_font = None
        self.pencil_font = None  # Smaller font for pencil marks
        self.seconds = 0
        self.game_over = False
        self.show_win_message = False
        self.show_lose_message = False
        self.message = ""
        self.message_color = self.BLACK
        self.message_timer = 0
        self.show_settings = False
        self.show_instructions = False  # Show how to play instructions
        self.show_credits = False  # Show audio credits
        self.show_remaining_digits = False  # Show remaining digits modal for large grids
        self.show_zoom_modal = False  # Show zoom modal for large grids
        self.zoom_center_cell = None  # (row, col) of center cell in zoom modal
        self.zoom_selected_cell = None  # Currently selected cell within zoom modal
        self.mouse_pos = (0, 0)  # Track mouse position for hover effects
        self.game_state = 'menu'  # 'menu' or 'playing'
        
        # Board generation state
        self.generating_board = False  # True while generating a new board
        self.generation_board = None  # Partial board being generated
        self.generation_progress = 0.0  # 0.0 to 1.0
        self.generation_spinner_angle = 0  # Spinner animation angle
        
        # Enhanced Scoring System
        self.combo_count = 0  # Current combo streak
        self.combo_multiplier = 1.0  # Current multiplier
        self.floating_points = []  # List of (x, y, points, color, timer) tuples
        self.animation_running_total = 0  # Running total of points during animation
        self.animation_cells_filled = 0  # Running count of cells filled during animation
        self.cell_flash_effects = []  # List of (row, col, color, timer) tuples
        self.last_action_triggered_combo = False  # Track if last action maintained combo
        
        # Animation state
        self.animation_queue = []
        self.current_animation_frame = 0
        self.animation_speed = ANIMATION_SPEED
        self.laser_particles = []
        self.laser_source = None
        
        # Difficulty settings
        self.difficulty_settings = DIFFICULTY_SETTINGS
        
        # Audio Manager
        self.audio = AudioManager()
        
        # Buttons
        self.buttons = {}
        self.create_buttons()
        
        # Timer
        self.clock = pygame.time.Clock()
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)
        
        # Start in menu state (don't auto-start game)
        # Game will start when user selects difficulty from menu
        
        # Start background music
        self.audio.play_music()
    
    def create_buttons(self):
        """Create button rectangles"""
        # Main menu buttons
        button_width = 300
        button_height = 120
        button_spacing = 30
        start_y = 280
        
        center_x = self.WINDOW_WIDTH // 2
        
        self.buttons['menu_easy'] = pygame.Rect(center_x - button_width // 2, start_y, 
                                                 button_width, button_height)
        self.buttons['menu_medium'] = pygame.Rect(center_x - button_width // 2, 
                                                   start_y + button_height + button_spacing,
                                                   button_width, button_height)
        self.buttons['menu_hard'] = pygame.Rect(center_x - button_width // 2, 
                                                 start_y + (button_height + button_spacing) * 2,
                                                 button_width, button_height)
        
        # How to Play button
        howto_width = 200
        howto_height = 50
        self.buttons['menu_howtoplay'] = pygame.Rect(center_x - howto_width // 2,
                                                      start_y + (button_height + button_spacing) * 3 + 20,
                                                      howto_width, howto_height)
        
        # Credits button
        credits_width = 240  # Widened to fit "Audio Credits" text (222px + margins)
        credits_height = 50
        self.buttons['menu_credits'] = pygame.Rect(center_x - credits_width // 2,
                                                    start_y + (button_height + button_spacing) * 3 + 80,
                                                    credits_width, credits_height)
        
        # Instruction modal - increased height to fit all instructions with proper spacing
        modal_width = 700  # Widened to prevent horizontal text overflow
        modal_height = 650  # Increased to accommodate text height + spacing
        modal_x = (self.WINDOW_WIDTH - modal_width) // 2
        modal_y = (self.WINDOW_HEIGHT - modal_height) // 2
        
        self.buttons['instructions_modal'] = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
        self.buttons['instructions_close'] = pygame.Rect(modal_x + modal_width - 50, modal_y + 10, 40, 40)
        
        # Control buttons (New Game, Hint, Undo, Settings, Remaining, Pencil) - fixed position
        # Note: "Remaining" button is always created but only drawn for large grids (16x16, 25x25)
        # FIX: Variable button widths to prevent text overflow - Red Donaldson, March 15, 2026
        button_widths = {
            'new_game': 72,    # "New" fits comfortably
            'hint': 72,        # "Hint" fits comfortably
            'undo': 72,        # "Undo" fits comfortably
            'settings': 120,   # "Settings" needs 116px, using 120px
            'remaining': 135,  # "Remaining" needs 128px, using 135px
            'pencil': 90       # "Pen/Pencil" mode button - Red Donaldson, March 17, 2026
        }
        button_height = 35
        button_y = 945  # Fixed position at bottom
        spacing = 8
        
        # FIX: Align buttons with text at top (x=80) - Red Donaldson, March 16, 2026
        # Matches left margin of Lives/Score/Time text for consistent layout
        start_x = 80
        
        # Create buttons with appropriate widths
        curr_x = start_x
        self.buttons['new_game'] = pygame.Rect(curr_x, button_y, button_widths['new_game'], button_height)
        curr_x += button_widths['new_game'] + spacing
        
        self.buttons['hint'] = pygame.Rect(curr_x, button_y, button_widths['hint'], button_height)
        curr_x += button_widths['hint'] + spacing
        
        self.buttons['undo'] = pygame.Rect(curr_x, button_y, button_widths['undo'], button_height)
        curr_x += button_widths['undo'] + spacing
        
        self.buttons['settings'] = pygame.Rect(curr_x, button_y, button_widths['settings'], button_height)
        curr_x += button_widths['settings'] + spacing
        
        self.buttons['remaining'] = pygame.Rect(curr_x, button_y, button_widths['remaining'], button_height)
        curr_x += button_widths['remaining'] + spacing
        
        self.buttons['pencil'] = pygame.Rect(curr_x, button_y, button_widths['pencil'], button_height)
        
        # Settings modal buttons
        # FIX: Increased modal width and button widths to prevent text overflow - Red Donaldson, March 15, 2026
        # Med (16x16) needs 163px, Hard (25x25) needs 176px, Check Solution needs 202px
        # FIX: Increased modal height to accommodate audio controls - Red Donaldson, March 16, 2026
        modal_width = 600  # Increased from 400 to accommodate wider buttons
        modal_height = 380  # Increased from 300 to fit volume sliders and sound toggle
        modal_x = (self.WINDOW_WIDTH - modal_width) // 2
        modal_y = (self.WINDOW_HEIGHT - modal_height) // 2
        
        self.buttons['settings_modal'] = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
        self.buttons['settings_close'] = pygame.Rect(modal_x + modal_width - 40, modal_y + 10, 30, 30)
        
        # Difficulty buttons - increased width to fit text comfortably
        diff_y = modal_y + 110
        diff_width = 180  # Increased from 115 to 180 to fit "Hard (25x25)" which needs 176px
        diff_spacing = 15
        diff_total_width = diff_width * 3 + diff_spacing * 2
        diff_start_x = modal_x + (modal_width - diff_total_width) // 2
        
        self.buttons['easy'] = pygame.Rect(diff_start_x, diff_y, diff_width, 35)
        self.buttons['medium'] = pygame.Rect(diff_start_x + diff_width + diff_spacing, 
                                       diff_y, diff_width, 35)
        self.buttons['hard'] = pygame.Rect(diff_start_x + (diff_width + diff_spacing) * 2, 
                                      diff_y, diff_width, 35)
        
        # FIX: Removed "Check Solution" button definition - Red Donaldson, March 15, 2026
        # Button removed from settings modal as it's redundant with instant lives feedback
        # No longer needed since players get immediate feedback on correct/wrong answers
        
        # Game over modal buttons
        gameover_modal_width = 450
        gameover_modal_height = 350  # Increased to fit buttons without overflow
        gameover_modal_x = (self.WINDOW_WIDTH - gameover_modal_width) // 2
        gameover_modal_y = (self.WINDOW_HEIGHT - gameover_modal_height) // 2
        
        self.buttons['gameover_modal'] = pygame.Rect(gameover_modal_x, gameover_modal_y, 
                                                      gameover_modal_width, gameover_modal_height)
        
        # New game button in game over modal
        newgame_width = 140
        newgame_x = gameover_modal_x + (gameover_modal_width - newgame_width) // 2
        self.buttons['gameover_newgame'] = pygame.Rect(newgame_x, gameover_modal_y + 240, 
                                                        newgame_width, 45)
        
        # Return to Menu button in game over modal
        menu_width = 140
        menu_x = gameover_modal_x + (gameover_modal_width - menu_width) // 2
        self.buttons['gameover_menu'] = pygame.Rect(menu_x, gameover_modal_y + 240 + 55, 
                                                     menu_width, 45)
        
        # Remaining digits modal (for large grids)
        remaining_modal_width = 500
        remaining_modal_height = 400
        remaining_modal_x = (self.WINDOW_WIDTH - remaining_modal_width) // 2
        remaining_modal_y = (self.WINDOW_HEIGHT - remaining_modal_height) // 2
        
        self.buttons['remaining_modal'] = pygame.Rect(remaining_modal_x, remaining_modal_y,
                                                       remaining_modal_width, remaining_modal_height)
        self.buttons['remaining_close'] = pygame.Rect(remaining_modal_x + remaining_modal_width - 40,
                                                       remaining_modal_y + 10, 30, 30)
        
        # Credits modal
        credits_modal_width = 750  # Widened to prevent horizontal text overflow
        credits_modal_height = 600
        credits_modal_x = (self.WINDOW_WIDTH - credits_modal_width) // 2
        credits_modal_y = (self.WINDOW_HEIGHT - credits_modal_height) // 2
        
        self.buttons['credits_modal'] = pygame.Rect(credits_modal_x, credits_modal_y,
                                                     credits_modal_width, credits_modal_height)
        self.buttons['credits_close'] = pygame.Rect(credits_modal_x + credits_modal_width - 50,
                                                     credits_modal_y + 10, 40, 40)
        
        # Zoom modal for large grids (5x5 or 7x7 view of adjacent cells)
        zoom_modal_width = 600
        zoom_modal_height = 600
        zoom_modal_x = (self.WINDOW_WIDTH - zoom_modal_width) // 2
        zoom_modal_y = (self.WINDOW_HEIGHT - zoom_modal_height) // 2
        
        self.buttons['zoom_modal'] = pygame.Rect(zoom_modal_x, zoom_modal_y,
                                                  zoom_modal_width, zoom_modal_height)
        self.buttons['zoom_close'] = pygame.Rect(zoom_modal_x + zoom_modal_width - 40,
                                                  zoom_modal_y + 10, 30, 30)
        
        # Volume sliders in settings modal (will be added programmatically)
        # FIX: Adjusted positions to prevent label/slider overlap - Red Donaldson, March 16, 2026
        # Labels at y=165 and y=210, sliders at y=185 and y=230
        slider_y = modal_y + 185  # Changed from 180 to give space for label above
        slider_width = 400
        slider_height = 8
        slider_x = modal_x + (modal_width - slider_width) // 2
        
        self.buttons['music_slider'] = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
        self.buttons['sfx_slider'] = pygame.Rect(slider_x, slider_y + 45, slider_width, slider_height)
        
        # Sound toggle button in settings - positioned below volume sliders
        sound_toggle_width = 150
        sound_toggle_x = modal_x + (modal_width - sound_toggle_width) // 2
        self.buttons['sound_toggle'] = pygame.Rect(sound_toggle_x, modal_y + 260, sound_toggle_width, 35)
    
    def update_cell_font(self):
        """Update cell font size based on grid size with proper spacing"""
        # Calculate cell size to determine safe font sizes
        cell_size = self.BOARD_SIZE // self.grid_size
        
        # Font size should be ~50-60% of cell height for comfortable fit
        # This prevents overlap while maintaining readability
        if self.grid_size == 9:
            font_size = 38  # Reduced from 40 for better spacing
        elif self.grid_size == 16:
            font_size = 26  # Reduced from 28 for better spacing
        else:  # 25
            font_size = 17  # Reduced from 20 to prevent tight fit
        
        # Calculate pencil mark size based on cell size
        # Each pencil mark occupies 1/box_size of the cell dimension
        # Font should be ~60-65% of that slot to leave spacing
        pencil_slot_size = cell_size / self.box_size
        pencil_size = int(pencil_slot_size * 0.62)  # Reduced from 68% for better spacing
        
        # Both fonts explicitly non-bold, non-italic for consistent character sizing
        # Critical: monospace fonts ensure all characters have identical widths
        try:
            self.cell_font = pygame.font.SysFont(FONT_NAME, font_size, bold=False, italic=False)
            self.pencil_font = pygame.font.SysFont(FONT_NAME, pencil_size, bold=False, italic=False)
        except:
            self.cell_font = pygame.font.SysFont(FONT_FALLBACK, font_size, bold=False, italic=False)
            self.pencil_font = pygame.font.SysFont(FONT_FALLBACK, pencil_size, bold=False, italic=False)
    
    def new_game(self):
        """Start a new game"""
        self.game_over = False
        self.show_win_message = False
        
        # Reset combo system
        self.combo_count = 0
        self.combo_multiplier = 1.0
        self.floating_points = []
        self.cell_flash_effects = []
        self.last_action_triggered_combo = False
        self.show_lose_message = False
        self.show_settings = False  # Close settings modal when starting new game
        self.show_remaining_digits = False  # FIX: Close remaining digits modal when starting new game - Red Donaldson
        self.game_state = 'playing'  # Set to playing state
        self.score = 0
        self.seconds = 0
        self.pencil_mode = False
        self.admin_mode = False  # Reset admin mode on new game
        self.undo_history = []  # Clear undo history on new game
        
        # Update grid settings based on difficulty
        settings = self.difficulty_settings[self.difficulty]
        self.grid_size = settings['grid_size']
        self.box_size = settings['box_size']
        self.symbols = settings['symbols']
        self.max_lives = settings['lives']
        self.lives = self.max_lives
        
        # Update board size to ensure cells divide evenly
        if self.grid_size == 9:
            self.BOARD_SIZE = 720  # 720/9 = 80px per cell
        elif self.grid_size == 16:
            self.BOARD_SIZE = 720  # 720/16 = 45px per cell
        else:  # 25
            self.BOARD_SIZE = 700  # 700/25 = 28px per cell
        
        self.BOARD_X = (self.WINDOW_WIDTH - self.BOARD_SIZE) // 2
        
        # Update cell font
        self.update_cell_font()
        
        # Generate puzzle with visual feedback
        self.generating_board = True
        self.generation_board = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.generation_progress = 0.0
        self.generation_spinner_angle = 0
        last_render_time = [0]  # Track last render time for throttling
        render_count = [0]  # Track number of renders to reduce deepcopy frequency
        
        # Define progress callback with time-based throttling
        # CRITICAL FIX: Removed deepcopy to prevent memory exhaustion - Red Donaldson, March 17, 2026
        def progress_callback(board, progress):
            import time
            current_time = time.time()
            
            # If progress is None, it's a spinner-only update during backtracking
            if progress is None:
                self.generation_spinner_angle = (self.generation_spinner_angle + 3) % 360  # Slower rotation
                # Only render occasionally during backtracking to avoid slowdown
                if current_time - last_render_time[0] >= 0.2:  # 5fps for spinner during backtracking
                    last_render_time[0] = current_time
                    from ui_renderer import draw_generation_screen
                    draw_generation_screen(self)
                    pygame.display.flip()
                return
            
            # Only render if at least 100ms has passed since last render
            # This prevents excessive rendering while still keeping UI responsive
            if current_time - last_render_time[0] < 0.1 and progress < 0.99:
                # Still update progress without rendering
                self.generation_progress = progress
                return
            
            last_render_time[0] = current_time
            render_count[0] += 1
            
            # CRITICAL: Copy board frequently during early phase (diagonal filling),
            # then reduce to every 10th render to save memory and prevent crashes
            # Fixed for 16x16 crashes by: Red Donaldson, March 17, 2026
            # 
            # Early phase (< 40%): Copy every render to show diagonal pattern
            # Mid phase (40-80%): Copy every 5th render to balance visibility and memory
            # Late phase (> 80%): Copy every 10th render to minimize memory pressure
            # Always copy at 99% to show final state
            if progress < 0.40:
                # Show diagonal filling phase clearly
                self.generation_board = copy.deepcopy(board)
            elif progress < 0.80:
                # Balance between visual updates and memory conservation
                if render_count[0] % 5 == 0:
                    self.generation_board = copy.deepcopy(board)
            elif render_count[0] % 10 == 0 or progress >= 0.99:
                # Minimize memory pressure during heavy backtracking
                self.generation_board = copy.deepcopy(board)
            
            self.generation_progress = progress
            self.generation_spinner_angle = (self.generation_spinner_angle + 3) % 360  # Slower rotation
            
            # Render the generation screen
            from ui_renderer import draw_generation_screen
            draw_generation_screen(self)
            pygame.display.flip()
            
            # Process events to keep UI responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
        # Generate puzzle
        self.solution = game_logic.generate_complete_sudoku(
            self.grid_size, self.box_size, self.symbols, progress_callback
        )
        
        self.generating_board = False
        
        self.board = copy.deepcopy(self.solution)
        game_logic.remove_numbers(
            self.board, self.grid_size, settings['cells_to_remove']
        )
        self.initial_board = copy.deepcopy(self.board)
        
        # Initialize pencil marks (empty sets for each cell)
        self.pencil_marks = [[set() for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        self.selected_cell = None
        # No message needed - new game is obvious from board reset
    
    def auto_fill_singles(self, source_cell=None, award_points=True):
        """Auto-fill cells that have only one possible value with combo system"""
        filled_sequence = game_logic.find_auto_fill_cells(
            self.board, self.initial_board, self.grid_size, 
            self.box_size, self.symbols, source_cell
        )
        
        filled_count = len(filled_sequence)
        
        # Award points with combo multiplier for auto-filled cells
        if filled_count > 0 and award_points:
            base_points = self.difficulty_settings[self.difficulty]['points_per_cell']
            total_points = 0
            
            # Calculate points for each cell (but don't show effects yet)
            # Effects will be shown sequentially during animation
            for idx, (row, col, value) in enumerate(filled_sequence):
                # Update combo multiplier
                self.update_combo(increment=True)
                
                # Calculate points for this cell with current multiplier
                cell_points = int((base_points // 2) * self.combo_multiplier)
                total_points += cell_points
            
            # Award total points
            self.score += total_points
            
            # Check for completion bonuses
            bonus_points = self.check_completion_bonuses()
            if bonus_points > 0:
                self.score += bonus_points
                # Add floating text at top center for bonus
                self.add_floating_points(
                    self.WINDOW_WIDTH // 2, 
                    150, 
                    bonus_points, 
                    (255, 215, 0)  # Gold for bonuses
                )
            
            # Don't show message upfront - it will count up during animation
            # Reset running totals for animation
            self.animation_running_total = 0
            self.animation_cells_filled = 0
            
            # Start animation with visual effects data
            self.start_animation(filled_sequence, source_cell, base_points)
            self.last_action_triggered_combo = True
        else:
            # No auto-fill means combo breaks
            if award_points:  # Only break combo for user actions
                self.reset_combo()
                self.last_action_triggered_combo = False
        
        return filled_count
    
    def start_animation(self, filled_sequence, source_cell=None, base_points=0):
        """Initialize animation for auto-filled cells with visual effects data"""
        if not filled_sequence:
            return
        
        # Build animation queue with effect data for each cell
        # Each entry: (row, col, value, points, combo_level)
        self.animation_queue = []
        combo_tracker = self.combo_count - len(filled_sequence)  # Start from before the fill
        
        for row, col, value in filled_sequence:
            combo_tracker += 1
            # Ensure combo_tracker stays within valid bounds [0, COMBO_MAX_LEVEL]
            combo_tracker = max(0, min(combo_tracker, COMBO_MAX_LEVEL))
            
            # Calculate points with combo multiplier
            multiplier = COMBO_MULTIPLIERS[combo_tracker]
            cell_points = int((base_points // 2) * multiplier)
            
            self.animation_queue.append((row, col, value, cell_points, combo_tracker))
        
        self.current_animation_frame = 0
        
        # Set laser source to the user's cell if provided
        if source_cell:
            self.laser_source = source_cell
        else:
            # Place first cell immediately and use it as laser source
            row, col, value, points, combo_level = self.animation_queue[0]
            self.board[row][col] = value
            self.pencil_marks[row][col].clear()
            self.laser_source = (row, col)
            self.animation_queue.pop(0)
    
    def update_animation(self):
        """Update animation state each frame - sequential cell filling with effects"""
        if not self.animation_queue:
            return
        
        self.current_animation_frame += 1
        
        # Move to next cell in animation
        if self.current_animation_frame >= self.animation_speed:
            self.current_animation_frame = 0
            
            # Fill the first cell in queue with visual effects
            if self.animation_queue:
                row, col, value, points, combo_level = self.animation_queue[0]
                
                # Place the cell
                self.board[row][col] = value
                self.pencil_marks[row][col].clear()
                
                # Add visual effects for this specific cell
                cell_size = self.BOARD_SIZE // self.grid_size
                x = self.BOARD_X + col * cell_size + cell_size // 2
                y = self.BOARD_Y + row * cell_size + cell_size // 2
                
                # Color based on combo level
                point_color = COMBO_COLORS[combo_level]
                
                # Show points floating from this cell
                self.add_floating_points(x, y, points, point_color)
                
                # Add green flash effect
                flash_type = 'combo' if combo_level > 0 else 'auto_fill'
                self.add_cell_flash(row, col, flash_type)
                
                # Update running totals and show incremental message
                self.animation_running_total += points
                self.animation_cells_filled += 1
                
                # Show incremental combo message as cells are filled
                if combo_level > 0:
                    combo_text = f"+{self.animation_running_total} pts ({self.animation_cells_filled} filled) {COMBO_MULTIPLIERS[combo_level]:.1f}x COMBO!"
                    self.show_message(combo_text, COMBO_COLORS[combo_level])
                else:
                    self.show_message(f"+{self.animation_running_total} pts ({self.animation_cells_filled} filled)", self.DARK_BLUE)
                
                # Update laser source to this cell for next animation frame
                self.laser_source = (row, col)
                self.animation_queue.pop(0)
            
            # Check if animation is complete
            if not self.animation_queue:
                self.laser_source = None
                if game_logic.is_puzzle_complete(self.board, self.solution, self.grid_size):
                    self.win_game()
    
    def update_combo(self, increment=True):
        """Update combo counter and multiplier"""
        if increment:
            old_combo = self.combo_count
            self.combo_count = min(self.combo_count + 1, COMBO_MAX_LEVEL)
            self.combo_multiplier = COMBO_MULTIPLIERS[self.combo_count]
            
            # Play combo sound when reaching a new multiplier level
            if self.combo_count > old_combo and self.combo_count >= 1:
                self.audio.play_sound('combo')
        else:
            self.combo_count = 0
            self.combo_multiplier = COMBO_MULTIPLIERS[0]
    
    def reset_combo(self):
        """Reset combo to zero"""
        self.update_combo(increment=False)
    
    def calculate_potential_combo(self, row, col):
        """Calculate how many cells would auto-fill if we place the correct value
        
        Added by: Red Donaldson
        Date: March 17, 2026
        
        Args:
            row: Row of the cell to test
            col: Column of the cell to test
        
        Returns:
            int: Number of cells that would auto-fill (combo length)
        """
        # Only calculate for empty cells
        if self.board[row][col] is not None:
            return 0
        
        # Create a temporary board with the correct value placed
        temp_board = [r[:] for r in self.board]
        temp_board[row][col] = self.solution[row][col]
        
        # Find cells that would auto-fill
        filled_sequence = game_logic.find_auto_fill_cells(
            temp_board, self.initial_board, self.grid_size, self.box_size, self.symbols, (row, col)
        )
        
        return len(filled_sequence)
    
    def add_floating_points(self, x, y, points, color):
        """Add a floating point animation"""
        self.floating_points.append({
            'x': x,
            'y': y,
            'points': points,
            'color': color,
            'timer': FLOATING_TEXT_DURATION
        })
    
    def add_cell_flash(self, row, col, flash_type='correct'):
        """Add a cell flash effect"""
        color = FLASH_COLORS.get(flash_type, FLASH_COLORS['correct'])
        self.cell_flash_effects.append({
            'row': row,
            'col': col,
            'color': color,
            'timer': FLASH_DURATION
        })
    
    def update_floating_points(self):
        """Update floating point animations"""
        for point_data in self.floating_points[:]:
            point_data['y'] -= FLOATING_TEXT_SPEED
            point_data['timer'] -= 1
            
            if point_data['timer'] <= 0:
                self.floating_points.remove(point_data)
    
    def update_cell_flashes(self):
        """Update cell flash effects"""
        for flash_data in self.cell_flash_effects[:]:
            flash_data['timer'] -= 1
            
            if flash_data['timer'] <= 0:
                self.cell_flash_effects.remove(flash_data)
    
    def check_completion_bonuses(self):
        """Check for and return completion bonuses"""
        bonus = 0
        
        # Check for completed rows
        for i in range(self.grid_size):
            if all(self.board[i][j] == self.solution[i][j] for j in range(self.grid_size)):
                # Check if this row was just completed (has at least one newly placed cell)
                row_is_new = True  # Simplified - could track which rows are already complete
                if row_is_new:
                    bonus += BONUS_ROW_COMPLETE
        
        # Check for completed columns
        for j in range(self.grid_size):
            if all(self.board[i][j] == self.solution[i][j] for i in range(self.grid_size)):
                col_is_new = True
                if col_is_new:
                    bonus += BONUS_COL_COMPLETE
        
        # Check for completed boxes
        for box_row in range(0, self.grid_size, self.box_size):
            for box_col in range(0, self.grid_size, self.box_size):
                box_complete = True
                for i in range(box_row, box_row + self.box_size):
                    for j in range(box_col, box_col + self.box_size):
                        if self.board[i][j] != self.solution[i][j]:
                            box_complete = False
                            break
                    if not box_complete:
                        break
                
                if box_complete:
                    bonus += BONUS_BOX_COMPLETE
        
        # Check for completed numbers (all instances of a symbol placed)
        for symbol in self.symbols:
            symbol_complete = True
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if self.solution[i][j] == symbol and self.board[i][j] != symbol:
                        symbol_complete = False
                        break
                if not symbol_complete:
                    break
            
            if symbol_complete:
                bonus += BONUS_NUMBER_COMPLETE
        
        return bonus
    
    def get_cell_from_pos(self, pos):
        """Get cell coordinates from mouse position"""
        x, y = pos
        
        if x < self.BOARD_X or x > self.BOARD_X + self.BOARD_SIZE:
            return None
        if y < self.BOARD_Y or y > self.BOARD_Y + self.BOARD_SIZE:
            return None
        
        cell_size = self.BOARD_SIZE // self.grid_size
        col = (x - self.BOARD_X) // cell_size
        row = (y - self.BOARD_Y) // cell_size
        
        return (row, col)
    
    def get_zoom_cell_from_pos(self, pos):
        """Get cell coordinates from mouse position within zoom modal"""
        if not self.show_zoom_modal or self.zoom_center_cell is None:
            return None
        
        x, y = pos
        modal = self.buttons['zoom_modal']
        
        # Determine zoom grid size (5x5 for 16x16, 7x7 for 25x25)
        zoom_size = 5 if self.grid_size == 16 else 7
        
        # Calculate available space for grid (leave margins for title and close button)
        grid_area_size = min(modal.width - 40, modal.height - 80)
        cell_size = grid_area_size // zoom_size
        
        # Center the grid in the modal
        grid_x = modal.centerx - (cell_size * zoom_size) // 2
        grid_y = modal.top + 60
        
        # Check if click is within the grid
        if x < grid_x or x > grid_x + cell_size * zoom_size:
            return None
        if y < grid_y or y > grid_y + cell_size * zoom_size:
            return None
        
        # Calculate which cell in the zoom view was clicked
        zoom_col = (x - grid_x) // cell_size
        zoom_row = (y - grid_y) // cell_size
        
        # Convert to actual board coordinates
        center_row, center_col = self.zoom_center_cell
        offset = zoom_size // 2
        
        actual_row = center_row - offset + zoom_row
        actual_col = center_col - offset + zoom_col
        
        # Make sure it's within bounds
        if actual_row < 0 or actual_row >= self.grid_size:
            return None
        if actual_col < 0 or actual_col >= self.grid_size:
            return None
        
        return (actual_row, actual_col)
    
    def place_number(self, symbol):
        """Place a number in the selected cell or add pencil mark"""
        if self.game_over or self.selected_cell is None:
            return
        
        row, col = self.selected_cell
        
        if self.initial_board[row][col] is not None:
            return
        
        # Save state before making changes (for undo)
        if symbol != 0 or self.board[row][col] is not None or self.pencil_marks[row][col]:
            self.save_state()
        
        # Convert number to string symbol if needed
        if isinstance(symbol, int):
            if symbol == 0:
                # Erase - clear both board and pencil marks
                self.board[row][col] = None
                self.pencil_marks[row][col].clear()
                return
            # Convert to appropriate symbol
            if self.grid_size == 9 and 1 <= symbol <= 9:
                symbol = str(symbol)
            elif self.grid_size == 16 and 0 <= symbol <= 9:
                symbol = str(symbol)
            elif self.grid_size >= 16:
                return  # Invalid for larger grids
        
        # Pencil mode - add/remove from pencil marks
        if self.pencil_mode:
            if symbol in self.pencil_marks[row][col]:
                self.pencil_marks[row][col].remove(symbol)
            else:
                self.pencil_marks[row][col].add(symbol)
            return
        
        # Pen mode - place the number
        is_correct = self.solution[row][col] == symbol
        
        if is_correct:
            self.board[row][col] = symbol
            self.pencil_marks[row][col].clear()  # Clear pencil marks when placing
            points = self.difficulty_settings[self.difficulty]['points_per_cell']
            self.score += points
            
            # Play correct sound
            self.audio.play_sound('correct')
            
            # Add visual feedback
            self.add_floating_points(
                self.BOARD_X + col * (self.BOARD_SIZE // self.grid_size) + (self.BOARD_SIZE // self.grid_size) // 2,
                self.BOARD_Y + row * (self.BOARD_SIZE // self.grid_size) + (self.BOARD_SIZE // self.grid_size) // 2,
                points,
                FLASH_COLORS['correct']
            )
            self.add_cell_flash(row, col, 'correct')
            
            auto_filled = self.auto_fill_singles(source_cell=(row, col))
            
            # Close zoom modal if flood-fill triggered
            if auto_filled > 0 and self.show_zoom_modal:
                self.show_zoom_modal = False
                self.zoom_selected_cell = None
            
            if auto_filled == 0:
                # No auto-fill, so show simple message and reset combo
                self.show_message(f"Correct! +{points} points", self.DARK_GREEN)
                self.reset_combo()
            
            if game_logic.is_puzzle_complete(self.board, self.solution, self.grid_size):
                self.win_game()
        else:
            self.lives -= 1
            self.reset_combo()  # Wrong move resets combo
            
            # Play wrong sound
            self.audio.play_sound('wrong')
            
            self.show_message("Wrong! -1 life", self.DARK_RED)
            
            if self.lives <= 0:
                self.lose_game()
    
    def handle_cell_input(self, char):
        """Handle character input for all grid sizes"""
        if self.game_over or self.selected_cell is None:
            return
        
        row, col = self.selected_cell
        
        if self.initial_board[row][col] is not None:
            return
        
        # Save state before making changes (for undo)
        self.save_state()
        
        # Convert to uppercase and check if valid symbol
        char = char.upper()
        if char in self.symbols:
            # Pencil mode - add/remove from pencil marks
            if self.pencil_mode:
                if char in self.pencil_marks[row][col]:
                    self.pencil_marks[row][col].remove(char)
                else:
                    self.pencil_marks[row][col].add(char)
            else:
                # Pen mode - place the value
                is_correct = self.solution[row][col] == char
                
                if is_correct:
                    self.board[row][col] = char
                    self.pencil_marks[row][col].clear()  # Clear pencil marks
                    points = self.difficulty_settings[self.difficulty]['points_per_cell']
                    self.score += points
                    
                    # Play correct sound
                    self.audio.play_sound('correct')
                    
                    # Add visual feedback
                    cell_size = self.BOARD_SIZE // self.grid_size
                    self.add_floating_points(
                        self.BOARD_X + col * cell_size + cell_size // 2,
                        self.BOARD_Y + row * cell_size + cell_size // 2,
                        points,
                        FLASH_COLORS['correct']
                    )
                    self.add_cell_flash(row, col, 'correct')
                    
                    auto_filled = self.auto_fill_singles(source_cell=(row, col))
                    
                    if auto_filled == 0:
                        self.show_message(f"Correct! +{points} points", self.DARK_GREEN)
                        self.reset_combo()
                    
                    if game_logic.is_puzzle_complete(self.board, self.solution, self.grid_size):
                        self.win_game()
                else:
                    self.lives -= 1
                    self.reset_combo()  # Wrong move resets combo
                    
                    # Play wrong sound
                    self.audio.play_sound('wrong')
                    
                    self.show_message("Wrong! -1 life", self.DARK_RED)
                    
                    if self.lives <= 0:
                        self.lose_game()
    
    def toggle_pencil_mode(self):
        """Toggle between pencil and pen mode"""
        self.pencil_mode = not self.pencil_mode
        mode = "Pencil" if self.pencil_mode else "Pen"
        self.show_message(f"{mode} mode", self.DARK_BLUE)
    
    def toggle_admin_mode(self):
        """Toggle admin mode - automatically shows correct values as pencil marks"""
        self.admin_mode = not self.admin_mode
        
        if self.admin_mode:
            # Populate all empty cells with correct values as pencil marks
            self.populate_admin_pencil_marks()
            self.show_message("Admin Mode: ON (Showing correct values)", CYAN)
        else:
            # Remove only the correct values from pencil marks (preserve user's manual marks)
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if self.board[i][j] is None:
                        correct_value = self.solution[i][j]
                        # Remove the correct value if it exists
                        self.pencil_marks[i][j].discard(correct_value)
            self.show_message("Admin Mode: OFF", self.BLACK)
    
    def populate_admin_pencil_marks(self):
        """Automatically populate pencil marks with correct values for empty cells"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Only add pencil marks for empty cells
                if self.board[i][j] is None:
                    correct_value = self.solution[i][j]
                    # Add correct value to existing pencil marks (don't replace)
                    self.pencil_marks[i][j].add(correct_value)
    
    def save_state(self):
        """Save current board state for undo"""
        # Deep copy the board and pencil marks
        board_copy = copy.deepcopy(self.board)
        pencil_copy = copy.deepcopy(self.pencil_marks)
        
        self.undo_history.append((board_copy, pencil_copy, self.score))
        
        # Limit history size
        if len(self.undo_history) > MAX_UNDO_HISTORY:
            self.undo_history.pop(0)
    
    def undo(self):
        """Undo the last move"""
        if self.game_over:
            return
        
        if not self.undo_history:
            self.show_message("Nothing to undo!", self.DARK_RED)
            return
        
        # Restore previous state
        board_state, pencil_state, score_state = self.undo_history.pop()
        self.board = copy.deepcopy(board_state)
        self.pencil_marks = copy.deepcopy(pencil_state)
        self.score = score_state
        
        # Play undo sound
        self.audio.play_sound('undo')
        
        self.show_message("Move undone!", self.DARK_BLUE)
    
    def give_hint(self):
        """Give a hint by revealing one cell"""
        if self.game_over:
            return
        
        if self.score >= 10:
            self.score -= 10
            
            empty_cells = []
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if self.board[i][j] is None:
                        empty_cells.append((i, j))
            
            if empty_cells:
                row, col = random.choice(empty_cells)
                self.board[row][col] = self.solution[row][col]
                self.pencil_marks[row][col].clear()  # Clear pencil marks when placing hint
                
                # Play hint sound
                self.audio.play_sound('hint')
                
                auto_filled = self.auto_fill_singles(source_cell=(row, col), award_points=False)
                
                if auto_filled == 0:
                    self.show_message("Hint given! -10 points", self.DARK_BLUE)
                
                if game_logic.is_puzzle_complete(self.board, self.solution, self.grid_size):
                    self.win_game()
            else:
                self.show_message("No empty cells left!", self.DARK_BLUE)
        else:
            self.show_message("Need at least 10 points for hint!", self.DARK_RED)
    
    def check_solution(self):
        """Check the current solution status"""
        if self.game_over:
            return
        
        correct_count, total_filled, wrong_count = game_logic.check_solution_status(
            self.board, self.solution, self.initial_board, self.grid_size
        )
        
        if total_filled == 0:
            self.show_message("No cells filled yet!", self.DARK_BLUE)
        elif correct_count == total_filled:
            self.show_message(f"All {total_filled} cells are correct!", self.DARK_GREEN)
        else:
            self.show_message(f"{correct_count} correct, {wrong_count} wrong", self.DARK_RED)
    
    def win_game(self):
        
        # Play win sound
        self.audio.play_sound('win')
        
        """Handle winning the game"""
        self.game_over = True
        self.show_win_message = True
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        self.message = f"You Won!\nScore: {self.score}\nTime: {minutes:02d}:{seconds:02d}"
        self.message_color = self.DARK_GREEN
    
    def lose_game(self):
        """Handle losing the game"""
        self.game_over = True
        self.show_lose_message = True
        self.message = f"Game Over!\nOut of lives\nFinal Score: {self.score}"
        self.message_color = self.DARK_RED
    
    def start_game_with_difficulty(self, difficulty):
        """Start a new game with specified difficulty"""
        self.difficulty = difficulty
        self.new_game()
    
    def show_message(self, text, color):
        """Display a temporary message"""
        self.message = text
        self.message_color = color
        self.message_timer = 180  # 3 seconds at 60 FPS
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        # Update mouse position for hover effects
        self.mouse_pos = pos
        
        # Handle menu state
        if self.game_state == 'menu':
            # Check for credits modal
            if self.show_credits:
                if self.buttons['credits_modal'].collidepoint(pos):
                    if self.buttons['credits_close'].collidepoint(pos):
                        self.show_credits = False
                        self.audio.play_sound('button')
                    return
                else:
                    self.show_credits = False
                    return
            
            # Check for instruction modal
            if self.show_instructions:
                if self.buttons['instructions_modal'].collidepoint(pos):
                    if self.buttons['instructions_close'].collidepoint(pos):
                        self.show_instructions = False
                        self.audio.play_sound('button')
                    return
                else:
                    self.show_instructions = False
                    return
            
            # Check menu buttons
            if self.buttons['menu_easy'].collidepoint(pos):
                self.audio.play_sound('button')
                self.start_game_with_difficulty('easy')
            elif self.buttons['menu_medium'].collidepoint(pos):
                self.audio.play_sound('button')
                self.start_game_with_difficulty('medium')
            elif self.buttons['menu_hard'].collidepoint(pos):
                self.audio.play_sound('button')
                self.start_game_with_difficulty('hard')
            elif self.buttons['menu_howtoplay'].collidepoint(pos):
                self.audio.play_sound('button')
                self.show_instructions = True
            elif self.buttons['menu_credits'].collidepoint(pos):
                self.audio.play_sound('button')
                self.show_credits = True
            return
        
        # Handle game over modal
        if self.show_win_message or self.show_lose_message:
            if self.buttons['gameover_modal'].collidepoint(pos):
                if self.buttons['gameover_newgame'].collidepoint(pos):
                    self.audio.play_sound('button')
                    self.new_game()
                elif self.buttons['gameover_menu'].collidepoint(pos):
                    self.audio.play_sound('button')
                    self.game_state = 'menu'
                    self.show_win_message = False
                    self.show_lose_message = False
                return
            else:
                # Click outside modal closes it
                self.show_win_message = False
                self.show_lose_message = False
                return
        
        if self.show_settings:
            # Handle settings modal
            if self.buttons['settings_modal'].collidepoint(pos):
                if self.buttons['settings_close'].collidepoint(pos):
                    self.audio.play_sound('button')
                    self.show_settings = False
                elif self.buttons['easy'].collidepoint(pos):
                    self.audio.play_sound('button')
                    if self.difficulty != 'easy':
                        self.difficulty = 'easy'
                        self.new_game()
                elif self.buttons['medium'].collidepoint(pos):
                    self.audio.play_sound('button')
                    if self.difficulty != 'medium':
                        self.difficulty = 'medium'
                        self.new_game()
                elif self.buttons['hard'].collidepoint(pos):
                    self.audio.play_sound('button')
                    if self.difficulty != 'hard':
                        self.difficulty = 'hard'
                        self.new_game()
                elif self.buttons['sound_toggle'].collidepoint(pos):
                    enabled = self.audio.toggle_sound()
                    status = "ON" if enabled else "OFF"
                    self.show_message(f"Sound {status}", self.DARK_BLUE)
                # Check if clicking on volume sliders
                elif self.buttons['music_slider'].collidepoint(pos):
                    # Calculate volume from click position
                    slider_rect = self.buttons['music_slider']
                    relative_x = pos[0] - slider_rect.x
                    volume = relative_x / slider_rect.width
                    self.audio.set_music_volume(volume)
                elif self.buttons['sfx_slider'].collidepoint(pos):
                    # Calculate volume from click position
                    slider_rect = self.buttons['sfx_slider']
                    relative_x = pos[0] - slider_rect.x
                    volume = relative_x / slider_rect.width
                    self.audio.set_sfx_volume(volume)
                    # Play a test sound
                    self.audio.play_sound('button')
                # FIX: Removed 'check' button handler - Red Donaldson, March 15, 2026
                # Check Solution feature removed as redundant with lives system
                # Players get instant feedback: wrong = lose life, correct = gain points
                return
            else:
                self.show_settings = False
                return
        
        if self.show_remaining_digits:
            # Handle remaining digits modal
            if self.buttons['remaining_modal'].collidepoint(pos):
                if self.buttons['remaining_close'].collidepoint(pos):
                    self.audio.play_sound('button')
                    self.show_remaining_digits = False
                return
            else:
                self.show_remaining_digits = False
                return
        
        if self.show_zoom_modal:
            # Handle zoom modal
            if self.buttons['zoom_modal'].collidepoint(pos):
                if self.buttons['zoom_close'].collidepoint(pos):
                    self.audio.play_sound('button')
                    self.show_zoom_modal = False
                    self.zoom_selected_cell = None
                    return
                # Check if clicking on a cell within the zoom modal
                zoom_cell = self.get_zoom_cell_from_pos(pos)
                if zoom_cell:
                    row, col = zoom_cell
                    if self.initial_board[row][col] is None:
                        self.zoom_selected_cell = zoom_cell
                        # Also update main selected cell for consistency
                        self.selected_cell = zoom_cell
                    return
            else:
                self.show_zoom_modal = False
                self.zoom_selected_cell = None
                return
        
        # Check board cells
        cell = self.get_cell_from_pos(pos)
        if cell:
            row, col = cell
            if self.initial_board[row][col] is None:
                # For large grids, open zoom modal instead of just selecting
                if self.grid_size > 9:
                    self.zoom_center_cell = cell
                    self.zoom_selected_cell = cell
                    self.selected_cell = cell
                    self.show_zoom_modal = True
                    self.audio.play_sound('button')
                else:
                    self.selected_cell = cell
            return
        
        # Check buttons
        if self.buttons['new_game'].collidepoint(pos):
            self.audio.play_sound('button')
            self.new_game()
        elif self.buttons['hint'].collidepoint(pos):
            self.give_hint()
        elif self.buttons['undo'].collidepoint(pos):
            self.undo()
        elif self.buttons['settings'].collidepoint(pos):
            self.audio.play_sound('button')
            self.show_settings = True
        elif 'remaining' in self.buttons and self.buttons['remaining'].collidepoint(pos):
            # Only handle click if button exists (defensive check) and for large grids
            if self.grid_size > 9:
                self.audio.play_sound('button')
                self.show_remaining_digits = True
        elif 'pencil' in self.buttons and self.buttons['pencil'].collidepoint(pos):
            # Toggle pencil mode - Red Donaldson, March 17, 2026
            self.audio.play_sound('button')
            self.toggle_pencil_mode()
    
    def handle_key(self, key):
        """Handle keyboard events"""
        if self.game_over:
            return
        
        # Check for Ctrl+Z (undo)
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] or keys[pygame.K_LMETA] or keys[pygame.K_RMETA]) and key == pygame.K_z:
            self.undo()
            return
        
        # Check for Ctrl+Shift+A (toggle admin mode)
        if ((keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] or keys[pygame.K_LMETA] or keys[pygame.K_RMETA]) and 
            (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and key == pygame.K_a):
            self.toggle_admin_mode()
            return
        
        # Toggle pencil mode with 'P' key (only for 9x9 grids)
        # For larger grids (16x16, 25x25), P is a valid symbol, so use button instead
        # For 16x16: P is NOT in hex (0-9, A-F), so toggle pencil mode
        # For 25x25: P is a valid symbol (A-Z except X), so place it
        # Fixed by: Red Donaldson, March 17, 2026
        if key == pygame.K_p:
            # Check if 'P' is a valid symbol in the current grid
            if 'P' in self.symbols:
                # P is valid symbol (25x25 grid) - place it
                self.handle_cell_input('P')
            else:
                # P not valid (9x9 or 16x16 grid) - toggle pencil mode
                self.toggle_pencil_mode()
            return
        
        # Handle number input for all grid sizes
        if key in range(pygame.K_0, pygame.K_9 + 1):
            if self.grid_size == 9:
                self.place_number(key - pygame.K_0)
            else:
                char = chr(key)
                self.handle_cell_input(char)
        # Handle keypad input - keypad constants are NOT sequential, so check individually
        elif key == pygame.K_KP0:
            digit = 0
            if self.grid_size == 9:
                self.place_number(digit)
            else:
                self.handle_cell_input(str(digit))
        elif key == pygame.K_KP1:
            digit = 1
            if self.grid_size == 9:
                self.place_number(digit)
            else:
                self.handle_cell_input(str(digit))
        elif key == pygame.K_KP2:
            digit = 2
            if self.grid_size == 9:
                self.place_number(digit)
            else:
                self.handle_cell_input(str(digit))
        elif key == pygame.K_KP3:
            digit = 3
            if self.grid_size == 9:
                self.place_number(digit)
            else:
                self.handle_cell_input(str(digit))
        elif key == pygame.K_KP4:
            digit = 4
            if self.grid_size == 9:
                self.place_number(digit)
            else:
                self.handle_cell_input(str(digit))
        elif key == pygame.K_KP5:
            digit = 5
            if self.grid_size == 9:
                self.place_number(digit)
            else:
                self.handle_cell_input(str(digit))
        elif key == pygame.K_KP6:
            digit = 6
            if self.grid_size == 9:
                self.place_number(digit)
            else:
                self.handle_cell_input(str(digit))
        elif key == pygame.K_KP7:
            digit = 7
            if self.grid_size == 9:
                self.place_number(digit)
            else:
                self.handle_cell_input(str(digit))
        elif key == pygame.K_KP8:
            digit = 8
            if self.grid_size == 9:
                self.place_number(digit)
            else:
                self.handle_cell_input(str(digit))
        elif key == pygame.K_KP9:
            digit = 9
            if self.grid_size == 9:
                self.place_number(digit)
            else:
                self.handle_cell_input(str(digit))
        elif key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
            self.place_number(0)
        # Handle character input for 16x16 and 25x25
        elif key in range(pygame.K_a, pygame.K_z + 1):
            char = chr(key)
            self.handle_cell_input(char)
        
        # Arrow keys for navigation
        if key == pygame.K_UP:
            self.move_selection(0, -1)
        elif key == pygame.K_DOWN:
            self.move_selection(0, 1)
        elif key == pygame.K_LEFT:
            self.move_selection(-1, 0)
        elif key == pygame.K_RIGHT:
            self.move_selection(1, 0)
    
    def move_selection(self, dx, dy):
        """Move the selected cell"""
        if self.selected_cell is None:
            self.selected_cell = (0, 0)
            return
        
        row, col = self.selected_cell
        new_row = (row + dy) % self.grid_size
        new_col = (col + dx) % self.grid_size
        self.selected_cell = (new_row, new_col)
    
    def draw(self):
        """Draw the game screen"""
        if self.game_state == 'menu':
            draw_main_menu(self)
        else:
            # Update all animations and effects
            self.update_animation()
            self.update_floating_points()
            self.update_cell_flashes()
            
            # Draw everything using the UI renderer
            draw_game_screen(self)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos  # Track mouse position for hover effects
                elif event.type == pygame.KEYDOWN:
                    # Only handle keyboard in playing state
                    if self.game_state == 'playing':
                        self.handle_key(event.key)
                    # ESC to return to menu (only when not in game over state)
                    elif event.key == pygame.K_ESCAPE and self.game_state == 'playing' and not self.game_over:
                        self.game_state = 'menu'
                elif event.type == self.timer_event:
                    # Only update timer when playing and not game over
                    if self.game_state == 'playing' and not self.game_over:
                        self.seconds += 1
            
            self.draw()
            self.clock.tick(FPS)
        
        # Clean up audio resources
        self.audio.cleanup()
        
        pygame.quit()
        sys.exit()


def main():
    """Main entry point"""
    game = SudokuGame()
    game.run()


if __name__ == "__main__":
    main()
