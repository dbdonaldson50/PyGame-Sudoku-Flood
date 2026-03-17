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


def generate_complete_sudoku(grid_size, box_size, symbols, progress_callback=None):
    """Generate a complete valid Sudoku board using simple backtracking algorithm
    
    Modified by: Red Donaldson
    Date: March 16, 2026
    
    CHANGE: Replaced complex optimized algorithm with simple proven algorithm
    REASON: Optimized version had bugs causing invalid boards for 25x25 grids  
    OPTIMIZATION: Pre-fill diagonal boxes to speed up generation significantly
    VISUAL FEEDBACK: Added progress_callback for UI updates during generation
    
    Args:
        grid_size: Size of the grid (9, 16, or 25)
        box_size: Size of each box (3, 4, or 5)
        symbols: List of symbols to use
        progress_callback: Optional function(board, progress) called periodically
    
    The optimized algorithm attempted to use:
    - Pre-filled diagonal boxes
    - Constraint caching
    - MRV heuristic
    - Constraint propagation
    
    However, it had race conditions in constraint tracking that caused
    duplicate symbols in rows/columns/boxes. This simple algorithm is
    slower but cannot produce invalid boards.
    
    Performance optimization: Pre-filling diagonal boxes is safe because
    diagonal boxes don't share rows, columns, or boxes with each other.
    This reduces the search space dramatically without introducing bugs.
    """
    board = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Pre-fill diagonal boxes (safe optimization)
    _prefill_diagonal_boxes(board, grid_size, box_size, symbols)
    
    # Call progress callback after diagonal boxes filled
    if progress_callback:
        progress_callback(board, 0.1)
    
    # Track progress for callbacks - use max position reached to avoid going backward during backtracking
    total_cells = grid_size * grid_size
    max_position = [0]  # Start from 0, will track maximum grid position reached
    
    def progress_wrapper(row, col, is_backtracking=False):
        """Wrapper to update progress during generation
        
        Uses position in grid (row * grid_size + col) as a measure of depth.
        Only updates progress when we reach a new maximum position to avoid
        progress going backward during backtracking.
        
        Always calls callback (even during backtracking) to keep spinner animated.
        
        Modified by: Red Donaldson
        Date: March 17, 2026
        """
        current_position = row * grid_size + col
        should_update_progress = current_position > max_position[0]
        
        if should_update_progress:
            max_position[0] = current_position
        
        # Call callback more frequently to keep spinner moving
        # Progress only updates when advancing, spinner always updates
        callback_frequency = max(10, grid_size)
        if progress_callback and (current_position % callback_frequency == 0 or should_update_progress):
            if should_update_progress:
                progress = 0.1 + 0.9 * (current_position / total_cells)
                progress_callback(board, min(0.99, progress))
            else:
                # During backtracking, call callback with current progress to update spinner
                progress_callback(board, None)  # None signals spinner update only
    
    if _fill_board_simple(board, grid_size, box_size, symbols, 0, 0, progress_wrapper):
        if progress_callback:
            progress_callback(board, 1.0)
        return board
    
    # This should never happen
    raise Exception("Failed to generate valid Sudoku board")


def _prefill_diagonal_boxes(board, grid_size, box_size, symbols):
    """Pre-fill diagonal boxes - they're independent so this is always safe
    
    Diagonal boxes don't share any rows, columns, or boxes with each other,
    so we can fill them independently without constraint conflicts.
    This dramatically speeds up generation for large grids.
    """
    num_boxes = grid_size // box_size
    
    for box_num in range(num_boxes):
        # Shuffle symbols for randomness
        shuffled_symbols = symbols.copy()
        random.shuffle(shuffled_symbols)
        
        # Fill this diagonal box
        box_start = box_num * box_size
        symbol_idx = 0
        
        for i in range(box_start, box_start + box_size):
            for j in range(box_start, box_start + box_size):
                board[i][j] = shuffled_symbols[symbol_idx]
                symbol_idx += 1


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


def _validate_board(board, grid_size, box_size):
    """Validate that a complete board has no duplicates in rows, columns, or boxes
    
    Added by: Red Donaldson
    Date: March 16, 2026
    """
    # Check rows
    for row in range(grid_size):
        row_values = [board[row][col] for col in range(grid_size)]
        if len(row_values) != len(set(row_values)):
            return False
    
    # Check columns
    for col in range(grid_size):
        col_values = [board[row][col] for row in range(grid_size)]
        if len(col_values) != len(set(col_values)):
            return False
    
    # Check boxes
    num_boxes = grid_size // box_size
    for box_row in range(num_boxes):
        for box_col in range(num_boxes):
            box_values = []
            box_start_row = box_row * box_size
            box_start_col = box_col * box_size
            
            for i in range(box_start_row, box_start_row + box_size):
                for j in range(box_start_col, box_start_col + box_size):
                    box_values.append(board[i][j])
            
            if len(box_values) != len(set(box_values)):
                return False
    
    return True


