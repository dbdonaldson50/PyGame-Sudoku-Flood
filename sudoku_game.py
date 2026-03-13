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


class SudokuGame:
    def __init__(self):
        pygame.init()
        
        # Window settings
        self.WINDOW_WIDTH = 700
        self.WINDOW_HEIGHT = 900
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
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.large_font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)
        self.cell_font = pygame.font.Font(None, 40)
        
        # Board settings
        self.BOARD_SIZE = 540
        self.CELL_SIZE = self.BOARD_SIZE // 9
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
        self.difficulty = 'medium'
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
        self.animation_speed = 10  # frames per cell
        self.laser_particles = []
        self.laser_source = None  # (row, col) of laser origin
        
        # Difficulty settings
        self.difficulty_settings = {
            'easy': {'cells_to_remove': 30, 'lives': 3, 'points_per_cell': 5},
            'medium': {'cells_to_remove': 40, 'lives': 3, 'points_per_cell': 10},
            'hard': {'cells_to_remove': 50, 'lives': 5, 'points_per_cell': 15}
        }
        
        # Buttons
        self.buttons = self.create_buttons()
        
        # Timer
        self.clock = pygame.time.Clock()
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)
        
        self.new_game()
    
    def create_buttons(self):
        """Create UI buttons"""
        buttons = {}
        
        # Control buttons
        button_y = self.BOARD_Y + self.BOARD_SIZE + 80
        button_width = 150
        button_height = 40
        spacing = 20
        
        start_x = (self.WINDOW_WIDTH - (button_width * 3 + spacing * 2)) // 2
        
        buttons['new_game'] = pygame.Rect(start_x, button_y, button_width, button_height)
        buttons['hint'] = pygame.Rect(start_x + button_width + spacing, button_y, 
                                      button_width, button_height)
        buttons['settings'] = pygame.Rect(start_x + (button_width + spacing) * 2, button_y, 
                                       button_width, button_height)
        
        # Number buttons
        number_y = self.BOARD_Y + self.BOARD_SIZE + 20
        number_size = 50
        number_spacing = 10
        total_width = number_size * 10 + number_spacing * 9
        number_start_x = (self.WINDOW_WIDTH - total_width) // 2
        
        for i in range(1, 10):
            x = number_start_x + (i - 1) * (number_size + number_spacing)
            buttons[f'num_{i}'] = pygame.Rect(x, number_y, number_size, number_size)
        
        # Erase button
        buttons['erase'] = pygame.Rect(
            number_start_x + 9 * (number_size + number_spacing), 
            number_y, number_size, number_size
        )
        
        # Settings modal buttons (positioned when settings is open)
        modal_width = 400
        modal_height = 300
        modal_x = (self.WINDOW_WIDTH - modal_width) // 2
        modal_y = (self.WINDOW_HEIGHT - modal_height) // 2
        
        buttons['settings_modal'] = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
        buttons['settings_close'] = pygame.Rect(modal_x + modal_width - 40, modal_y + 10, 30, 30)
        
        # Difficulty buttons in settings - centered within modal
        diff_y = modal_y + 110
        diff_width = 100
        diff_spacing = 20
        diff_total_width = diff_width * 3 + diff_spacing * 2
        diff_start_x = modal_x + (modal_width - diff_total_width) // 2
        
        buttons['easy'] = pygame.Rect(diff_start_x, diff_y, diff_width, 35)
        buttons['medium'] = pygame.Rect(diff_start_x + diff_width + diff_spacing, 
                                       diff_y, diff_width, 35)
        buttons['hard'] = pygame.Rect(diff_start_x + (diff_width + diff_spacing) * 2, 
                                      diff_y, diff_width, 35)
        
        # Check button in settings - centered within modal
        check_width = 140
        check_x = modal_x + (modal_width - check_width) // 2
        buttons['check'] = pygame.Rect(check_x, diff_y + 70, check_width, 40)
        
        return buttons
    
    def new_game(self):
        """Start a new game"""
        self.game_over = False
        self.show_win_message = False
        self.show_lose_message = False
        self.score = 0
        self.seconds = 0
        
        # Set lives based on difficulty
        self.max_lives = self.difficulty_settings[self.difficulty]['lives']
        self.lives = self.max_lives
        
        # Generate puzzle
        self.solution = self.generate_complete_sudoku()
        self.board = copy.deepcopy(self.solution)
        self.remove_numbers()
        self.initial_board = copy.deepcopy(self.board)
        
        self.selected_cell = None
        self.show_message("New game started! Good luck!", self.DARK_BLUE)
    
    def generate_complete_sudoku(self):
        """Generate a complete valid Sudoku board"""
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_board(board)
        return board
    
    def fill_board(self, board, row=0, col=0):
        """Fill the Sudoku board using backtracking"""
        if row == 9:
            return True
        if col == 9:
            return self.fill_board(board, row + 1, 0)
        
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for num in numbers:
            if self.is_valid_placement(board, row, col, num):
                board[row][col] = num
                if self.fill_board(board, row, col + 1):
                    return True
                board[row][col] = 0
        
        return False
    
    def is_valid_placement(self, board, row, col, num):
        """Check if a number can be placed at the given position"""
        # Check row
        if num in board[row]:
            return False
        
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def remove_numbers(self):
        """Remove numbers from the complete board to create puzzle"""
        cells_to_remove = self.difficulty_settings[self.difficulty]['cells_to_remove']
        removed = 0
        
        while removed < cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1
    
    def get_possible_values(self, row, col):
        """Get all possible values for a given cell"""
        return self.get_possible_values_for_board(self.board, row, col)
    
    def get_possible_values_for_board(self, board, row, col):
        """Get all possible values for a given cell on a specific board"""
        if board[row][col] != 0:
            return set()
        
        possible = set(range(1, 10))
        
        # Remove values in same row
        for c in range(9):
            if board[row][c] != 0:
                possible.discard(board[row][c])
        
        # Remove values in same column
        for r in range(9):
            if board[r][col] != 0:
                possible.discard(board[r][col])
        
        # Remove values in same 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] != 0:
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
            
            for i in range(9):
                for j in range(9):
                    # Skip cells that are already filled or initially given
                    if temp_board[i][j] != 0 or self.initial_board[i][j] != 0:
                        continue
                    
                    # Get possible values based on temp board
                    possible = self.get_possible_values_for_board(temp_board, i, j)
                    
                    # If only one possibility, record it (but don't fill real board yet)
                    if len(possible) == 1:
                        value = possible.pop()
                        temp_board[i][j] = value  # Fill temp board for cascade detection
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
        
        # Set laser source to the user's cell if provided, otherwise first filled cell
        if source_cell:
            self.laser_source = source_cell
        else:
            # Fill the first cell immediately if no source provided
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
            
            # Fill the first cell in queue that the laser just reached
            if self.animation_queue:
                row, col, value = self.animation_queue[0]
                self.board[row][col] = value
                
                # Set this cell as the new laser source
                self.laser_source = (row, col)
                self.animation_queue.pop(0)
            
            # Check if animation is complete
            if not self.animation_queue:
                self.laser_source = None
                # Check if puzzle is complete after animation finishes
                if self.is_puzzle_complete():
                    self.win_game()
    
    def get_cell_center(self, row, col):
        """Get the center coordinates of a cell"""
        x = self.BOARD_X + col * self.CELL_SIZE + self.CELL_SIZE // 2
        y = self.BOARD_Y + row * self.CELL_SIZE + self.CELL_SIZE // 2
        return (x, y)
    
    def draw_laser_effect(self):
        """Draw laser effect between animated cells"""
        if not self.animation_queue or self.laser_source is None:
            return
        
        # Get source and target cells
        source_row, source_col = self.laser_source
        target_row, target_col = self.animation_queue[0][0], self.animation_queue[0][1]
        
        # Get center points
        source_pos = self.get_cell_center(source_row, source_col)
        target_pos = self.get_cell_center(target_row, target_col)
        
        # Calculate animation progress (0 to 1)
        progress = self.current_animation_frame / self.animation_speed
        
        # Interpolate laser position
        laser_x = source_pos[0] + (target_pos[0] - source_pos[0]) * progress
        laser_y = source_pos[1] + (target_pos[1] - source_pos[1]) * progress
        
        # Draw laser beam
        laser_color = (100, 200, 255)  # Cyan/blue laser
        glow_color = (150, 220, 255)
        
        # Draw glow effect (thicker, more transparent)
        pygame.draw.line(self.screen, glow_color, source_pos, (laser_x, laser_y), 8)
        # Draw main laser (thinner, brighter)
        pygame.draw.line(self.screen, laser_color, source_pos, (laser_x, laser_y), 4)
        
        # Draw particles at laser tip
        pygame.draw.circle(self.screen, self.WHITE, (int(laser_x), int(laser_y)), 6)
        pygame.draw.circle(self.screen, laser_color, (int(laser_x), int(laser_y)), 4)
    
    def get_cell_from_pos(self, pos):
        """Get board cell coordinates from mouse position"""
        x, y = pos
        if (self.BOARD_X <= x < self.BOARD_X + self.BOARD_SIZE and
            self.BOARD_Y <= y < self.BOARD_Y + self.BOARD_SIZE):
            col = (x - self.BOARD_X) // self.CELL_SIZE
            row = (y - self.BOARD_Y) // self.CELL_SIZE
            return (row, col)
        return None
    
    def place_number(self, number):
        """Place a number in the selected cell"""
        if self.game_over or self.selected_cell is None:
            return
        
        row, col = self.selected_cell
        
        # Can't modify pre-filled cells
        if self.initial_board[row][col] != 0:
            return
        
        # Erase
        if number == 0:
            self.board[row][col] = 0
            return
        
        # Check if correct
        is_correct = self.solution[row][col] == number
        
        if is_correct:
            self.board[row][col] = number
            points = self.difficulty_settings[self.difficulty]['points_per_cell']
            self.score += points
            
            # Auto-fill cells with only one possibility, starting from current cell
            auto_filled = self.auto_fill_singles(source_cell=(row, col))
            
            # Show message about placement (auto-fill message will override if any were filled)
            if auto_filled == 0:
                self.show_message(f"Correct! +{points} points", self.DARK_GREEN)
            
            # Check if puzzle complete
            if self.is_puzzle_complete():
                self.win_game()
        else:
            self.lives -= 1
            self.show_message("Wrong! -1 life", self.DARK_RED)
            
            if self.lives <= 0:
                self.lose_game()
    
    def is_puzzle_complete(self):
        """Check if the puzzle is completely solved"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != self.solution[i][j]:
                    return False
        return True
    
    def give_hint(self):
        """Give a hint by revealing one cell"""
        if self.game_over:
            return
        
        if self.score >= 10:
            self.score -= 10
            
            # Find empty cells
            empty_cells = []
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == 0:
                        empty_cells.append((i, j))
            
            if empty_cells:
                row, col = random.choice(empty_cells)
                self.board[row][col] = self.solution[row][col]
                
                # Auto-fill cells with only one possibility after hint, starting from hint cell
                auto_filled = self.auto_fill_singles(source_cell=(row, col))
                
                # Show message (auto-fill message will override if any were filled)
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
        
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0 and self.initial_board[i][j] == 0:
                    total_filled += 1
                    if self.board[i][j] == self.solution[i][j]:
                        correct_count += 1
        
        if total_filled == 0:
            self.show_message("Place some numbers first!", self.DARK_BLUE)
        else:
            percentage = round((correct_count / total_filled) * 100)
            self.show_message(
                f"{correct_count}/{total_filled} correct ({percentage}%)",
                self.DARK_BLUE
            )
    
    def win_game(self):
        """Handle winning the game"""
        self.game_over = True
        self.show_win_message = True
        
        time_bonus = max(0, 500 - self.seconds)
        lives_bonus = self.lives * 50
        total_score = self.score + time_bonus + lives_bonus
        
        self.message = (f"🎉 You Win! Total Score: {total_score}\n"
                       f"(Base: {self.score} + Time: {time_bonus} + Lives: {lives_bonus})")
        self.message_color = self.DARK_GREEN
    
    def lose_game(self):
        """Handle losing the game"""
        self.game_over = True
        self.show_lose_message = True
        
        self.message = f"💀 Game Over! You ran out of lives.\nFinal Score: {self.score}"
        self.message_color = self.DARK_RED
        
        # Show solution after a delay
        self.board = copy.deepcopy(self.solution)
    
    def show_message(self, text, color):
        """Show a temporary message"""
        self.message = text
        self.message_color = color
        self.message_timer = 180  # 3 seconds at 60 FPS
    
    def handle_click(self, pos):
        """Handle mouse click events"""
        # If settings modal is open, handle those clicks first
        if self.show_settings:
            if self.buttons['settings_close'].collidepoint(pos):
                self.show_settings = False
                return
            elif self.buttons['settings_modal'].collidepoint(pos):
                # Click inside modal
                if self.buttons['easy'].collidepoint(pos):
                    self.difficulty = 'easy'
                elif self.buttons['medium'].collidepoint(pos):
                    self.difficulty = 'medium'
                elif self.buttons['hard'].collidepoint(pos):
                    self.difficulty = 'hard'
                elif self.buttons['check'].collidepoint(pos):
                    self.check_solution()
                return
            else:
                # Click outside modal - close it
                self.show_settings = False
                return
        
        # Check board cells
        cell = self.get_cell_from_pos(pos)
        if cell:
            row, col = cell
            if self.initial_board[row][col] == 0:
                self.selected_cell = cell
            return
        
        # Check buttons
        if self.buttons['new_game'].collidepoint(pos):
            self.new_game()
        elif self.buttons['hint'].collidepoint(pos):
            self.give_hint()
        elif self.buttons['settings'].collidepoint(pos):
            self.show_settings = True
        elif self.buttons['erase'].collidepoint(pos):
            self.place_number(0)
        else:
            # Check number buttons
            for i in range(1, 10):
                if self.buttons[f'num_{i}'].collidepoint(pos):
                    self.place_number(i)
                    break
    
    def handle_key(self, key):
        """Handle keyboard events"""
        if self.game_over:
            return
        
        # Handle number input (1-9 and 0 for erase)
        if key in range(pygame.K_0, pygame.K_9 + 1):
            self.place_number(key - pygame.K_0)
        # Handle numpad input
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
        
        # Handle arrow keys for cell navigation
        elif key == pygame.K_UP:
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
            # Start at top-left if no cell selected
            self.selected_cell = (0, 0)
            return
        
        row, col = self.selected_cell
        new_row = (row + dy) % 9
        new_col = (col + dx) % 9
        self.selected_cell = (new_row, new_col)
    
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
        self.screen.blit(lives_text, (100, info_y))
        
        # Score
        score_text = self.medium_font.render(f"Score: {self.score}", True, self.DARK_GREEN)
        score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, info_y + 14))
        self.screen.blit(score_text, score_rect)
        
        # Timer
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        timer_text = self.medium_font.render(f"Time: {minutes:02d}:{seconds:02d}", 
                                            True, self.BLACK)
        timer_rect = timer_text.get_rect(right=self.WINDOW_WIDTH - 100, centery=info_y + 14)
        self.screen.blit(timer_text, timer_rect)
        
        # Message
        if self.message and (self.message_timer > 0 or self.game_over):
            lines = self.message.split('\n')
            for i, line in enumerate(lines):
                msg_text = self.small_font.render(line, True, self.message_color)
                msg_rect = msg_text.get_rect(center=(self.WINDOW_WIDTH // 2, 140 + i * 25))
                self.screen.blit(msg_text, msg_rect)
            
            if self.message_timer > 0:
                self.message_timer -= 1
        
        # Draw board
        self.draw_board()
        
        # Draw laser animation effect
        self.draw_laser_effect()
        
        # Draw number buttons
        self.draw_number_buttons()
        
        # Draw control buttons
        self.draw_control_buttons()
        
        # Draw settings modal if open
        if self.show_settings:
            self.draw_settings_modal()
        
        pygame.display.flip()
    
    def draw_board(self):
        """Draw the Sudoku board"""
        # Draw cells
        for i in range(9):
            for j in range(9):
                x = self.BOARD_X + j * self.CELL_SIZE
                y = self.BOARD_Y + i * self.CELL_SIZE
                
                # Determine cell color
                if self.selected_cell == (i, j):
                    color = self.BLUE
                elif self.initial_board[i][j] != 0:
                    color = self.LIGHT_GRAY
                elif self.board[i][j] != 0 and self.board[i][j] == self.solution[i][j]:
                    color = self.GREEN
                else:
                    color = self.WHITE
                
                pygame.draw.rect(self.screen, color, 
                               (x, y, self.CELL_SIZE, self.CELL_SIZE))
                pygame.draw.rect(self.screen, self.GRAY, 
                               (x, y, self.CELL_SIZE, self.CELL_SIZE), 1)
                
                # Draw number
                if self.board[i][j] != 0:
                    num_text = self.cell_font.render(str(self.board[i][j]), True, self.BLACK)
                    num_rect = num_text.get_rect(
                        center=(x + self.CELL_SIZE // 2, y + self.CELL_SIZE // 2)
                    )
                    self.screen.blit(num_text, num_rect)
        
        # Draw thick lines for 3x3 boxes
        for i in range(10):
            thickness = 4 if i % 3 == 0 else 1
            # Horizontal lines
            pygame.draw.line(self.screen, self.BLACK,
                           (self.BOARD_X, self.BOARD_Y + i * self.CELL_SIZE),
                           (self.BOARD_X + self.BOARD_SIZE, self.BOARD_Y + i * self.CELL_SIZE),
                           thickness)
            # Vertical lines
            pygame.draw.line(self.screen, self.BLACK,
                           (self.BOARD_X + i * self.CELL_SIZE, self.BOARD_Y),
                           (self.BOARD_X + i * self.CELL_SIZE, self.BOARD_Y + self.BOARD_SIZE),
                           thickness)
    
    def draw_number_buttons(self):
        """Draw number selector buttons"""
        for i in range(1, 10):
            btn = self.buttons[f'num_{i}']
            pygame.draw.rect(self.screen, self.DARK_BLUE, btn, border_radius=8)
            pygame.draw.rect(self.screen, self.BLACK, btn, 2, border_radius=8)
            
            text = self.medium_font.render(str(i), True, self.WHITE)
            text_rect = text.get_rect(center=btn.center)
            self.screen.blit(text, text_rect)
        
        # Erase button
        btn = self.buttons['erase']
        pygame.draw.rect(self.screen, self.DARK_RED, btn, border_radius=8)
        pygame.draw.rect(self.screen, self.BLACK, btn, 2, border_radius=8)
        
        text = self.medium_font.render("X", True, self.WHITE)
        text_rect = text.get_rect(center=btn.center)
        self.screen.blit(text, text_rect)
    
    def draw_control_buttons(self):
        """Draw control buttons"""
        buttons_info = [
            ('new_game', 'New Game'),
            ('hint', 'Hint (-10)'),
            ('settings', 'Settings')
        ]
        
        for btn_name, label in buttons_info:
            btn = self.buttons[btn_name]
            pygame.draw.rect(self.screen, self.DARK_BLUE, btn, border_radius=8)
            pygame.draw.rect(self.screen, self.BLACK, btn, 2, border_radius=8)
            
            text = self.small_font.render(label, True, self.WHITE)
            text_rect = text.get_rect(center=btn.center)
            self.screen.blit(text, text_rect)
    
    def draw_settings_modal(self):
        """Draw settings modal overlay"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw modal background
        modal = self.buttons['settings_modal']
        pygame.draw.rect(self.screen, self.WHITE, modal, border_radius=10)
        pygame.draw.rect(self.screen, self.DARK_BLUE, modal, 4, border_radius=10)
        
        # Draw close button
        close_btn = self.buttons['settings_close']
        pygame.draw.rect(self.screen, self.DARK_RED, close_btn, border_radius=5)
        close_text = self.medium_font.render('X', True, self.WHITE)
        close_rect = close_text.get_rect(center=close_btn.center)
        self.screen.blit(close_text, close_rect)
        
        # Title
        title = self.large_font.render('Settings', True, self.PURPLE)
        title_rect = title.get_rect(center=(modal.centerx, modal.top + 40))
        self.screen.blit(title, title_rect)
        
        # Difficulty label
        diff_label = self.medium_font.render('Difficulty:', True, self.BLACK)
        diff_label_rect = diff_label.get_rect(center=(modal.centerx, modal.top + 85))
        self.screen.blit(diff_label, diff_label_rect)
        
        # Difficulty buttons
        difficulties = ['easy', 'medium', 'hard']
        for diff in difficulties:
            btn = self.buttons[diff]
            
            # Highlight selected difficulty
            if self.difficulty == diff:
                color = self.PURPLE
            else:
                color = self.GRAY
            
            pygame.draw.rect(self.screen, color, btn, border_radius=5)
            pygame.draw.rect(self.screen, self.BLACK, btn, 2, border_radius=5)
            
            text_color = self.WHITE if self.difficulty == diff else self.BLACK
            text = self.small_font.render(diff.capitalize(), True, text_color)
            text_rect = text.get_rect(center=btn.center)
            self.screen.blit(text, text_rect)
        
        # Check button
        check_btn = self.buttons['check']
        pygame.draw.rect(self.screen, self.DARK_BLUE, check_btn, border_radius=8)
        pygame.draw.rect(self.screen, self.BLACK, check_btn, 2, border_radius=8)
        check_text = self.small_font.render('Check', True, self.WHITE)
        check_text_rect = check_text.get_rect(center=check_btn.center)
        self.screen.blit(check_text, check_text_rect)
        
        # Info text
        info_text = self.small_font.render('Click outside to close', True, self.GRAY)
        info_rect = info_text.get_rect(center=(modal.centerx, modal.bottom - 30))
        self.screen.blit(info_text, info_rect)
    
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
