"""
Sudoku Game Logic
Author: Red Donaldson
Date: March 13, 2026

Performance optimizations for 25x25 generation:
- Constraint propagation with pre-computed available value sets
- Shuffled symbol list created once per generation
- Early termination when cells have no valid options
- Efficient constraint tracking without repeated scans
"""

import random
import copy


def generate_complete_sudoku(grid_size, box_size, symbols):
    """Generate a complete valid Sudoku board using optimized algorithm"""
    board = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Pre-shuffle symbols once for randomization
    shuffled_symbols = symbols.copy()
    random.shuffle(shuffled_symbols)
    
    # Initialize constraint sets for fast validation
    row_sets = [set() for _ in range(grid_size)]
    col_sets = [set() for _ in range(grid_size)]
    box_sets = [[set() for _ in range(grid_size // box_size)] 
                for _ in range(grid_size // box_size)]
    
    fill_board_optimized(board, grid_size, box_size, shuffled_symbols,
                        row_sets, col_sets, box_sets)
    return board


def fill_board_optimized(board, grid_size, box_size, symbols, 
                        row_sets, col_sets, box_sets, pos=0):
    """
    Optimized board filling using constraint propagation.
    
    Key optimizations:
    1. Use pre-computed constraint sets (row_sets, col_sets, box_sets)
    2. Single shuffled symbol list shared across all calls
    3. Linear position tracking instead of row/col recursion
    4. Early exit when no valid symbols available
    """
    if pos == grid_size * grid_size:
        return True
    
    row = pos // grid_size
    col = pos % grid_size
    box_row = row // box_size
    box_col = col // box_size
    
    # Find valid symbols using constraint sets (O(1) lookups)
    valid_symbols = []
    for symbol in symbols:
        if (symbol not in row_sets[row] and 
            symbol not in col_sets[col] and 
            symbol not in box_sets[box_row][box_col]):
            valid_symbols.append(symbol)
    
    # Early termination: no valid options available
    if not valid_symbols:
        return False
    
    # Try each valid symbol
    for symbol in valid_symbols:
        # Place symbol and update constraints
        board[row][col] = symbol
        row_sets[row].add(symbol)
        col_sets[col].add(symbol)
        box_sets[box_row][box_col].add(symbol)
        
        # Recurse to next position
        if fill_board_optimized(board, grid_size, box_size, symbols,
                               row_sets, col_sets, box_sets, pos + 1):
            return True
        
        # Backtrack: remove symbol and restore constraints
        board[row][col] = None
        row_sets[row].remove(symbol)
        col_sets[col].remove(symbol)
        box_sets[box_row][box_col].remove(symbol)
    
    return False


def fill_board(board, grid_size, box_size, symbols, row=0, col=0):
    """Legacy fill_board function for backwards compatibility"""
    # Delegate to optimized version
    row_sets = [set() for _ in range(grid_size)]
    col_sets = [set() for _ in range(grid_size)]
    box_sets = [[set() for _ in range(grid_size // box_size)] 
                for _ in range(grid_size // box_size)]
    
    # Populate existing constraints from board
    for r in range(grid_size):
        for c in range(grid_size):
            if board[r][c] is not None:
                symbol = board[r][c]
                row_sets[r].add(symbol)
                col_sets[c].add(symbol)
                box_r = r // box_size
                box_c = c // box_size
                box_sets[box_r][box_c].add(symbol)
    
    pos = row * grid_size + col
    return fill_board_optimized(board, grid_size, box_size, symbols,
                               row_sets, col_sets, box_sets, pos)


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
