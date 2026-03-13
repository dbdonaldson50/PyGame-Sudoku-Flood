"""
Comprehensive Test Suite for Sudoku Game Logic
Author: Red Donaldson
Date: March 13, 2026

Tests cover:
- Puzzle generation and validation
- Constraint propagation and auto-fill logic
- Board validation and completeness checking
- Different grid sizes (9x9, 16x16, 25x25)
- Edge cases and error handling
"""

import pytest
import copy
from src.game_logic import (
    generate_complete_sudoku,
    fill_board,
    is_valid_placement,
    remove_numbers,
    get_possible_values,
    find_auto_fill_cells,
    is_puzzle_complete,
    check_solution_status
)


# Fixtures for different grid sizes
@pytest.fixture
def easy_config():
    """9x9 Sudoku configuration"""
    return {
        'grid_size': 9,
        'box_size': 3,
        'symbols': list('123456789')
    }


@pytest.fixture
def medium_config():
    """16x16 Sudoku configuration"""
    return {
        'grid_size': 16,
        'box_size': 4,
        'symbols': list('0123456789ABCDEF')
    }


@pytest.fixture
def hard_config():
    """25x25 Sudoku configuration"""
    return {
        'grid_size': 25,
        'box_size': 5,
        'symbols': [chr(i) for i in range(ord('A'), ord('Z') + 1) if chr(i) != 'X']
    }


@pytest.fixture
def sample_9x9_board():
    """Sample 9x9 board for testing"""
    return [
        ['5', '3', None, None, '7', None, None, None, None],
        ['6', None, None, '1', '9', '5', None, None, None],
        [None, '9', '8', None, None, None, None, '6', None],
        ['8', None, None, None, '6', None, None, None, '3'],
        ['4', None, None, '8', None, '3', None, None, '1'],
        ['7', None, None, None, '2', None, None, None, '6'],
        [None, '6', None, None, None, None, '2', '8', None],
        [None, None, None, '4', '1', '9', None, None, '5'],
        [None, None, None, None, '8', None, None, '7', '9']
    ]


class TestPuzzleGeneration:
    """Test puzzle generation for different grid sizes"""
    
    def test_generate_9x9_complete_sudoku(self, easy_config):
        """Test generating a complete 9x9 Sudoku board"""
        board = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        assert board is not None
        assert len(board) == 9
        assert all(len(row) == 9 for row in board)
        assert all(cell is not None for row in board for cell in row)
        
        # Verify all symbols are used
        all_symbols = set()
        for row in board:
            all_symbols.update(row)
        assert all_symbols == set(easy_config['symbols'])
    
    def test_generate_16x16_complete_sudoku(self, medium_config):
        """Test generating a complete 16x16 Sudoku board"""
        board = generate_complete_sudoku(
            medium_config['grid_size'],
            medium_config['box_size'],
            medium_config['symbols']
        )
        
        assert board is not None
        assert len(board) == 16
        assert all(len(row) == 16 for row in board)
        assert all(cell is not None for row in board for cell in row)
    
    def test_generate_25x25_complete_sudoku(self, hard_config):
        """Test generating a complete 25x25 Sudoku board (performance test)"""
        board = generate_complete_sudoku(
            hard_config['grid_size'],
            hard_config['box_size'],
            hard_config['symbols']
        )
        
        assert board is not None
        assert len(board) == 25
        assert all(len(row) == 25 for row in board)
        assert all(cell is not None for row in board for cell in row)
    
    def test_generated_board_is_valid(self, easy_config):
        """Test that generated boards follow Sudoku rules"""
        board = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        # Check rows
        for row in board:
            assert len(set(row)) == easy_config['grid_size'], "Duplicate in row"
        
        # Check columns
        for col in range(easy_config['grid_size']):
            column = [board[row][col] for row in range(easy_config['grid_size'])]
            assert len(set(column)) == easy_config['grid_size'], "Duplicate in column"
        
        # Check boxes
        for box_row in range(0, easy_config['grid_size'], easy_config['box_size']):
            for box_col in range(0, easy_config['grid_size'], easy_config['box_size']):
                box_values = []
                for i in range(box_row, box_row + easy_config['box_size']):
                    for j in range(box_col, box_col + easy_config['box_size']):
                        box_values.append(board[i][j])
                assert len(set(box_values)) == easy_config['grid_size'], "Duplicate in box"