def _generate_complete_sudoku_fallback(grid_size, box_size, symbols):
    """Fallback generator using simpler algorithm - slower but guaranteed correct
    
    Added by: Red Donaldson
    Date: March 16, 2026
    """
    board = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    
    if _fill_board_simple(board, grid_size, box_size, symbols, 0, 0):
        return board
    
    # This should never happen, but just in case
    raise Exception("Failed to generate valid Sudoku board")


def _fill_board_simple(board, grid_size, box_size, symbols, row, col, progress_callback=None):
    """Optimized recursive backtracking with forward checking
    
    Optimizations:
    - Pre-filter valid symbols (forward checking)
    - Try symbols in smart order (least used first)
    - Early exits on impossible cases
    
    Modified by: Red Donaldson
    Date: March 17, 2026
    """
    if row == grid_size:
        return True
    if col == grid_size:
        return _fill_board_simple(board, grid_size, box_size, symbols, row + 1, 0, progress_callback)
    
    # Skip if cell already filled
    if board[row][col] is not None:
        return _fill_board_simple(board, grid_size, box_size, symbols, row, col + 1, progress_callback)
    
    # Forward checking: Get only valid symbols for this position
    valid_symbols = get_valid_symbols(board, row, col, symbols, grid_size, box_size)
    
    # Early exit if no valid options
    if not valid_symbols:
        return False
    
    # Try symbols in random order (for variety) but with valid ones only
    random.shuffle(valid_symbols)
    
    for symbol in valid_symbols:
        board[row][col] = symbol
        
        # Call progress callback
        if progress_callback:
            progress_callback(row, col, False)
        
        if _fill_board_simple(board, grid_size, box_size, symbols, row, col + 1, progress_callback):
            return True
        
        board[row][col] = None
        
        # Update spinner during backtracking
        if progress_callback:
            progress_callback(row, col, True)
    
    return False


def get_valid_symbols(board, row, col, symbols, grid_size, box_size):
    """Get list of symbols that can be placed at (row, col)
    
    Forward checking optimization: Pre-filter valid options.
    Much faster than trying all symbols and checking validity.
    
    Added by: Red Donaldson
    Date: March 17, 2026
    """
    used = set()
    
    # Collect symbols already used in row
    for c in range(grid_size):
        if board[row][c] is not None:
            used.add(board[row][c])
    
    # Collect symbols already used in column
    for r in range(grid_size):
        if board[r][col] is not None:
            used.add(board[r][col])
    
    # Collect symbols already used in box
    box_row = (row // box_size) * box_size
    box_col = (col // box_size) * box_size
    for i in range(box_row, box_row + box_size):
        for j in range(box_col, box_col + box_size):
            if board[i][j] is not None:
                used.add(board[i][j])
    
    # Return symbols not yet used
    return [s for s in symbols if s not in used]


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
    """Remove numbers to create the puzzle with 180° rotational symmetry
    
    Modified by: Red Donaldson
    Date: March 14, 2026
    
    The pattern of given digits now follows 180° rotational symmetry:
    - If cell (r,c) is removed, cell (grid_size-1-r, grid_size-1-c) is also removed
    - Center cell (for odd grid sizes) is handled independently
    - This creates visually pleasing, professionally symmetric puzzles
    """
    removed = 0
    attempts = 0
    max_attempts = cells_to_remove * 5  # Increased for symmetry constraints
    
    # Generate symmetric cell pairs for 180° rotational symmetry
    cell_pairs = []
    center_cell = None
    
    # Track all cells and create symmetric pairs
    processed = set()
    
    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) in processed:
                continue
            
            # Calculate symmetric counterpart (180° rotation)
            sym_i = grid_size - 1 - i
            sym_j = grid_size - 1 - j
            
            # Check if this is the center cell (maps to itself)
            if i == sym_i and j == sym_j:
                center_cell = (i, j)
            else:
                # Add as a symmetric pair
                cell_pairs.append(((i, j), (sym_i, sym_j)))
                processed.add((i, j))
                processed.add((sym_i, sym_j))
    
    # Shuffle pairs for randomization
    random.shuffle(cell_pairs)
    
    # Remove cells in symmetric pairs
    pair_idx = 0
    while removed < cells_to_remove and attempts < max_attempts:
        attempts += 1
        
        # Determine how many cells we need to remove
        cells_needed = cells_to_remove - removed
        
        # Try to remove a symmetric pair (2 cells)
        if cells_needed >= 2 and pair_idx < len(cell_pairs):
            cell1, cell2 = cell_pairs[pair_idx]
            pair_idx += 1
            
            # Remove both cells in the pair
            if board[cell1[0]][cell1[1]] is not None and board[cell2[0]][cell2[1]] is not None:
                board[cell1[0]][cell1[1]] = None
                board[cell2[0]][cell2[1]] = None
                removed += 2
        
        # If we need exactly 1 more cell, remove center cell (odd grid sizes)
        elif cells_needed == 1 and center_cell is not None:
            if board[center_cell[0]][center_cell[1]] is not None:
                board[center_cell[0]][center_cell[1]] = None
                removed += 1
            break
        
        # If we've run out of pairs, break
        elif pair_idx >= len(cell_pairs):
            break


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
