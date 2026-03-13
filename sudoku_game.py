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


class SudokuGame:
    def __init__(self):
        pygame.init()
        
        # Window settings
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 1000
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Sudoku Game")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.LIGHT_GRAY = (240, 240, 240)
        self.BLUE = (187, 222, 251)
        self.DARK_BLUE = (102, 126, 234)
        self.GREEN = (200, 230, 201)
        self.RED = (255, 205, 210)
        self.PURPLE = (118, 75, 162)
        self.DARK_GREEN = (46, 125, 50)
        self.DARK_RED = (198, 40, 40)
        self.YELLOW = (255, 255, 200)
        
        # Try to load Ubuntu Mono font, fallback to monospace
        try:
            self.title_font = pygame.font.SysFont('ubuntumono', 52, bold=True)
            self.large_font = pygame.font.SysFont('ubuntumono', 38)
            self.medium_font = pygame.font.SysFont('ubuntumono', 28)
            self.small_font = pygame.font.SysFont('ubuntumono', 22)
            self.button_font = pygame.font.SysFont('ubuntumono', 20)
        except:
            # Fallback to monospace
            self.title_font = pygame.font.SysFont('monospace', 52, bold=True)
            self.large_font = pygame.font.SysFont('monospace', 38)
            self.medium_font = pygame.font.SysFont('monospace', 28)
            self.small_font = pygame.font.SysFont('monospace', 22)
            self.button_font = pygame.font.SysFont('monospace', 20)
        
        # Board settings (will be updated per difficulty)
        self.BOARD_SIZE = 720  # Divisible by 9, 16, and 25
        self.BOARD_X = (self.WINDOW_WIDTH - self.BOARD_SIZE) // 2
        self.BOARD_Y = 180
        
        # Game state
        self.board = []
        self.solution = []
        self.initial_board = []
        self.lives = 3
        self.max_lives = 3
        self.score = 0
        self.selected_cell = None
        self.cell_input_buffer = ""  # For multi-character input
        self.difficulty = 'easy'
        self.grid_size = 9
        self.box_size = 3
        self.symbols = []
        self.cell_font = None
        self.seconds = 0
        self.game_over = False
        self.show_win_message = False
        self.show_lose_message = False
        self.message = ""
        self.message_color = self.BLACK
        self.message_timer = 0
        self.show_settings = False
        
        # Animation state
        self.animation_queue = []
        self.current_animation_frame = 0
        self.animation_speed = 10
        self.laser_particles = []
        self.laser_source = None
        
        # Difficulty settings
        self.difficulty_settings = {
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
        
        # Buttons
        self.buttons = {}
        self.create_buttons()
        
        # Timer
        self.clock = pygame.time.Clock()
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)
        
        self.new_game()
    
    def create_buttons(self):
        """Create UI buttons"""
        self.buttons = {}
        
        # Control buttons - fixed position at bottom (below max board size)
        # Max board: BOARD_Y (180) + max BOARD_SIZE (720) = 900
        button_y = 945  # Fixed position to stay within 1000px window
        button_width = 100
        button_height = 35
        spacing = 15
        
        start_x = (self.WINDOW_WIDTH - (button_width * 3 + spacing * 2)) // 2
        
        self.buttons['new_game'] = pygame.Rect(start_x, button_y, button_width, button_height)
        self.buttons['hint'] = pygame.Rect(start_x + button_width + spacing, button_y, 
                                      button_width, button_height)
        self.buttons['settings'] = pygame.Rect(start_x + (button_width + spacing) * 2, button_y, 
                                       button_width, button_height)
        
        # Cell confirm/clear buttons (for 16x16 and 25x25) - fixed position
        confirm_y = 905  # 5px below max board
        self.buttons['confirm'] = pygame.Rect((self.WINDOW_WIDTH - 180) // 2, confirm_y, 85, 35)
        self.buttons['clear_cell'] = pygame.Rect((self.WINDOW_WIDTH + 10) // 2, confirm_y, 85, 35)
        
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
        """Update cell font based on grid size"""
        if self.grid_size == 9:
            font_size = 40
        elif self.grid_size == 16:
            font_size = 28
        else:  # 25x25
            font_size = 20
        
        try:
            self.cell_font = pygame.font.SysFont('ubuntumono', font_size, bold=True)
        except:
            self.cell_font = pygame.font.SysFont('monospace', font_size, bold=True)
    
    def new_game(self):
        """Start a new game"""
        self.game_over = False
        self.show_win_message = False
        self.show_lose_message = False
        self.score = 0
        self.seconds = 0
        self.cell_input_buffer = ""
        
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
        self.solution = self.generate_complete_sudoku()
        self.board = copy.deepcopy(self.solution)
        self.remove_numbers()
        self.initial_board = copy.deepcopy(self.board)
        
        self.selected_cell = None
        self.show_message("New game started! Good luck!", self.DARK_BLUE)
    
    def generate_complete_sudoku(self):
        """Generate a complete valid Sudoku board"""
        board = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.fill_board(board)
        return board
    
    def fill_board(self, board, row=0, col=0):
        """Fill the Sudoku board using backtracking"""
        if row == self.grid_size:
            return True
        if col == self.grid_size:
            return self.fill_board(board, row + 1, 0)
        
        symbols = self.symbols.copy()
        random.shuffle(symbols)
        
        for symbol in symbols:
            if self.is_valid_placement(board, row, col, symbol):
                board[row][col] = symbol
                if self.fill_board(board, row, col + 1):
                    return True
                board[row][col] = None
        
        return False
    
    def is_valid_placement(self, board, row, col, symbol):
        """Check if placing symbol at (row, col) is valid"""
        # Check row
        for c in range(self.grid_size):
            if board[row][c] == symbol:
                return False
        
        # Check column
        for r in range(self.grid_size):
            if board[r][col] == symbol:
                return False
        
        # Check box
        box_row = (row // self.box_size) * self.box_size
        box_col = (col // self.box_size) * self.box_size
        for i in range(box_row, box_row + self.box_size):
            for j in range(box_col, box_col + self.box_size):
                if board[i][j] == symbol:
                    return False
        
        return True
    
    def remove_numbers(self):
        """Remove numbers to create the puzzle"""
        cells_to_remove = self.difficulty_settings[self.difficulty]['cells_to_remove']
        removed = 0
        
        while removed < cells_to_remove:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            
            if self.board[row][col] is not None:
                self.board[row][col] = None
                removed += 1
    
    def get_possible_values(self, row, col):
        """Get all possible values for a given cell"""
        return self.get_possible_values_for_board(self.board, row, col)
    
    def get_possible_values_for_board(self, board, row, col):
        """Get all possible values for a given cell on a specific board"""
        if board[row][col] is not None:
            return set()
        
        possible = set(self.symbols)
        
        # Remove values in same row
        for c in range(self.grid_size):
            if board[row][c] is not None:
                possible.discard(board[row][c])
        
        # Remove values in same column
        for r in range(self.grid_size):
            if board[r][col] is not None:
                possible.discard(board[r][col])
        
        # Remove values in same box
        box_row = (row // self.box_size) * self.box_size
        box_col = (col // self.box_size) * self.box_size
        for i in range(box_row, box_row + self.box_size):
            for j in range(box_col, box_col + self.box_size):
                if board[i][j] is not None:
                    possible.discard(board[i][j])
        
        return possible
    
    def auto_fill_singles(self, source_cell=None):
        """Auto-fill cells that have only one possible value"""
        filled_sequence = []
        changes_made = True
        
        # Create a temporary board to simulate the fills
        temp_board = [row[:] for row in self.board]
        
        # Keep looping until no more single-possibility cells are found
        while changes_made:
            changes_made = False
            
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    # Skip cells that are already filled or initially given
                    if temp_board[i][j] is not None or self.initial_board[i][j] is not None:
                        continue
                    
                    # Get possible values based on temp board
                    possible = self.get_possible_values_for_board(temp_board, i, j)
                    
                    # If only one possibility, record it
                    if len(possible) == 1:
                        value = possible.pop()
                        temp_board[i][j] = value
                        filled_sequence.append((i, j, value))
                        changes_made = True
        
        # Sort filled sequence by distance from source cell if provided
        if source_cell and filled_sequence:
            source_row, source_col = source_cell
            filled_sequence.sort(key=lambda cell: abs(cell[0] - source_row) + abs(cell[1] - source_col))
        
        # Award partial points for auto-filled cells
        filled_count = len(filled_sequence)
        if filled_count > 0:
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
                
                self.laser_source = (row, col)
                self.animation_queue.pop(0)
            
            # Check if animation is complete
            if not self.animation_queue:
                self.laser_source = None
                if self.is_puzzle_complete():
                    self.win_game()
    
    def get_cell_center(self, row, col):
        """Get the center coordinates of a cell"""
        cell_size = self.BOARD_SIZE // self.grid_size
        x = self.BOARD_X + col * cell_size + cell_size // 2
        y = self.BOARD_Y + row * cell_size + cell_size // 2
        return (x, y)
    
    def draw_laser_effect(self):
        """Draw laser effect between animated cells"""
        if not self.animation_queue or self.laser_source is None:
            return
        
        source_row, source_col = self.laser_source
        target_row, target_col = self.animation_queue[0][0], self.animation_queue[0][1]
        
        source_pos = self.get_cell_center(source_row, source_col)
        target_pos = self.get_cell_center(target_row, target_col)
        
        progress = self.current_animation_frame / self.animation_speed
        
        laser_x = source_pos[0] + (target_pos[0] - source_pos[0]) * progress
        laser_y = source_pos[1] + (target_pos[1] - source_pos[1]) * progress
        
        laser_color = (100, 200, 255)
        glow_color = (150, 220, 255)
        
        pygame.draw.line(self.screen, glow_color, source_pos, (laser_x, laser_y), 8)
        pygame.draw.line(self.screen, laser_color, source_pos, (laser_x, laser_y), 4)
        
        pygame.draw.circle(self.screen, self.WHITE, (int(laser_x), int(laser_y)), 6)
        pygame.draw.circle(self.screen, laser_color, (int(laser_x), int(laser_y)), 4)
    
    def get_cell_from_pos(self, pos):
        """Get board cell coordinates from mouse position"""
        x, y = pos
        
        if (x < self.BOARD_X or x >= self.BOARD_X + self.BOARD_SIZE or
            y < self.BOARD_Y or y >= self.BOARD_Y + self.BOARD_SIZE):
            return None
        
        cell_size = self.BOARD_SIZE // self.grid_size
        col = (x - self.BOARD_X) // cell_size
        row = (y - self.BOARD_Y) // cell_size
        
        return (row, col)
    
    def place_number(self, symbol):
        """Place a number in the selected cell (for 9x9 only)"""
        if self.game_over or self.selected_cell is None:
            return
        
        # Only direct placement for 9x9
        if self.grid_size != 9:
            return
        
        row, col = self.selected_cell
        
        if self.initial_board[row][col] is not None:
            return
        
        # Erase
        if symbol == '0' or symbol == 0:
            self.board[row][col] = None
            return
        
        # Convert number to string symbol
        if isinstance(symbol, int) and 1 <= symbol <= 9:
            symbol = str(symbol)
        
        # Check if correct
        is_correct = self.solution[row][col] == symbol
        
        if is_correct:
            self.board[row][col] = symbol
            points = self.difficulty_settings[self.difficulty]['points_per_cell']
            self.score += points
            
            auto_filled = self.auto_fill_singles(source_cell=(row, col))
            
            if auto_filled == 0:
                self.show_message(f"Correct! +{points} points", self.DARK_GREEN)
            
            if self.is_puzzle_complete():
                self.win_game()
        else:
            self.lives -= 1
            self.show_message("Wrong! -1 life", self.DARK_RED)
            
            if self.lives <= 0:
                self.lose_game()
    
    def handle_cell_input(self, char):
        """Handle character input for multi-character cells (16x16, 25x25)"""
        if self.game_over or self.selected_cell is None:
            return
        
        if self.grid_size == 9:
            return
        
        row, col = self.selected_cell
        
        if self.initial_board[row][col] is not None:
            return
        
        # Add character to buffer
        char = char.upper()
        if char in self.symbols:
            self.cell_input_buffer = char
    
    def confirm_cell_input(self):
        """Confirm the cell input for multi-character grids"""
        if self.game_over or self.selected_cell is None or not self.cell_input_buffer:
            return
        
        if self.grid_size == 9:
            return
        
        row, col = self.selected_cell
        
        if self.initial_board[row][col] is not None:
            return
        
        symbol = self.cell_input_buffer
        is_correct = self.solution[row][col] == symbol
        
        if is_correct:
            self.board[row][col] = symbol
            points = self.difficulty_settings[self.difficulty]['points_per_cell']
            self.score += points
            
            auto_filled = self.auto_fill_singles(source_cell=(row, col))
            
            if auto_filled == 0:
                self.show_message(f"Correct! +{points} points", self.DARK_GREEN)
            
            if self.is_puzzle_complete():
                self.win_game()
        else:
            self.lives -= 1
            self.show_message("Wrong! -1 life", self.DARK_RED)
            
            if self.lives <= 0:
                self.lose_game()
        
        self.cell_input_buffer = ""
    
    def clear_cell_input(self):
        """Clear the cell input buffer"""
        if self.grid_size == 9:
            # For 9x9, clear the cell
            if self.selected_cell and self.initial_board[self.selected_cell[0]][self.selected_cell[1]] is None:
                self.board[self.selected_cell[0]][self.selected_cell[1]] = None
        else:
            self.cell_input_buffer = ""
    
    def is_puzzle_complete(self):
        """Check if the puzzle is completely solved"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] != self.solution[i][j]:
                    return False
        return True
    
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
                
                auto_filled = self.auto_fill_singles(source_cell=(row, col))
                
                if auto_filled == 0:
                    self.show_message("Hint given! -10 points", self.DARK_BLUE)
                
                if self.is_puzzle_complete():
                    self.win_game()
        else:
            self.show_message("Not enough points for a hint! (Need 10 points)", self.DARK_RED)
    
    def check_solution(self):
        """Check the current solution status"""
        if self.game_over:
            return
        
        correct_count = 0
        total_filled = 0
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] is not None and self.initial_board[i][j] is None:
                    total_filled += 1
                    if self.board[i][j] == self.solution[i][j]:
                        correct_count += 1
        
        if total_filled == 0:
            self.show_message("No cells filled yet!", self.DARK_BLUE)
        elif correct_count == total_filled:
            self.show_message(f"All {total_filled} cells are correct!", self.DARK_GREEN)
        else:
            wrong_count = total_filled - correct_count
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
                if self.grid_size != 9:
                    self.cell_input_buffer = ""
            return
        
        # Check buttons
        if self.buttons['new_game'].collidepoint(pos):
            self.new_game()
        elif self.buttons['hint'].collidepoint(pos):
            self.give_hint()
        elif self.buttons['settings'].collidepoint(pos):
            self.show_settings = True
        elif self.grid_size != 9:
            # Confirm/Clear buttons for larger grids
            if self.buttons['confirm'].collidepoint(pos):
                self.confirm_cell_input()
            elif self.buttons['clear_cell'].collidepoint(pos):
                self.clear_cell_input()
    
    def handle_key(self, key):
        """Handle keyboard events"""
        if self.game_over:
            return
        
        if self.grid_size == 9:
            # Handle number input for 9x9
            if key in range(pygame.K_0, pygame.K_9 + 1):
                self.place_number(key - pygame.K_0)
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
        else:
            # Handle character input for 16x16 and 25x25
            if pygame.K_0 <= key <= pygame.K_9:
                self.handle_cell_input(chr(key))
            elif pygame.K_a <= key <= pygame.K_z:
                self.handle_cell_input(chr(key).upper())
            elif pygame.K_KP0 <= key <= pygame.K_KP9:
                self.handle_cell_input(str(key - pygame.K_KP0))
            elif key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
                self.confirm_cell_input()
            elif key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                self.clear_cell_input()
        
        # Handle arrow keys for cell navigation
        if key == pygame.K_UP:
            self.move_selection(0, -1)
        elif key == pygame.K_DOWN:
            self.move_selection(0, 1)
        elif key == pygame.K_LEFT:
            self.move_selection(-1, 0)
        elif key == pygame.K_RIGHT:
            self.move_selection(1, 0)
    
    def move_selection(self, dx, dy):
        """Move the selected cell by dx, dy"""
        if self.selected_cell is None:
            self.selected_cell = (0, 0)
            return
        
        row, col = self.selected_cell
        new_row = (row + dy) % self.grid_size
        new_col = (col + dx) % self.grid_size
        self.selected_cell = (new_row, new_col)
        if self.grid_size != 9:
            self.cell_input_buffer = ""
    
    def draw(self):
        """Draw the game screen"""
        self.screen.fill(self.WHITE)
        
        # Update animation
        self.update_animation()
        
        # Title
        title_text = self.title_font.render("Sudoku Game", True, self.PURPLE)
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 40))
        self.screen.blit(title_text, title_rect)
        
        # Game info
        info_y = 90
        
        # Lives
        lives_text = self.medium_font.render(f"Lives: {self.lives}", True, self.DARK_RED)
        self.screen.blit(lives_text, (80, info_y))
        
        # Score
        score_text = self.medium_font.render(f"Score: {self.score}", True, self.DARK_GREEN)
        score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, info_y + 12))
        self.screen.blit(score_text, score_rect)
        
        # Timer
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        timer_text = self.medium_font.render(f"Time: {minutes:02d}:{seconds:02d}", 
                                            True, self.BLACK)
        timer_rect = timer_text.get_rect(right=self.WINDOW_WIDTH - 80, centery=info_y + 12)
        self.screen.blit(timer_text, timer_rect)
        
        # Temporary message (not game over messages)
        if self.message and self.message_timer > 0 and not self.game_over:
            lines = self.message.split('\n')
            for i, line in enumerate(lines):
                msg_text = self.small_font.render(line, True, self.message_color)
                msg_rect = msg_text.get_rect(center=(self.WINDOW_WIDTH // 2, 135 + i * 22))
                self.screen.blit(msg_text, msg_rect)
            self.message_timer -= 1
        
        # Draw board
        self.draw_board()
        
        # Draw laser animation effect
        self.draw_laser_effect()
        
        # Draw control buttons
        self.draw_control_buttons()
        
        # Draw confirm/clear buttons for larger grids
        if self.grid_size != 9:
            self.draw_cell_buttons()
        
        # Draw settings modal if open
        if self.show_settings:
            self.draw_settings_modal()
        
        # Draw game over modal if game is over
        if self.show_win_message or self.show_lose_message:
            self.draw_game_over_modal()
        
        pygame.display.flip()
    
    def draw_board(self):
        """Draw the Sudoku board"""
        cell_size = self.BOARD_SIZE // self.grid_size
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = self.BOARD_X + j * cell_size
                y = self.BOARD_Y + i * cell_size
                
                # Determine cell color
                if self.selected_cell == (i, j):
                    if self.grid_size != 9 and self.cell_input_buffer:
                        color = self.YELLOW
                    else:
                        color = self.BLUE
                elif self.initial_board[i][j] is not None:
                    color = self.LIGHT_GRAY
                elif self.board[i][j] is not None and self.board[i][j] == self.solution[i][j]:
                    color = self.GREEN
                else:
                    color = self.WHITE
                
                pygame.draw.rect(self.screen, color, 
                               (x, y, cell_size, cell_size))
                pygame.draw.rect(self.screen, self.GRAY, 
                               (x, y, cell_size, cell_size), 1)
                
                # Draw number or buffer
                display_text = None
                if self.selected_cell == (i, j) and self.cell_input_buffer and self.grid_size != 9:
                    display_text = self.cell_input_buffer
                elif self.board[i][j] is not None:
                    display_text = str(self.board[i][j])
                
                if display_text:
                    num_text = self.cell_font.render(display_text, True, self.BLACK)
                    num_rect = num_text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
                    self.screen.blit(num_text, num_rect)
        
        # Draw thick lines for boxes
        for i in range(0, self.grid_size + 1, self.box_size):
            # Horizontal
            pygame.draw.line(self.screen, self.BLACK,
                           (self.BOARD_X, self.BOARD_Y + i * cell_size),
                           (self.BOARD_X + self.BOARD_SIZE, self.BOARD_Y + i * cell_size), 3)
            # Vertical
            pygame.draw.line(self.screen, self.BLACK,
                           (self.BOARD_X + i * cell_size, self.BOARD_Y),
                           (self.BOARD_X + i * cell_size, self.BOARD_Y + self.BOARD_SIZE), 3)
    
    def draw_control_buttons(self):
        """Draw control buttons"""
        button_data = [
            ('new_game', 'New Game', self.DARK_BLUE),
            ('hint', 'Hint', self.DARK_GREEN),
            ('settings', 'Settings', self.PURPLE)
        ]
        
        for key, text, color in button_data:
            rect = self.buttons[key]
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.BLACK, rect, 2)
            
            text_surface = self.button_font.render(text, True, self.WHITE)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
    
    def draw_cell_buttons(self):
        """Draw confirm/clear buttons for multi-character input"""
        # Confirm button
        pygame.draw.rect(self.screen, self.DARK_GREEN, self.buttons['confirm'])
        pygame.draw.rect(self.screen, self.BLACK, self.buttons['confirm'], 2)
        confirm_text = self.button_font.render("Confirm", True, self.WHITE)
        confirm_rect = confirm_text.get_rect(center=self.buttons['confirm'].center)
        self.screen.blit(confirm_text, confirm_rect)
        
        # Clear button
        pygame.draw.rect(self.screen, self.DARK_RED, self.buttons['clear_cell'])
        pygame.draw.rect(self.screen, self.BLACK, self.buttons['clear_cell'], 2)
        clear_text = self.button_font.render("Clear", True, self.WHITE)
        clear_rect = clear_text.get_rect(center=self.buttons['clear_cell'].center)
        self.screen.blit(clear_text, clear_rect)
    
    def draw_settings_modal(self):
        """Draw the settings modal"""
        modal = self.buttons['settings_modal']
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw modal
        pygame.draw.rect(self.screen, self.WHITE, modal)
        pygame.draw.rect(self.screen, self.BLACK, modal, 3)
        
        # Title
        title_text = self.large_font.render("Settings", True, self.PURPLE)
        title_rect = title_text.get_rect(center=(modal.centerx, modal.top + 40))
        self.screen.blit(title_text, title_rect)
        
        # Difficulty label
        diff_label = self.medium_font.render("Difficulty:", True, self.BLACK)
        diff_label_rect = diff_label.get_rect(center=(modal.centerx, modal.top + 80))
        self.screen.blit(diff_label, diff_label_rect)
        
        # Difficulty buttons
        difficulties = ['easy', 'medium', 'hard']
        labels = ['Easy (9x9)', 'Med (16x16)', 'Hard (25x25)']
        
        for i, (diff, label) in enumerate(zip(difficulties, labels)):
            button = self.buttons[diff]
            color = self.DARK_GREEN if self.difficulty == diff else self.GRAY
            
            pygame.draw.rect(self.screen, color, button)
            pygame.draw.rect(self.screen, self.BLACK, button, 2)
            
            # Use smaller font for button text
            text_surface = self.small_font.render(label, True, self.WHITE if self.difficulty == diff else self.BLACK)
            text_rect = text_surface.get_rect(center=button.center)
            self.screen.blit(text_surface, text_rect)
        
        # Check button
        check_button = self.buttons['check']
        pygame.draw.rect(self.screen, self.DARK_BLUE, check_button)
        pygame.draw.rect(self.screen, self.BLACK, check_button, 2)
        
        check_text = self.button_font.render("Check Solution", True, self.WHITE)
        check_rect = check_text.get_rect(center=check_button.center)
        self.screen.blit(check_text, check_rect)
        
        # Close button
        close_button = self.buttons['settings_close']
        pygame.draw.rect(self.screen, self.DARK_RED, close_button)
        pygame.draw.rect(self.screen, self.BLACK, close_button, 2)
        
        close_text = self.medium_font.render("X", True, self.WHITE)
        close_rect = close_text.get_rect(center=close_button.center)
        self.screen.blit(close_text, close_rect)
    
    def draw_game_over_modal(self):
        """Draw the game over modal"""
        modal = self.buttons['gameover_modal']
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw modal
        pygame.draw.rect(self.screen, self.WHITE, modal)
        pygame.draw.rect(self.screen, self.BLACK, modal, 3)
        
        # Title - Victory or Game Over
        if self.show_win_message:
            title_text = self.large_font.render("Victory!", True, self.DARK_GREEN)
        else:
            title_text = self.large_font.render("Game Over", True, self.DARK_RED)
        title_rect = title_text.get_rect(center=(modal.centerx, modal.top + 50))
        self.screen.blit(title_text, title_rect)
        
        # Display game stats
        y_offset = modal.top + 110
        
        # Score
        score_text = self.medium_font.render(f"Final Score: {self.score}", True, self.BLACK)
        score_rect = score_text.get_rect(center=(modal.centerx, y_offset))
        self.screen.blit(score_text, score_rect)
        
        # Time
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        time_text = self.medium_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, self.BLACK)
        time_rect = time_text.get_rect(center=(modal.centerx, y_offset + 40))
        self.screen.blit(time_text, time_rect)
        
        # Lives remaining (if won)
        if self.show_win_message:
            lives_text = self.medium_font.render(f"Lives Remaining: {self.lives}", True, self.BLACK)
            lives_rect = lives_text.get_rect(center=(modal.centerx, y_offset + 80))
            self.screen.blit(lives_text, lives_rect)
        
        # New game button
        newgame_button = self.buttons['gameover_newgame']
        pygame.draw.rect(self.screen, self.DARK_GREEN, newgame_button)
        pygame.draw.rect(self.screen, self.BLACK, newgame_button, 2)
        
        newgame_text = self.button_font.render("New Game", True, self.WHITE)
        newgame_rect = newgame_text.get_rect(center=newgame_button.center)
        self.screen.blit(newgame_text, newgame_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)
                elif event.type == self.timer_event:
                    if not self.game_over:
                        self.seconds += 1
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


def main():
    """Main entry point"""
    game = SudokuGame()
    game.run()


if __name__ == "__main__":
    main()