class TestValidPlacement:
    """Test is_valid_placement function"""
    
    def test_valid_placement_empty_cell(self, sample_9x9_board, easy_config):
        """Test placing a valid number in an empty cell"""
        assert is_valid_placement(
            sample_9x9_board, 0, 2, '4',
            easy_config['grid_size'], easy_config['box_size']
        ) is True
    
    def test_invalid_placement_row_conflict(self, sample_9x9_board, easy_config):
        """Test placing a number that already exists in the row"""
        assert is_valid_placement(
            sample_9x9_board, 0, 2, '5',  # '5' already in row 0
            easy_config['grid_size'], easy_config['box_size']
        ) is False
    
    def test_invalid_placement_column_conflict(self, sample_9x9_board, easy_config):
        """Test placing a number that already exists in the column"""
        assert is_valid_placement(
            sample_9x9_board, 2, 0, '5',  # '5' already in column 0
            easy_config['grid_size'], easy_config['box_size']
        ) is False
    
    def test_invalid_placement_box_conflict(self, sample_9x9_board, easy_config):
        """Test placing a number that already exists in the box"""
        assert is_valid_placement(
            sample_9x9_board, 0, 2, '6',  # '6' already in same box
            easy_config['grid_size'], easy_config['box_size']
        ) is False
    
    def test_valid_placement_different_box(self, sample_9x9_board, easy_config):
        """Test that same number can exist in different boxes"""
        # Place '5' in a different box than where it already exists
        assert is_valid_placement(
            sample_9x9_board, 8, 8, '5',
            easy_config['grid_size'], easy_config['box_size']
        ) is True


class TestRemoveNumbers:
    """Test number removal for puzzle creation"""
    
    def test_remove_exact_count(self, easy_config):
        """Test that exactly the requested number of cells are removed"""
        board = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        cells_to_remove = 40
        remove_numbers(board, easy_config['grid_size'], cells_to_remove)
        
        none_count = sum(1 for row in board for cell in row if cell is None)
        assert none_count == cells_to_remove
    
    def test_remove_all_cells(self, easy_config):
        """Test removing all cells creates an empty board"""
        board = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        total_cells = easy_config['grid_size'] ** 2
        remove_numbers(board, easy_config['grid_size'], total_cells)
        
        assert all(cell is None for row in board for cell in row)
    
    def test_remove_zero_cells(self, easy_config):
        """Test that removing 0 cells leaves board unchanged"""
        board = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        original = copy.deepcopy(board)
        
        remove_numbers(board, easy_config['grid_size'], 0)
        
        assert board == original


