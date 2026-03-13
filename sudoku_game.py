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
        buttons['settings_close'] = pygame.Rect(modal_x + modal_width - 35, modal_y + 5, 30, 30)
        
        # Difficulty buttons in settings
        diff_y = modal_y + 100
        diff_width = 100
        diff_spacing = 20
        diff_start_x = (self.WINDOW_WIDTH - (diff_width * 3 + diff_spacing * 2)) // 2
        
        buttons['easy'] = pygame.Rect(diff_start_x, diff_y, diff_width, 35)
        buttons['medium'] = pygame.Rect(diff_start_x + diff_width + diff_spacing, 
                                       diff_y, diff_width, 35)
        buttons['hard'] = pygame.Rect(diff_start_x + (diff_width + diff_spacing) * 2, 
                                      diff_y, diff_width, 35)
        
        # Check button in settings
        buttons['check'] = pygame.Rect(diff_start_x + diff_width, diff_y + 60, diff_width, 40)
        
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
        
        if key in range(pygame.K_1, pygame.K_9 + 1):
            self.place_number(key - pygame.K_0)
        elif key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
            self.place_number(0)
    
    def draw(self):
        """Draw the game screen"""
        self.screen.fill(self.WHITE)
        
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
        
        text = self.medium_font.render("✖", True, self.WHITE)
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
        close_text = self.small_font.render('✖', True, self.WHITE)
        close_rect = close_text.get_rect(center=close_btn.center)
        self.screen.blit(close_text, close_rect)
        
        # Title
        title = self.large_font.render('Settings', True, self.PURPLE)
        title_rect = title.get_rect(center=(self.WINDOW_WIDTH // 2, modal.top + 40))
        self.screen.blit(title, title_rect)
        
        # Difficulty label
        diff_label = self.medium_font.render('Difficulty:', True, self.BLACK)
        diff_label_rect = diff_label.get_rect(center=(self.WINDOW_WIDTH // 2, modal.top + 80))
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
        check_text = self.small_font.render('Check Solution', True, self.WHITE)
        check_text_rect = check_text.get_rect(center=check_btn.center)
        self.screen.blit(check_text, check_text_rect)
        
        # Info text
        info_text = self.small_font.render('Click outside to close', True, self.GRAY)
        info_rect = info_text.get_rect(center=(self.WINDOW_WIDTH // 2, modal.bottom - 30))
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
