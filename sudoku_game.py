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

# Import game modules
from constants import *
import game_logic
from ui_renderer import draw_game_screen


class SudokuGame:
    def __init__(self):
        pygame.init()
        
        # Window settings
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Sudoku Game")
        
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
        try:
            self.title_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['title'], bold=True)
            self.large_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['large'])
            self.medium_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['medium'])
            self.small_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['small'])
            self.button_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['button'])
        except:
            # Fallback to monospace
            self.title_font = pygame.font.SysFont(FONT_FALLBACK, FONT_SIZES['title'], bold=True)
            self.large_font = pygame.font.SysFont(FONT_FALLBACK, FONT_SIZES['large'])
            self.medium_font = pygame.font.SysFont(FONT_FALLBACK, FONT_SIZES['medium'])
            self.small_font = pygame.font.SysFont(FONT_FALLBACK, FONT_SIZES['small'])
            self.button_font = pygame.font.SysFont(FONT_FALLBACK, FONT_SIZES['button'])
        
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
        self.mouse_pos = (0, 0)  # Track mouse position for hover effects
        
        # Animation state
        self.animation_queue = []
        self.current_animation_frame = 0
        self.animation_speed = ANIMATION_SPEED
        self.laser_particles = []
        self.laser_source = None
        
        # Difficulty settings
        self.difficulty_settings = DIFFICULTY_SETTINGS
        
        # Buttons
        self.buttons = {}
        self.create_buttons()
        
        # Timer
        self.clock = pygame.time.Clock()
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)
        
        # Start first game
        self.new_game()
    
    def create_buttons(self):
        """Create button rectangles"""
        # Control buttons (New Game, Hint, Undo, Settings) - fixed position
        button_width = 72
        button_height = 35
        button_y = 945  # Fixed position at bottom
        spacing = 8
        
        total_buttons = 4
        start_x = (self.WINDOW_WIDTH - (button_width * total_buttons + spacing * (total_buttons - 1))) // 2
        
        self.buttons['new_game'] = pygame.Rect(start_x, button_y, button_width, button_height)
        self.buttons['hint'] = pygame.Rect(start_x + button_width + spacing, button_y, 
                                      button_width, button_height)
        self.buttons['undo'] = pygame.Rect(start_x + (button_width + spacing) * 2, button_y,
                                      button_width, button_height)
        self.buttons['settings'] = pygame.Rect(start_x + (button_width + spacing) * 3, button_y, 
                                       button_width, button_height)
        
        # Settings modal buttons
        modal_width = 400
        modal_height = 300
        modal_x = (self.WINDOW_WIDTH - modal_width) // 2
        modal_y = (self.WINDOW_HEIGHT - modal_height) // 2
        
        self.buttons['settings_modal'] = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
        self.buttons['settings_close'] = pygame.Rect(modal_x + modal_width - 40, modal_y + 10, 30, 30)
        
        # Difficulty buttons
        diff_y = modal_y + 110
        diff_width = 100
        diff_spacing = 20
        diff_total_width = diff_width * 3 + diff_spacing * 2
        diff_start_x = modal_x + (modal_width - diff_total_width) // 2
        
        self.buttons['easy'] = pygame.Rect(diff_start_x, diff_y, diff_width, 35)
        self.buttons['medium'] = pygame.Rect(diff_start_x + diff_width + diff_spacing, 
                                       diff_y, diff_width, 35)
        self.buttons['hard'] = pygame.Rect(diff_start_x + (diff_width + diff_spacing) * 2, 
                                      diff_y, diff_width, 35)
        
        # Check button
        check_width = 140
        check_x = modal_x + (modal_width - check_width) // 2
        self.buttons['check'] = pygame.Rect(check_x, diff_y + 70, check_width, 40)
        
        # Game over modal buttons
        gameover_modal_width = 450
        gameover_modal_height = 300
        gameover_modal_x = (self.WINDOW_WIDTH - gameover_modal_width) // 2
        gameover_modal_y = (self.WINDOW_HEIGHT - gameover_modal_height) // 2
        
        self.buttons['gameover_modal'] = pygame.Rect(gameover_modal_x, gameover_modal_y, 
                                                      gameover_modal_width, gameover_modal_height)
        
        # New game button in game over modal
        newgame_width = 140
        newgame_x = gameover_modal_x + (gameover_modal_width - newgame_width) // 2
        self.buttons['gameover_newgame'] = pygame.Rect(newgame_x, gameover_modal_y + 220, 
                                                        newgame_width, 45)
    
    def update_cell_font(self):
        """Update cell font size based on grid size"""
        if self.grid_size == 9:
            font_size = 40
        elif self.grid_size == 16:
            font_size = 28
        else:  # 25
            font_size = 20
        
        # Calculate pencil mark size based on cell size
        # Each pencil mark occupies 1/box_size of the cell dimension
        # Font should be ~65-70% of that slot to leave spacing
        cell_size = self.BOARD_SIZE // self.grid_size
        pencil_slot_size = cell_size / self.box_size
        pencil_size = int(pencil_slot_size * 0.68)  # 68% of slot size for spacing
        
        try:
            self.cell_font = pygame.font.SysFont(FONT_NAME, font_size, bold=True)
            self.pencil_font = pygame.font.SysFont(FONT_NAME, pencil_size)
        except:
            self.cell_font = pygame.font.SysFont(FONT_FALLBACK, font_size, bold=True)
            self.pencil_font = pygame.font.SysFont(FONT_FALLBACK, pencil_size)
    
    def new_game(self):
        """Start a new game"""
        self.game_over = False
        self.show_win_message = False
        self.show_lose_message = False
        self.show_settings = False  # FIX: Close settings modal when starting new game
        self.score = 0
        self.seconds = 0
        self.pencil_mode = False
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
        
        # Generate puzzle
        self.solution = game_logic.generate_complete_sudoku(
            self.grid_size, self.box_size, self.symbols
        )
        self.board = copy.deepcopy(self.solution)
        game_logic.remove_numbers(
            self.board, self.grid_size, settings['cells_to_remove']
        )
        self.initial_board = copy.deepcopy(self.board)
        
        # Initialize pencil marks (empty sets for each cell)
        self.pencil_marks = [[set() for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        self.selected_cell = None
        self.show_message("New game started! Good luck!", self.DARK_BLUE)
    
    def auto_fill_singles(self, source_cell=None, award_points=True):
        """Auto-fill cells that have only one possible value"""
        filled_sequence = game_logic.find_auto_fill_cells(
            self.board, self.initial_board, self.grid_size, 
            self.box_size, self.symbols, source_cell
        )
        
        # Award partial points for auto-filled cells (unless from hint)
        filled_count = len(filled_sequence)
        if filled_count > 0 and award_points:
            points_per_cell = self.difficulty_settings[self.difficulty]['points_per_cell']
            auto_points = (points_per_cell // 2) * filled_count
            self.score += auto_points
            
            if filled_count == 1:
                self.show_message(f"+{auto_points} pts (1 auto-filled)", self.DARK_BLUE)
            else:
                self.show_message(f"+{auto_points} pts ({filled_count} auto-filled)", self.DARK_BLUE)
            
            # Start animation
            self.start_animation(filled_sequence, source_cell)
        
        return filled_count
    
    def start_animation(self, filled_sequence, source_cell=None):
        """Initialize animation for auto-filled cells"""
        if not filled_sequence:
            return
        
        self.animation_queue = filled_sequence.copy()
        self.current_animation_frame = 0
        
        # Set laser source to the user's cell if provided
        if source_cell:
            self.laser_source = source_cell
        else:
            row, col, value = filled_sequence[0]
            self.board[row][col] = value
            self.laser_source = (row, col)
    
    def update_animation(self):
        """Update animation state each frame"""
        if not self.animation_queue:
            return
        
        self.current_animation_frame += 1
        
        # Move to next cell in animation
        if self.current_animation_frame >= self.animation_speed:
            self.current_animation_frame = 0
            
            # Fill the first cell in queue
            if self.animation_queue:
                row, col, value = self.animation_queue[0]
                self.board[row][col] = value
                self.pencil_marks[row][col].clear()  # Clear pencil marks when auto-filling
                
                self.laser_source = (row, col)
                self.animation_queue.pop(0)
            
            # Check if animation is complete
            if not self.animation_queue:
                self.laser_source = None
                if game_logic.is_puzzle_complete(self.board, self.solution, self.grid_size):
                    self.win_game()
    
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
            
            auto_filled = self.auto_fill_singles(source_cell=(row, col))
            
            if auto_filled == 0:
                self.show_message(f"Correct! +{points} points", self.DARK_GREEN)
            
            if game_logic.is_puzzle_complete(self.board, self.solution, self.grid_size):
                self.win_game()
        else:
            self.lives -= 1
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
                    
                    auto_filled = self.auto_fill_singles(source_cell=(row, col))
                    
                    if auto_filled == 0:
                        self.show_message(f"Correct! +{points} points", self.DARK_GREEN)
                    
                    if game_logic.is_puzzle_complete(self.board, self.solution, self.grid_size):
                        self.win_game()
                else:
                    self.lives -= 1
                    self.show_message("Wrong! -1 life", self.DARK_RED)
                    
                    if self.lives <= 0:
                        self.lose_game()
    
    def toggle_pencil_mode(self):
        """Toggle between pencil and pen mode"""
        self.pencil_mode = not self.pencil_mode
        mode = "Pencil" if self.pencil_mode else "Pen"
        self.show_message(f"{mode} mode", self.DARK_BLUE)
    
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
    
    def show_message(self, text, color):
        """Display a temporary message"""
        self.message = text
        self.message_color = color
        self.message_timer = 180  # 3 seconds at 60 FPS
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        # Update mouse position for hover effects
        self.mouse_pos = pos
        
        # Handle game over modal
        if self.show_win_message or self.show_lose_message:
            if self.buttons['gameover_modal'].collidepoint(pos):
                if self.buttons['gameover_newgame'].collidepoint(pos):
                    self.new_game()
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
                    self.show_settings = False
                elif self.buttons['easy'].collidepoint(pos):
                    if self.difficulty != 'easy':
                        self.difficulty = 'easy'
                        self.new_game()
                elif self.buttons['medium'].collidepoint(pos):
                    if self.difficulty != 'medium':
                        self.difficulty = 'medium'
                        self.new_game()
                elif self.buttons['hard'].collidepoint(pos):
                    if self.difficulty != 'hard':
                        self.difficulty = 'hard'
                        self.new_game()
                elif self.buttons['check'].collidepoint(pos):
                    self.check_solution()
                return
            else:
                self.show_settings = False
                return
        
        # Check board cells
        cell = self.get_cell_from_pos(pos)
        if cell:
            row, col = cell
            if self.initial_board[row][col] is None:
                self.selected_cell = cell
            return
        
        # Check buttons
        if self.buttons['new_game'].collidepoint(pos):
            self.new_game()
        elif self.buttons['hint'].collidepoint(pos):
            self.give_hint()
        elif self.buttons['undo'].collidepoint(pos):
            self.undo()
        elif self.buttons['settings'].collidepoint(pos):
            self.show_settings = True
    
    def handle_key(self, key):
        """Handle keyboard events"""
        if self.game_over:
            return
        
        # Check for Ctrl+Z (undo)
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] or keys[pygame.K_LMETA] or keys[pygame.K_RMETA]) and key == pygame.K_z:
            self.undo()
            return
        
        # Toggle pencil mode with 'P' key
        if key == pygame.K_p:
            self.toggle_pencil_mode()
            return
        
        # Handle number input for all grid sizes
        if key in range(pygame.K_0, pygame.K_9 + 1):
            if self.grid_size == 9:
                self.place_number(key - pygame.K_0)
            else:
                char = chr(key)
                self.handle_cell_input(char)
        elif key == pygame.K_KP0:
            self.place_number(0)
        elif key == pygame.K_KP1:
            self.place_number(1)
        elif key == pygame.K_KP2:
            self.place_number(2)
        elif key == pygame.K_KP3:
            self.place_number(3)
        elif key == pygame.K_KP4:
            self.place_number(4)
        elif key == pygame.K_KP5:
            self.place_number(5)
        elif key == pygame.K_KP6:
            self.place_number(6)
        elif key == pygame.K_KP7:
            self.place_number(7)
        elif key == pygame.K_KP8:
            self.place_number(8)
        elif key == pygame.K_KP9:
            self.place_number(9)
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
        # Update animation
        self.update_animation()
        
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
                    self.handle_key(event.key)
                elif event.type == self.timer_event:
                    if not self.game_over:
                        self.seconds += 1
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Main entry point"""
    game = SudokuGame()
    game.run()


if __name__ == "__main__":
    main()