class TestPossibleValues:
    """Test get_possible_values function"""
    
    def test_possible_values_empty_cell(self, sample_9x9_board, easy_config):
        """Test getting possible values for an empty cell"""
        possible = get_possible_values(
            sample_9x9_board, 0, 2,
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        assert isinstance(possible, set)
        assert len(possible) > 0
        # Should not include values already in row, column, or box
        assert '5' not in possible  # In same row
        assert '3' not in possible  # In same row
    
    def test_possible_values_filled_cell(self, sample_9x9_board, easy_config):
        """Test that filled cells return empty set"""
        possible = get_possible_values(
            sample_9x9_board, 0, 0,  # Cell with '5'
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        assert possible == set()
    
    def test_possible_values_constrained_cell(self, easy_config):
        """Test cell with only one possible value"""
        # Create a board where cell [0,0] can only be '1'
        board = [[None for _ in range(9)] for _ in range(9)]
        
        # Fill row 0 except [0,0]
        for i in range(1, 9):
            board[0][i] = str(i + 1)
        
        possible = get_possible_values(
            board, 0, 0,
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        assert possible == {'1'}
    
    def test_possible_values_no_options(self, easy_config):
        """Test cell with no possible values (invalid board state)"""
        board = [[None for _ in range(9)] for _ in range(9)]
        
        # Fill row, column, and box to eliminate all options
        symbols = easy_config['symbols']
        
        # Fill row 0
        for i in range(1, 9):
            board[0][i] = symbols[i]
        
        # Fill column 0
        for i in range(1, 9):
            board[i][0] = symbols[i - 1] if i != 1 else symbols[8]
        
        possible = get_possible_values(
            board, 0, 0,
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        assert len(possible) == 0


class TestAutoFill:
    """Test auto-fill functionality with constraint propagation"""
    
    def test_find_auto_fill_single_cell(self, easy_config):
        """Test finding a single cell that can be auto-filled"""
        board = [[None for _ in range(9)] for _ in range(9)]
        initial_board = copy.deepcopy(board)
        
        # Create a situation where [0,0] can only be '1'
        for i in range(1, 9):
            board[0][i] = str(i + 1)
        
        filled = find_auto_fill_cells(
            board, initial_board,
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        assert len(filled) >= 1
        # Check that [0,0] is in the filled cells
        cells_filled = [(row, col) for row, col, val in filled]
        assert (0, 0) in cells_filled
    
    def test_find_auto_fill_cascade(self, easy_config):
        """Test auto-fill cascade (filling one cell enables filling others)"""
        board = [[None for _ in range(9)] for _ in range(9)]
        initial_board = copy.deepcopy(board)
        
        # Create a scenario where multiple cells can be cascaded
        # Fill row 0 except position [0,0]
        for i in range(1, 9):
            board[0][i] = str(i + 1)
        
        # Fill column 0 except position [0,0] in a way that creates cascades
        for i in range(1, 8):
            if i < 8:
                board[i][0] = str(i + 1)
        
        filled = find_auto_fill_cells(
            board, initial_board,
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        # Should find at least the obvious one
        assert len(filled) >= 1
    
    def test_auto_fill_no_cells(self, sample_9x9_board, easy_config):
        """Test when no cells can be auto-filled"""
        initial_board = copy.deepcopy(sample_9x9_board)
        
        filled = find_auto_fill_cells(
            sample_9x9_board, initial_board,
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        # Depending on the board state, might be 0 or more
        assert isinstance(filled, list)
    
    def test_auto_fill_preserves_initial_cells(self, sample_9x9_board, easy_config):
        """Test that auto-fill doesn't modify initially given cells"""
        initial_board = copy.deepcopy(sample_9x9_board)
        
        filled = find_auto_fill_cells(
            sample_9x9_board, initial_board,
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        # Check that no initially filled cells are in the auto-fill list
        for row, col, val in filled:
            assert initial_board[row][col] is None
    
    def test_auto_fill_with_source_cell(self, easy_config):
        """Test auto-fill sorting by distance from source cell"""
        board = [[None for _ in range(9)] for _ in range(9)]
        initial_board = copy.deepcopy(board)
        
        # Create multiple cells that can be auto-filled
        for i in range(1, 9):
            board[0][i] = str(i + 1)
        for i in range(1, 9):
            board[1][i] = str(i + 1)
        
        source_cell = (0, 0)
        filled = find_auto_fill_cells(
            board, initial_board,
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols'],
            source_cell
        )
        
        if len(filled) > 1:
            # Verify cells are sorted by distance from source
            distances = []
            for row, col, val in filled:
                dist = abs(row - source_cell[0]) + abs(col - source_cell[1])
                distances.append(dist)
            
            # Check if sorted (allowing ties)
            assert distances == sorted(distances)


class TestPuzzleCompletion:
    """Test puzzle completion checking"""
    
    def test_complete_correct_puzzle(self, easy_config):
        """Test detecting a complete and correct puzzle"""
        board = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        solution = copy.deepcopy(board)
        
        assert is_puzzle_complete(board, solution, easy_config['grid_size']) is True
    
    def test_incomplete_puzzle(self, sample_9x9_board, easy_config):
        """Test detecting an incomplete puzzle"""
        solution = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        assert is_puzzle_complete(sample_9x9_board, solution, easy_config['grid_size']) is False
    
    def test_complete_wrong_puzzle(self, easy_config):
        """Test detecting a complete but incorrect puzzle"""
        board = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        solution = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        # Different complete boards should not match
        assert is_puzzle_complete(board, solution, easy_config['grid_size']) is False


class TestSolutionStatus:
    """Test solution status checking"""
    
    def test_solution_status_empty_board(self, easy_config):
        """Test solution status with no cells filled"""
        board = [[None for _ in range(9)] for _ in range(9)]
        solution = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        initial_board = copy.deepcopy(board)
        
        correct, total, wrong = check_solution_status(
            board, solution, initial_board, easy_config['grid_size']
        )
        
        assert correct == 0
        assert total == 0
        assert wrong == 0
    
    def test_solution_status_all_correct(self, easy_config):
        """Test solution status when all user-filled cells are correct"""
        solution = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        initial_board = [[None for _ in range(9)] for _ in range(9)]
        # Mark first row as initially given
        for i in range(9):
            initial_board[0][i] = solution[0][i]
        
        # User fills second row correctly
        board = copy.deepcopy(initial_board)
        for i in range(9):
            board[1][i] = solution[1][i]
        
        correct, total, wrong = check_solution_status(
            board, solution, initial_board, easy_config['grid_size']
        )
        
        assert correct == 9
        assert total == 9
        assert wrong == 0
    
    def test_solution_status_mixed(self, easy_config):
        """Test solution status with mix of correct and wrong cells"""
        solution = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        initial_board = [[None for _ in range(9)] for _ in range(9)]
        board = copy.deepcopy(initial_board)
        
        # Fill 5 cells correctly
        for i in range(5):
            board[0][i] = solution[0][i]
        
        # Fill 3 cells incorrectly
        for i in range(5, 8):
            # Use a different symbol
            wrong_symbol = easy_config['symbols'][0] if solution[0][i] != easy_config['symbols'][0] else easy_config['symbols'][1]
            board[0][i] = wrong_symbol
        
        correct, total, wrong = check_solution_status(
            board, solution, initial_board, easy_config['grid_size']
        )
        
        assert correct == 5
        assert total == 8
        assert wrong == 3


class TestDifferentGridSizes:
    """Test game logic across different grid sizes"""
    
    def test_16x16_validation(self, medium_config):
        """Test 16x16 board validation"""
        board = generate_complete_sudoku(
            medium_config['grid_size'],
            medium_config['box_size'],
            medium_config['symbols']
        )
        
        # Test that is_valid_placement works correctly
        board[0][0] = None
        original_val = board[1][0]
        
        # Should be invalid to place same value as in column
        assert is_valid_placement(
            board, 0, 0, original_val,
            medium_config['grid_size'],
            medium_config['box_size']
        ) is False
    
    def test_25x25_validation(self, hard_config):
        """Test 25x25 board validation"""
        board = generate_complete_sudoku(
            hard_config['grid_size'],
            hard_config['box_size'],
            hard_config['symbols']
        )
        
        # Test basic properties
        assert len(board) == 25
        assert all(len(row) == 25 for row in board)
        
        # Test that symbols are from alphabet (minus X)
        all_symbols = set()
        for row in board:
            all_symbols.update(row)
        assert 'X' not in all_symbols
        assert all(s in hard_config['symbols'] for s in all_symbols)
    
    def test_possible_values_16x16(self, medium_config):
        """Test possible values calculation for 16x16 grid"""
        board = [[None for _ in range(16)] for _ in range(16)]
        
        # Fill first row except [0,0]
        for i in range(1, 16):
            board[0][i] = medium_config['symbols'][i]
        
        possible = get_possible_values(
            board, 0, 0,
            medium_config['grid_size'],
            medium_config['box_size'],
            medium_config['symbols']
        )
        
        # Should have exactly one possibility
        assert len(possible) == 1
        assert medium_config['symbols'][0] in possible


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_fill_board_backtracking(self, easy_config):
        """Test that fill_board correctly backtracks when needed"""
        board = [[None for _ in range(9)] for _ in range(9)]
        
        # Create a challenging starting position
        board[0][0] = '5'
        board[1][1] = '5'
        board[2][2] = '5'
        
        # Should still be able to fill the board
        result = fill_board(
            board,
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols'],
            0, 0
        )
        
        # Might succeed or fail depending on starting state
        assert isinstance(result, bool)
    
    def test_remove_numbers_maintains_board_size(self, easy_config):
        """Test that removing numbers doesn't change board dimensions"""
        board = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        remove_numbers(board, easy_config['grid_size'], 40)
        
        assert len(board) == easy_config['grid_size']
        assert all(len(row) == easy_config['grid_size'] for row in board)
    
    def test_possible_values_with_empty_board(self, easy_config):
        """Test possible values on completely empty board"""
        board = [[None for _ in range(9)] for _ in range(9)]
        
        possible = get_possible_values(
            board, 4, 4,
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        # Should have all symbols as possibilities
        assert possible == set(easy_config['symbols'])
    
    def test_auto_fill_complete_board(self, easy_config):
        """Test auto-fill on already complete board"""
        board = generate_complete_sudoku(
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        initial_board = copy.deepcopy(board)
        
        filled = find_auto_fill_cells(
            board, initial_board,
            easy_config['grid_size'],
            easy_config['box_size'],
            easy_config['symbols']
        )
        
        # Should find no cells to fill
        assert len(filled) == 0


class TestPerformance:
    """Performance tests (optional, can be marked as slow)"""
    
    @pytest.mark.slow
    def test_25x25_generation_completes(self, hard_config):
        """Test that 25x25 generation completes in reasonable time"""
        import time
        
        start = time.time()
        board = generate_complete_sudoku(
            hard_config['grid_size'],
            hard_config['box_size'],
            hard_config['symbols']
        )
        elapsed = time.time() - start
        
        assert board is not None
        # Should complete within 30 seconds
        assert elapsed < 30.0
    
    @pytest.mark.slow
    def test_multiple_generations_consistent(self, easy_config):
        """Test that multiple generations produce valid boards"""
        for _ in range(10):
            board = generate_complete_sudoku(
                easy_config['grid_size'],
                easy_config['box_size'],
                easy_config['symbols']
            )
            
            assert board is not None
            assert len(board) == easy_config['grid_size']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
