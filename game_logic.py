"""
Sudoku Game Logic - Optimized for Performance
Author: Red Donaldson
Date: March 13, 2026

Optimizations:
- Pre-fill diagonal boxes for faster initial state
- Constraint caching (used values in rows/cols/boxes)
- MRV heuristic (Most Constrained Variable first)
- Set-based lookups for O(1) constraint checking
- Early exit conditions in validation
"""

import random
import copy


def generate_complete_sudoku(grid_size, box_size, symbols):
    """Generate a complete valid Sudoku board using highly optimized algorithm
    
    Strategy:
    1. Pre-fill diagonal boxes (independent, fast)
    2. Fill first row (constrains column choices)
    3. Fill first column (constrains row choices)
    4. Use MRV heuristic with constraint propagation for rest
    
    This approach dramatically reduces search space and backtracking
    """
    board = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Initialize constraint tracking sets for O(1) lookups
    symbols_set = set(symbols)
    row_constraints = [set() for _ in range(grid_size)]
    col_constraints = [set() for _ in range(grid_size)]
    box_constraints = [set() for _ in range(grid_size)]
    
    # Pre-fill diagonal boxes (they don't constrain each other)
    _fill_diagonal_boxes(board, grid_size, box_size, symbols, 
                         row_constraints, col_constraints, box_constraints)
    
    # Fill first row (provides strong column constraints)
    if not _fill_first_row(board, grid_size, box_size, symbols_set,
                           row_constraints, col_constraints, box_constraints):
        # Retry with fresh board if first row fails
        return generate_complete_sudoku(grid_size, box_size, symbols)
    
    # Fill first column (provides strong row constraints)
    if not _fill_first_column(board, grid_size, box_size, symbols_set,
                              row_constraints, col_constraints, box_constraints):
        # Retry with fresh board if first column fails
        return generate_complete_sudoku(grid_size, box_size, symbols)
    
    # Fill remaining cells with optimized backtracking
    if not _fill_remaining(board, grid_size, box_size, symbols_set,
                          row_constraints, col_constraints, box_constraints):
        # Retry if filling fails (rare with this approach)
        return generate_complete_sudoku(grid_size, box_size, symbols)
    
    return board


def _fill_first_row(board, grid_size, box_size, symbols_set,
                    row_constraints, col_constraints, box_constraints):
    """Fill the first row completely to constrain column choices"""
    row = 0
    
    for col in range(grid_size):
        # Skip if already filled (from diagonal boxes)
        if board[row][col] is not None:
            continue
        
        # Get valid symbols for this position
        valid = _get_valid_symbols(row, col, symbols_set, row_constraints,
                                   col_constraints, box_constraints, box_size, grid_size)
        
        if not valid:
            return False  # No valid options, need to retry
        
        # Pick a random valid symbol
        symbol = random.choice(valid)
        board[row][col] = symbol
        
        # Update constraints
        box_idx = _get_box_index(row, col, box_size, grid_size)
        row_constraints[row].add(symbol)
        col_constraints[col].add(symbol)
        box_constraints[box_idx].add(symbol)
    
    return True


def _fill_first_column(board, grid_size, box_size, symbols_set,
                       row_constraints, col_constraints, box_constraints):
    """Fill the first column completely to constrain row choices"""
    col = 0
    
    for row in range(grid_size):
        # Skip if already filled (from diagonal boxes or first row)
        if board[row][col] is not None:
            continue
        
        # Get valid symbols for this position
        valid = _get_valid_symbols(row, col, symbols_set, row_constraints,
                                   col_constraints, box_constraints, box_size, grid_size)
        
        if not valid:
            return False  # No valid options, need to retry
        
        # Pick a random valid symbol
        symbol = random.choice(valid)
        board[row][col] = symbol
        
        # Update constraints
        box_idx = _get_box_index(row, col, box_size, grid_size)
        row_constraints[row].add(symbol)
        col_constraints[col].add(symbol)
        box_constraints[box_idx].add(symbol)
    
    return True


