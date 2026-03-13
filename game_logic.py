"""
Sudoku Game Logic
Author: Red Donaldson
Date: March 13, 2026
"""

import random
import copy


def generate_complete_sudoku(grid_size, box_size, symbols):
    """Generate a complete valid Sudoku board"""
    board = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    fill_board(board, grid_size, box_size, symbols)
    return board


def fill_board(board, grid_size, box_size, symbols, row=0, col=0):
    """Fill the Sudoku board using backtracking"""
    if row == grid_size:
        return True
    if col == grid_size:
        return fill_board(board, grid_size, box_size, symbols, row + 1, 0)
    
    symbols_copy = symbols.copy()
    random.shuffle(symbols_copy)
    
    for symbol in symbols_copy:
        if is_valid_placement(board, row, col, symbol, grid_size, box_size):
            board[row][col] = symbol
            if fill_board(board, grid_size, box_size, symbols, row, col + 1):
                return True
            board[row][col] = None
    
    return False


def is_valid_placement(board, row, col, symbol, grid_size, box_size):
    """Check if placing symbol at (row, col) is valid"""
    # Check row
    for c in range(grid_size):
        if board[row][c] == symbol:
            return False
    
    # Check column
    for r in range(grid_size):
        if board[r][col] == symbol:
            return False
    
    # Check box
    box_row = (row // box_size) * box_size
    box_col = (col // box_size) * box_size
    for i in range(box_row, box_row + box_size):
        for j in range(box_col, box_col + box_size):
            if board[i][j] == symbol:
                return False
    
    return True


def remove_numbers(board, grid_size, cells_to_remove):
    """Remove numbers to create the puzzle"""
    removed = 0
    
    while removed < cells_to_remove:
        row = random.randint(0, grid_size - 1)
        col = random.randint(0, grid_size - 1)
        
        if board[row][col] is not None:
            board[row][col] = None
            removed += 1


def get_possible_values(board, row, col, grid_size, box_size, symbols):
    """Get all possible values for a given cell"""
    if board[row][col] is not None:
        return set()
    
    possible = set(symbols)
    
    # Remove values in same row
    for c in range(grid_size):
        if board[row][c] is not None:
            possible.discard(board[row][c])
    
    # Remove values in same column
    for r in range(grid_size):
        if board[r][col] is not None:
            possible.discard(board[r][col])
    
    # Remove values in same box
    box_row = (row // box_size) * box_size
    box_col = (col // box_size) * box_size
    for i in range(box_row, box_row + box_size):
        for j in range(box_col, box_col + box_size):
            if board[i][j] is not None:
                possible.discard(board[i][j])
    
    return possible


def find_auto_fill_cells(board, initial_board, grid_size, box_size, symbols, source_cell=None):
    """Find cells that can be auto-filled (only one possible value)"""
    filled_sequence = []
    changes_made = True
    
    # Create a temporary board to simulate the fills
    temp_board = [row[:] for row in board]
    
    # Keep looping until no more single-possibility cells are found
    while changes_made:
        changes_made = False
        
        for i in range(grid_size):
            for j in range(grid_size):
                # Skip cells that are already filled or initially given
                if temp_board[i][j] is not None or initial_board[i][j] is not None:
                    continue
                
                # Get possible values based on temp board
                possible = get_possible_values(temp_board, i, j, grid_size, box_size, symbols)
                
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
    
    return filled_sequence


def is_puzzle_complete(board, solution, grid_size):
    """Check if the puzzle is complete and correct"""
    for i in range(grid_size):
        for j in range(grid_size):
            if board[i][j] != solution[i][j]:
                return False
    return True


def check_solution_status(board, solution, initial_board, grid_size):
    """Check the current solution status
    
    Returns:
        tuple: (correct_count, total_filled, wrong_count)
    """
    correct_count = 0
    total_filled = 0
    
    for i in range(grid_size):
        for j in range(grid_size):
            if board[i][j] is not None and initial_board[i][j] is None:
                total_filled += 1
                if board[i][j] == solution[i][j]:
                    correct_count += 1
    
    wrong_count = total_filled - correct_count
    return (correct_count, total_filled, wrong_count)
