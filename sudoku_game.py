#!/usr/bin/env python3
"""
Sudoku Game with Points and Lives System
Author: Red Donaldson
Date: March 13, 2026
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import copy
from datetime import datetime, timedelta


class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.resizable(False, False)
        
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
        self.timer_running = False
        
        # Difficulty settings
        self.difficulty_settings = {
            'easy': {'cells_to_remove': 30, 'lives': 3, 'points_per_cell': 5},
            'medium': {'cells_to_remove': 40, 'lives': 3, 'points_per_cell': 10},
            'hard': {'cells_to_remove': 50, 'lives': 5, 'points_per_cell': 15}
        }
        
        # Colors
        self.colors = {
            'bg': '#f0f0f0',
            'board_bg': 'white',
            'given': '#f5f5f5',
            'selected': '#bbdefb',
            'correct': '#c8e6c9',
            'incorrect': '#ffcdd2',
            'border': '#333333',
            'text': '#333333',
            'given_text': '#000000'
        }
        
        # GUI elements
        self.cells = []
        self.cell_entries = []
        
        self.setup_gui()
        self.new_game()
    
    def setup_gui(self):
        """Create the GUI layout"""
        self.root.configure(bg=self.colors['bg'])
        
        # Title
        title_label = tk.Label(
            self.root,
            text="Sudoku Game",
            font=('Arial', 24, 'bold'),
            bg=self.colors['bg'],
            fg='#667eea'
        )
        title_label.pack(pady=10)
        
        # Info panel
        info_frame = tk.Frame(self.root, bg=self.colors['bg'])
        info_frame.pack(pady=10)
        
        # Lives
        lives_frame = tk.Frame(info_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        lives_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(lives_frame, text="Lives", font=('Arial', 10), bg='white').pack()
        self.lives_label = tk.Label(lives_frame, text="3", font=('Arial', 18, 'bold'), 
                                     fg='#e74c3c', bg='white')
        self.lives_label.pack(padx=20, pady=5)
        
        # Score
        score_frame = tk.Frame(info_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        score_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(score_frame, text="Score", font=('Arial', 10), bg='white').pack()
        self.score_label = tk.Label(score_frame, text="0", font=('Arial', 18, 'bold'), 
                                     fg='#27ae60', bg='white')
        self.score_label.pack(padx=20, pady=5)
        
        # Timer
        timer_frame = tk.Frame(info_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        timer_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(timer_frame, text="Time", font=('Arial', 10), bg='white').pack()
        self.timer_label = tk.Label(timer_frame, text="00:00", font=('Arial', 18, 'bold'), 
                                     fg='#333333', bg='white')
        self.timer_label.pack(padx=20, pady=5)
        
        # Message area
        self.message_label = tk.Label(
            self.root,
            text="",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg='#333333',
            height=2
        )
        self.message_label.pack(pady=5)
        
        # Sudoku board
        board_frame = tk.Frame(self.root, bg=self.colors['border'], relief=tk.RAISED, borderwidth=3)
        board_frame.pack(pady=10)
        
        for i in range(9):
            row_cells = []
            for j in range(9):
                # Create frame for each cell
                cell_frame = tk.Frame(
                    board_frame,
                    bg=self.colors['board_bg'],
                    width=50,
                    height=50,
                    relief=tk.SOLID,
                    borderwidth=1
                )
                
                # Add thicker borders for 3x3 boxes
                padx = (3 if j % 3 == 0 else 1, 3 if j % 3 == 2 else 1)
                pady = (3 if i % 3 == 0 else 1, 3 if i % 3 == 2 else 1)
                
                cell_frame.grid(row=i, column=j, padx=padx, pady=pady)
                cell_frame.grid_propagate(False)
                
                # Create label for cell
                cell_label = tk.Label(
                    cell_frame,
                    text="",
                    font=('Arial', 20, 'bold'),
                    bg=self.colors['board_bg'],
                    fg=self.colors['text']
                )
                cell_label.pack(expand=True, fill=tk.BOTH)
                cell_label.bind('<Button-1>', lambda e, r=i, c=j: self.select_cell(r, c))
                
                row_cells.append({'frame': cell_frame, 'label': cell_label})
            
            self.cells.append(row_cells)
        
        # Number selector
        number_frame = tk.Frame(self.root, bg=self.colors['bg'])
        number_frame.pack(pady=10)
        
        for i in range(1, 10):
            btn = tk.Button(
                number_frame,
                text=str(i),
                font=('Arial', 14, 'bold'),
                width=3,
                height=1,
                command=lambda n=i: self.place_number(n),
                bg='white',
                fg='#667eea',
                relief=tk.RAISED,
                borderwidth=2
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        # Erase button
        erase_btn = tk.Button(
            number_frame,
            text="✖",
            font=('Arial', 14, 'bold'),
            width=3,
            height=1,
            command=lambda: self.place_number(0),
            bg='white',
            fg='#e74c3c',
            relief=tk.RAISED,
            borderwidth=2
        )
        erase_btn.pack(side=tk.LEFT, padx=3)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg=self.colors['bg'])
        control_frame.pack(pady=10)
        
        new_game_btn = tk.Button(
            control_frame,
            text="New Game",
            font=('Arial', 12, 'bold'),
            command=self.new_game,
            bg='#667eea',
            fg='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=15,
            pady=5
        )
        new_game_btn.pack(side=tk.LEFT, padx=5)
        
        hint_btn = tk.Button(
            control_frame,
            text="Hint (-10 pts)",
            font=('Arial', 12, 'bold'),
            command=self.give_hint,
            bg='#667eea',
            fg='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=15,
            pady=5
        )
        hint_btn.pack(side=tk.LEFT, padx=5)
        
        check_btn = tk.Button(
            control_frame,
            text="Check Solution",
            font=('Arial', 12, 'bold'),
            command=self.check_solution,
            bg='#667eea',
            fg='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=15,
            pady=5
        )
        check_btn.pack(side=tk.LEFT, padx=5)
        
        # Difficulty selector
        difficulty_frame = tk.Frame(self.root, bg=self.colors['bg'])
        difficulty_frame.pack(pady=10)
        
        tk.Label(
            difficulty_frame,
            text="Difficulty:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg']
        ).pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value='medium')
        difficulty_combo = ttk.Combobox(
            difficulty_frame,
            textvariable=self.difficulty_var,
            values=['easy', 'medium', 'hard'],
            state='readonly',
            font=('Arial', 11),
            width=15
        )
        difficulty_combo.pack(side=tk.LEFT, padx=5)
        difficulty_combo.bind('<<ComboboxSelected>>', 
                            lambda e: setattr(self, 'difficulty', self.difficulty_var.get()))
        
        # Keyboard bindings
        self.root.bind('<Key>', self.on_key_press)
    
    def new_game(self):
        """Start a new game"""
        self.game_over = False
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
        self.update_display()
        self.render_board()
        self.start_timer()
        self.show_message("New game started! Good luck!", "#0c5460", "#d1ecf1")
    
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
    
    def select_cell(self, row, col):
        """Select a cell on the board"""
        if self.game_over:
            return
        
        # Can't select pre-filled cells
        if self.initial_board[row][col] != 0:
            return
        
        self.selected_cell = (row, col)
        self.render_board()
    
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
            self.render_board()
            return
        
        # Check if correct
        is_correct = self.solution[row][col] == number
        
        if is_correct:
            self.board[row][col] = number
            points = self.difficulty_settings[self.difficulty]['points_per_cell']
            self.score += points
            self.show_message(f"Correct! +{points} points", "#155724", "#d4edda")
            
            # Check if puzzle complete
            if self.is_puzzle_complete():
                self.win_game()
        else:
            self.lives -= 1
            self.show_message("Wrong! -1 life", "#721c24", "#f8d7da")
            
            # Flash incorrect
            cell = self.cells[row][col]
            original_bg = cell['frame']['bg']
            cell['frame'].configure(bg=self.colors['incorrect'])
            cell['label'].configure(bg=self.colors['incorrect'])
            self.root.after(500, lambda: (
                cell['frame'].configure(bg=original_bg),
                cell['label'].configure(bg=original_bg)
            ))
            
            if self.lives <= 0:
                self.lose_game()
        
        self.update_display()
        self.render_board()
    
    def render_board(self):
        """Render the current board state"""
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                value = self.board[i][j]
                
                # Set text
                cell['label']['text'] = str(value) if value != 0 else ""
                
                # Set colors
                if self.initial_board[i][j] != 0:
                    # Given cells
                    cell['frame'].configure(bg=self.colors['given'])
                    cell['label'].configure(bg=self.colors['given'], 
                                          fg=self.colors['given_text'])
                elif value != 0 and value == self.solution[i][j]:
                    # Correct cells
                    cell['frame'].configure(bg=self.colors['correct'])
                    cell['label'].configure(bg=self.colors['correct'], 
                                          fg=self.colors['text'])
                else:
                    # Empty or user cells
                    cell['frame'].configure(bg=self.colors['board_bg'])
                    cell['label'].configure(bg=self.colors['board_bg'], 
                                          fg=self.colors['text'])
                
                # Highlight selected cell
                if self.selected_cell and self.selected_cell == (i, j):
                    cell['frame'].configure(bg=self.colors['selected'])
                    cell['label'].configure(bg=self.colors['selected'])
    
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
                self.show_message("Hint given! -10 points", "#0c5460", "#d1ecf1")
                
                if self.is_puzzle_complete():
                    self.win_game()
                
                self.update_display()
                self.render_board()
        else:
            self.show_message("Not enough points for a hint! (Need 10 points)", 
                            "#721c24", "#f8d7da")
    
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
            self.show_message("Place some numbers first!", "#0c5460", "#d1ecf1")
        else:
            percentage = round((correct_count / total_filled) * 100)
            self.show_message(
                f"{correct_count}/{total_filled} correct ({percentage}%)",
                "#0c5460", "#d1ecf1"
            )
    
    def win_game(self):
        """Handle winning the game"""
        self.game_over = True
        self.stop_timer()
        
        time_bonus = max(0, 500 - self.seconds)
        lives_bonus = self.lives * 50
        total_score = self.score + time_bonus + lives_bonus
        
        message = (f"🎉 You Win!\n"
                  f"Total Score: {total_score}\n"
                  f"(Base: {self.score} + Time: {time_bonus} + Lives: {lives_bonus})")
        
        messagebox.showinfo("Congratulations!", message)
        self.show_message(f"You Win! Total: {total_score}", "#155724", "#d4edda")
    
    def lose_game(self):
        """Handle losing the game"""
        self.game_over = True
        self.stop_timer()
        
        message = f"💀 Game Over!\nYou ran out of lives.\nFinal Score: {self.score}"
        messagebox.showinfo("Game Over", message)
        self.show_message(f"Game Over! Score: {self.score}", "#721c24", "#f8d7da")
        
        # Show solution
        self.root.after(1500, lambda: (
            setattr(self, 'board', copy.deepcopy(self.solution)),
            self.render_board()
        ))
    
    def start_timer(self):
        """Start the game timer"""
        self.timer_running = True
        self.update_timer()
    
    def stop_timer(self):
        """Stop the game timer"""
        self.timer_running = False
    
    def update_timer(self):
        """Update the timer display"""
        if self.timer_running and not self.game_over:
            self.seconds += 1
            minutes = self.seconds // 60
            seconds = self.seconds % 60
            self.timer_label['text'] = f"{minutes:02d}:{seconds:02d}"
            self.root.after(1000, self.update_timer)
    
    def update_display(self):
        """Update the score and lives display"""
        self.lives_label['text'] = str(self.lives)
        self.score_label['text'] = str(self.score)
    
    def show_message(self, text, fg, bg):
        """Show a message to the user"""
        self.message_label['text'] = text
        self.message_label['fg'] = fg
        self.message_label['bg'] = bg
        
        # Clear message after 3 seconds
        self.root.after(3000, lambda: self.message_label.configure(text="", 
                                                                   bg=self.colors['bg']))
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        if self.game_over:
            return
        
        if event.char in '123456789':
            self.place_number(int(event.char))
        elif event.keysym in ['BackSpace', 'Delete']:
            self.place_number(0)


def main():
    """Main entry point"""
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