def _fill_diagonal_boxes(board, grid_size, box_size, symbols,
                         row_constraints, col_constraints, box_constraints):
    """Pre-fill diagonal boxes (they're independent) for faster generation"""
    num_boxes = grid_size // box_size
    
    for box_idx in range(num_boxes):
        # Shuffle symbols for randomness
        box_symbols = symbols.copy()
        random.shuffle(box_symbols)
        
        # Fill this diagonal box
        box_start = box_idx * box_size
        symbol_idx = 0
        
        for i in range(box_start, box_start + box_size):
            for j in range(box_start, box_start + box_size):
                symbol = box_symbols[symbol_idx]
                board[i][j] = symbol
                
                # Update constraint sets
                row_constraints[i].add(symbol)
                col_constraints[j].add(symbol)
                box_constraints[_get_box_index(i, j, box_size, grid_size)].add(symbol)
                
                symbol_idx += 1


def _get_box_index(row, col, box_size, grid_size):
    """Calculate box index for constraint tracking"""
    return (row // box_size) * (grid_size // box_size) + (col // box_size)


def _get_valid_symbols(row, col, symbols_set, row_constraints, 
                       col_constraints, box_constraints, box_size, grid_size):
    """Get valid symbols for a cell using cached constraints - O(1) lookups"""
    box_idx = _get_box_index(row, col, box_size, grid_size)
    
    # Use set operations for fast constraint checking
    used = row_constraints[row] | col_constraints[col] | box_constraints[box_idx]
    return list(symbols_set - used)


def _find_best_cell(board, grid_size, box_size, symbols_set,
                    row_constraints, col_constraints, box_constraints):
    """Find empty cell with fewest valid options (MRV heuristic)
    
    This dramatically reduces backtracking by filling constrained cells first
    
    Returns: (cell, valid_options) or (None, None) if no empty cells
    """
    min_options = float('inf')
    best_cell = None
    best_options = None
    
    for i in range(grid_size):
        for j in range(grid_size):
            if board[i][j] is None:
                valid_symbols = _get_valid_symbols(
                    i, j, symbols_set, row_constraints, 
                    col_constraints, box_constraints, box_size, grid_size
                )
                
                num_options = len(valid_symbols)
                
                # Early exit if no options (fail fast)
                if num_options == 0:
                    return (i, j), []
                
                # Found cell with fewer options
                if num_options < min_options:
                    min_options = num_options
                    best_cell = (i, j)
                    best_options = valid_symbols
                    
                    # Early exit if only one option (will fill immediately)
                    if min_options == 1:
                        return best_cell, best_options
    
    # Return None, None if no empty cells found
    if best_cell is None:
        return None, None
    
    return best_cell, best_options


def _fill_remaining(board, grid_size, box_size, symbols_set,
                    row_constraints, col_constraints, box_constraints):
    """Fill remaining cells using optimized backtracking with constraint propagation
    
    Uses a two-phase approach:
    1. Constraint propagation (fill naked singles - cells with only one option)
    2. Backtracking with MRV heuristic for remaining cells
    """
    # Phase 1: Constraint propagation - fill all naked singles
    changes_made = True
    while changes_made:
        changes_made = False
        
        for i in range(grid_size):
            for j in range(grid_size):
                if board[i][j] is None:
                    valid = _get_valid_symbols(i, j, symbols_set, row_constraints,
                                              col_constraints, box_constraints, box_size, grid_size)
                    
                    # Naked single - only one valid option
                    if len(valid) == 1:
                        symbol = valid[0]
                        board[i][j] = symbol
                        
                        # Update constraints
                        box_idx = _get_box_index(i, j, box_size, grid_size)
                        row_constraints[i].add(symbol)
                        col_constraints[j].add(symbol)
                        box_constraints[box_idx].add(symbol)
                        
                        changes_made = True
                    
                    # Dead end - no valid options
                    elif len(valid) == 0:
                        return False
    
    # Phase 2: Check if board is complete
    all_filled = all(board[i][j] is not None 
                    for i in range(grid_size) 
                    for j in range(grid_size))
    
    if all_filled:
        return True
    
    # Phase 3: Backtracking with MRV for remaining cells
    return _backtrack_remaining(board, grid_size, box_size, symbols_set,
                               row_constraints, col_constraints, box_constraints)


def _backtrack_remaining(board, grid_size, box_size, symbols_set,
                        row_constraints, col_constraints, box_constraints):
    """Backtracking with MRV heuristic for cells that couldn't be filled by constraint propagation"""
    # Find best cell to fill next (most constrained)
    cell, valid_symbols = _find_best_cell(
        board, grid_size, box_size, symbols_set,
        row_constraints, col_constraints, box_constraints
    )
    
    # Base case: no empty cells (success)
    if cell is None:
        return True
    
    # No valid options for this cell (dead end)
    if not valid_symbols:
        return False
    
    row, col = cell
    box_idx = _get_box_index(row, col, box_size, grid_size)
    
    # Try each valid symbol in random order
    random.shuffle(valid_symbols)
    
    for symbol in valid_symbols:
        # Place symbol and update constraints
        board[row][col] = symbol
        row_constraints[row].add(symbol)
        col_constraints[col].add(symbol)
        box_constraints[box_idx].add(symbol)
        
        # Recurse with constraint propagation
        if _fill_remaining(board, grid_size, box_size, symbols_set,
                          row_constraints, col_constraints, box_constraints):
            return True
        
        # Backtrack
        board[row][col] = None
        row_constraints[row].discard(symbol)
        col_constraints[col].discard(symbol)
        box_constraints[box_idx].discard(symbol)
    
    return False


def fill_board(board, grid_size, box_size, symbols, row=0, col=0):
    """Legacy function - kept for compatibility
    
    Note: Use generate_complete_sudoku() directly for better performance
    """
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
    """Check if placing symbol at (row, col) is valid
    
    Optimized with early exits
    """
    # Check row - early exit on first match
    for c in range(grid_size):
        if board[row][c] == symbol:
            return False
    
    # Check column - early exit on first match
    for r in range(grid_size):
        if board[r][col] == symbol:
            return False
    
    # Check box - early exit on first match
    box_row = (row // box_size) * box_size
    box_col = (col // box_size) * box_size
    for i in range(box_row, box_row + box_size):
        for j in range(box_col, box_col + box_size):
            if board[i][j] == symbol:
                return False
    
    return True


def remove_numbers(board, grid_size, cells_to_remove):
    """Remove numbers to create the puzzle - optimized for better distribution"""
    removed = 0
    attempts = 0
    max_attempts = cells_to_remove * 3  # Prevent infinite loops
    
    # Create list of all cell positions for better randomization
    all_positions = [(i, j) for i in range(grid_size) for j in range(grid_size)]
    random.shuffle(all_positions)
    
    pos_idx = 0
    while removed < cells_to_remove and attempts < max_attempts:
        row, col = all_positions[pos_idx % len(all_positions)]
        pos_idx += 1
        attempts += 1
        
        if board[row][col] is not None:
            board[row][col] = None
            removed += 1


def get_possible_values(board, row, col, grid_size, box_size, symbols):
    """Get all possible values for a given cell - optimized with sets"""
    if board[row][col] is not None:
        return set()
    
    possible = set(symbols)
    
    # Use set for faster lookups - build used set in one pass
    used = set()
    
    # Collect values in same row
    for c in range(grid_size):
        if board[row][c] is not None:
            used.add(board[row][c])
    
    # Collect values in same column
    for r in range(grid_size):
        if board[r][col] is not None:
            used.add(board[r][col])
    
    # Collect values in same box
    box_row = (row // box_size) * box_size
    box_col = (col // box_size) * box_size
    for i in range(box_row, box_row + box_size):
        for j in range(box_col, box_col + box_size):
            if board[i][j] is not None:
                used.add(board[i][j])
    
    # Return difference in O(n) where n = len(symbols)
    return possible - used


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
