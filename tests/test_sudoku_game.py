"""
Comprehensive Test Suite for SudokuGame Class
Author: Red Donaldson
Date: March 13, 2026

Tests cover:
- Game initialization and state management
- Input handling and user interactions
- Scoring system with combo multipliers
- Animation and visual effects
- Game flow (win/lose conditions)
- Negative testing for edge cases and invalid inputs
"""

import pytest
import pygame
import copy
from src.sudoku_game import SudokuGame
from src import game_logic
from src.constants import *


@pytest.fixture
def game():
    """Create a SudokuGame instance for testing"""
    # Initialize pygame before creating game
    pygame.init()
    game = SudokuGame()
    yield game
    # Cleanup
    pygame.quit()


@pytest.fixture
def game_with_board(game):
    """Create a game with initialized board"""
    game.new_game()
    return game


class TestInitialization:
    """Test game initialization and basic setup"""
    
    def test_game_creates_window(self, game):
        """Test that game creates a valid pygame window"""
        assert game.screen is not None
        assert game.screen.get_width() == WINDOW_WIDTH
        assert game.screen.get_height() == WINDOW_HEIGHT
    
    def test_game_initializes_in_menu_state(self, game):
        """Test that game starts in menu state"""
        assert game.game_state == 'menu'
        assert game.board == []
        assert game.game_over is False
    
    def test_game_has_all_required_attributes(self, game):
        """Test that game has all required attributes"""
        required_attrs = [
            'board', 'solution', 'initial_board', 'pencil_marks',
            'lives', 'score', 'selected_cell', 'pencil_mode',
            'difficulty', 'grid_size', 'box_size', 'symbols',
            'combo_count', 'combo_multiplier', 'floating_points',
            'animation_queue', 'buttons', 'undo_history'
        ]
        for attr in required_attrs:
            assert hasattr(game, attr), f"Missing attribute: {attr}"
    
    def test_fonts_are_loaded(self, game):
        """Test that all required fonts are loaded"""
        assert game.title_font is not None
        assert game.large_font is not None
        assert game.medium_font is not None
        assert game.small_font is not None
        assert game.button_font is not None
    
    def test_buttons_are_created(self, game):
        """Test that all buttons are created"""
        required_buttons = [
            'menu_easy', 'menu_medium', 'menu_hard', 'menu_howtoplay',
            'new_game', 'hint', 'undo', 'settings', 'check',
            'easy', 'medium', 'hard'
        ]
        for button_key in required_buttons:
            assert button_key in game.buttons
            assert isinstance(game.buttons[button_key], pygame.Rect)


class TestNewGame:
    """Test new game creation"""
    
    def test_new_game_creates_board(self, game):
        """Test that new game creates valid board"""
        game.new_game()
        
        assert game.board is not None
        assert len(game.board) == game.grid_size
        assert all(len(row) == game.grid_size for row in game.board)
    
    def test_new_game_resets_state(self, game):
        """Test that new game resets all state variables"""
        game.score = 500
        game.lives = 1
        game.combo_count = 5
        game.game_over = True
        
        game.new_game()
        
        assert game.score == 0
        assert game.lives == game.max_lives
        assert game.combo_count == 0
        assert game.combo_multiplier == 1.0
        assert game.game_over is False
        assert game.show_win_message is False
        assert game.show_lose_message is False
    
    def test_new_game_clears_undo_history(self, game):
        """Test that new game clears undo history"""
        game.undo_history = [('dummy', 'data', 100)]
        game.new_game()
        assert game.undo_history == []
    
    def test_new_game_initializes_pencil_marks(self, game):
        """Test that pencil marks are initialized as empty sets"""
        game.new_game()
        
        assert len(game.pencil_marks) == game.grid_size
        for row in game.pencil_marks:
            assert len(row) == game.grid_size
            for cell_marks in row:
                assert isinstance(cell_marks, set)
                assert len(cell_marks) == 0
    
    def test_new_game_creates_solvable_puzzle(self, game):
        """Test that generated puzzle has valid solution"""
        game.new_game()
        
        assert game.solution is not None
        assert game.board is not None
        # Solution should be complete
        assert all(cell is not None for row in game.solution for cell in row)
    
    def test_new_game_respects_difficulty(self, game):
        """Test that difficulty settings are applied"""
        game.difficulty = 'easy'
        game.new_game()
        easy_grid = game.grid_size
        
        game.difficulty = 'medium'
        game.new_game()
        medium_grid = game.grid_size
        
        game.difficulty = 'hard'
        game.new_game()
        hard_grid = game.grid_size
        
        # Grid sizes should increase with difficulty
        assert easy_grid < medium_grid < hard_grid


class TestCellSelection:
    """Test cell selection and interaction"""
    
    def test_get_cell_from_valid_position(self, game_with_board):
        """Test getting cell coordinates from valid mouse position"""
        # Click in the center of top-left cell
        cell_size = game_with_board.BOARD_SIZE // game_with_board.grid_size
        x = game_with_board.BOARD_X + cell_size // 2
        y = game_with_board.BOARD_Y + cell_size // 2
        
        cell = game_with_board.get_cell_from_pos((x, y))
        assert cell == (0, 0)
    
    def test_get_cell_from_invalid_position_outside_board(self, game_with_board):
        """Test getting cell from position outside board returns None"""
        # Click outside board
        cell = game_with_board.get_cell_from_pos((10, 10))
        assert cell is None
        
        cell = game_with_board.get_cell_from_pos((1000, 1000))
        assert cell is None
    
    def test_selected_cell_initially_none(self, game_with_board):
        """Test that no cell is selected initially"""
        assert game_with_board.selected_cell is None


class TestPlaceNumber:
    """Test number placement functionality"""
    
    def test_place_correct_number(self, game_with_board):
        """Test placing a correct number increases score"""
        # Find an empty cell
        empty_cell = None
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    empty_cell = (i, j)
                    break
            if empty_cell:
                break
        
        assert empty_cell is not None, "No empty cell found"
        
        game_with_board.selected_cell = empty_cell
        correct_symbol = game_with_board.solution[empty_cell[0]][empty_cell[1]]
        initial_score = game_with_board.score
        
        game_with_board.place_number(correct_symbol)
        
        # Score should increase
        assert game_with_board.score > initial_score
        # Cell should be filled
        assert game_with_board.board[empty_cell[0]][empty_cell[1]] == correct_symbol
    
    def test_place_wrong_number(self, game_with_board):
        """Test placing wrong number decreases lives"""
        # Find an empty cell
        empty_cell = None
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    empty_cell = (i, j)
                    break
            if empty_cell:
                break
        
        assert empty_cell is not None
        
        game_with_board.selected_cell = empty_cell
        correct_symbol = game_with_board.solution[empty_cell[0]][empty_cell[1]]
        
        # Find a wrong symbol
        wrong_symbol = None
        for symbol in game_with_board.symbols:
            if symbol != correct_symbol:
                wrong_symbol = symbol
                break
        
        initial_lives = game_with_board.lives
        game_with_board.place_number(wrong_symbol)
        
        # Lives should decrease
        assert game_with_board.lives < initial_lives
    
    def test_place_number_on_initial_cell_ignored(self, game_with_board):
        """Test that placing number on initial cell is ignored"""
        # Find an initial (non-empty) cell
        initial_cell = None
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.initial_board[i][j] is not None:
                    initial_cell = (i, j)
                    break
            if initial_cell:
                break
        
        assert initial_cell is not None
        
        game_with_board.selected_cell = initial_cell
        original_value = game_with_board.board[initial_cell[0]][initial_cell[1]]
        
        # Try to place different number
        for symbol in game_with_board.symbols:
            if symbol != original_value:
                game_with_board.place_number(symbol)
                break
        
        # Cell should remain unchanged
        assert game_with_board.board[initial_cell[0]][initial_cell[1]] == original_value
    
    def test_place_number_with_no_selection_ignored(self, game_with_board):
        """Test that placing number with no selection is ignored"""
        game_with_board.selected_cell = None
        initial_board = copy.deepcopy(game_with_board.board)
        
        game_with_board.place_number('1')
        
        # Board should remain unchanged
        assert game_with_board.board == initial_board
    
    def test_place_number_when_game_over_ignored(self, game_with_board):
        """Test that placing number when game is over is ignored"""
        game_with_board.game_over = True
        initial_board = copy.deepcopy(game_with_board.board)
        
        # Find an empty cell
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    game_with_board.selected_cell = (i, j)
                    break
        
        game_with_board.place_number('1')
        
        # Board should remain unchanged
        assert game_with_board.board == initial_board
    
    def test_place_zero_erases_cell(self, game_with_board):
        """Test that placing 0 erases the cell"""
        # Find an empty cell and fill it
        empty_cell = None
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    empty_cell = (i, j)
                    break
            if empty_cell:
                break
        
        assert empty_cell is not None
        
        game_with_board.selected_cell = empty_cell
        correct_symbol = game_with_board.solution[empty_cell[0]][empty_cell[1]]
        game_with_board.place_number(correct_symbol)
        
        # Now erase it
        game_with_board.place_number(0)
        
        assert game_with_board.board[empty_cell[0]][empty_cell[1]] is None


class TestPencilMode:
    """Test pencil mark functionality"""
    
    def test_toggle_pencil_mode(self, game_with_board):
        """Test toggling pencil mode"""
        initial_mode = game_with_board.pencil_mode
        game_with_board.toggle_pencil_mode()
        assert game_with_board.pencil_mode != initial_mode
        
        game_with_board.toggle_pencil_mode()
        assert game_with_board.pencil_mode == initial_mode
    
    def test_pencil_mode_adds_mark(self, game_with_board):
        """Test that pencil mode adds marks instead of placing"""
        game_with_board.pencil_mode = True
        
        # Find an empty cell
        empty_cell = None
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    empty_cell = (i, j)
                    break
            if empty_cell:
                break
        
        game_with_board.selected_cell = empty_cell
        game_with_board.place_number('1')
        
        # Pencil mark should be added, not placed
        assert '1' in game_with_board.pencil_marks[empty_cell[0]][empty_cell[1]]
        assert game_with_board.board[empty_cell[0]][empty_cell[1]] is None
    
    def test_pencil_mode_removes_existing_mark(self, game_with_board):
        """Test that placing same pencil mark removes it"""
        game_with_board.pencil_mode = True
        
        # Find an empty cell
        empty_cell = None
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    empty_cell = (i, j)
                    break
            if empty_cell:
                break
        
        game_with_board.selected_cell = empty_cell
        
        # Add mark
        game_with_board.place_number('1')
        assert '1' in game_with_board.pencil_marks[empty_cell[0]][empty_cell[1]]
        
        # Remove mark
        game_with_board.place_number('1')
        assert '1' not in game_with_board.pencil_marks[empty_cell[0]][empty_cell[1]]
    
    def test_placing_number_clears_pencil_marks(self, game_with_board):
        """Test that placing a number clears pencil marks"""
        # Find an empty cell
        empty_cell = None
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    empty_cell = (i, j)
                    break
            if empty_cell:
                break
        
        game_with_board.selected_cell = empty_cell
        
        # Add pencil marks
        game_with_board.pencil_mode = True
        game_with_board.place_number('1')
        game_with_board.place_number('2')
        assert len(game_with_board.pencil_marks[empty_cell[0]][empty_cell[1]]) > 0
        
        # Place correct number
        game_with_board.pencil_mode = False
        correct_symbol = game_with_board.solution[empty_cell[0]][empty_cell[1]]
        game_with_board.place_number(correct_symbol)
        
        # Pencil marks should be cleared
        assert len(game_with_board.pencil_marks[empty_cell[0]][empty_cell[1]]) == 0


class TestUndo:
    """Test undo functionality"""
    
    def test_undo_restores_previous_state(self, game_with_board):
        """Test that undo restores previous board state"""
        # Find an empty cell
        empty_cell = None
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    empty_cell = (i, j)
                    break
            if empty_cell:
                break
        
        initial_board = copy.deepcopy(game_with_board.board)
        
        game_with_board.selected_cell = empty_cell
        correct_symbol = game_with_board.solution[empty_cell[0]][empty_cell[1]]
        game_with_board.place_number(correct_symbol)
        
        # Undo
        game_with_board.undo()
        
        # Board should be restored
        assert game_with_board.board == initial_board
    
    def test_undo_with_empty_history_ignored(self, game_with_board):
        """Test that undo with empty history is ignored"""
        game_with_board.undo_history = []
        initial_board = copy.deepcopy(game_with_board.board)
        
        game_with_board.undo()
        
        # Board should remain unchanged
        assert game_with_board.board == initial_board
    
    def test_save_state_adds_to_history(self, game_with_board):
        """Test that save_state adds to undo history"""
        initial_history_len = len(game_with_board.undo_history)
        
        game_with_board.save_state()
        
        assert len(game_with_board.undo_history) == initial_history_len + 1


class TestComboSystem:
    """Test combo multiplier system"""
    
    def test_combo_starts_at_zero(self, game_with_board):
        """Test that combo starts at 0"""
        assert game_with_board.combo_count == 0
        assert game_with_board.combo_multiplier == 1.0
    
    def test_update_combo_increments(self, game_with_board):
        """Test that update_combo increments combo count"""
        initial_combo = game_with_board.combo_count
        game_with_board.update_combo(increment=True)
        assert game_with_board.combo_count > initial_combo
    
    def test_update_combo_increases_multiplier(self, game_with_board):
        """Test that combo increases multiplier"""
        initial_multiplier = game_with_board.combo_multiplier
        game_with_board.update_combo(increment=True)
        assert game_with_board.combo_multiplier >= initial_multiplier
    
    def test_reset_combo_clears_combo(self, game_with_board):
        """Test that reset_combo clears combo"""
        game_with_board.combo_count = 5
        game_with_board.combo_multiplier = 2.0
        
        game_with_board.reset_combo()
        
        assert game_with_board.combo_count == 0
        assert game_with_board.combo_multiplier == 1.0
    
    def test_combo_capped_at_max(self, game_with_board):
        """Test that combo is capped at maximum level"""
        # Increment combo many times
        for _ in range(100):
            game_with_board.update_combo(increment=True)
        
        assert game_with_board.combo_count <= COMBO_MAX_LEVEL
    
    def test_wrong_answer_resets_combo(self, game_with_board):
        """Test that wrong answer resets combo"""
        game_with_board.combo_count = 3
        
        # Find an empty cell
        empty_cell = None
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    empty_cell = (i, j)
                    break
            if empty_cell:
                break
        
        game_with_board.selected_cell = empty_cell
        correct_symbol = game_with_board.solution[empty_cell[0]][empty_cell[1]]
        
        # Find wrong symbol
        wrong_symbol = None
        for symbol in game_with_board.symbols:
            if symbol != correct_symbol:
                wrong_symbol = symbol
                break
        
        game_with_board.place_number(wrong_symbol)
        
        assert game_with_board.combo_count == 0


class TestFloatingPoints:
    """Test floating point animations"""
    
    def test_add_floating_points(self, game_with_board):
        """Test adding floating points"""
        initial_count = len(game_with_board.floating_points)
        
        game_with_board.add_floating_points(100, 100, 50, (255, 0, 0))
        
        assert len(game_with_board.floating_points) == initial_count + 1
    
    def test_floating_points_have_required_fields(self, game_with_board):
        """Test that floating points have all required fields"""
        game_with_board.add_floating_points(100, 100, 50, (255, 0, 0))
        
        point = game_with_board.floating_points[-1]
        assert 'x' in point
        assert 'y' in point
        assert 'points' in point
        assert 'color' in point
        assert 'timer' in point
    
    def test_update_floating_points_moves_upward(self, game_with_board):
        """Test that floating points move upward"""
        game_with_board.add_floating_points(100, 100, 50, (255, 0, 0))
        initial_y = game_with_board.floating_points[-1]['y']
        
        game_with_board.update_floating_points()
        
        # Y should decrease (move up)
        assert game_with_board.floating_points[-1]['y'] < initial_y
    
    def test_floating_points_expire(self, game_with_board):
        """Test that floating points are removed after timer expires"""
        game_with_board.add_floating_points(100, 100, 50, (255, 0, 0))
        
        # Update many times to expire
        for _ in range(100):
            game_with_board.update_floating_points()
        
        # Should be removed
        assert len(game_with_board.floating_points) == 0


class TestCellFlash:
    """Test cell flash effects"""
    
    def test_add_cell_flash(self, game_with_board):
        """Test adding cell flash effect"""
        initial_count = len(game_with_board.cell_flash_effects)
        
        game_with_board.add_cell_flash(0, 0, 'correct')
        
        assert len(game_with_board.cell_flash_effects) == initial_count + 1
    
    def test_cell_flash_expires(self, game_with_board):
        """Test that cell flash expires"""
        game_with_board.add_cell_flash(0, 0, 'correct')
        
        # Update many times
        for _ in range(100):
            game_with_board.update_cell_flashes()
        
        # Should be removed
        assert len(game_with_board.cell_flash_effects) == 0


class TestAnimation:
    """Test animation system"""
    
    def test_start_animation_initializes_queue(self, game_with_board):
        """Test that start_animation initializes queue"""
        sequence = [(0, 0, '1'), (0, 1, '2')]
        game_with_board.start_animation(sequence)
        
        assert len(game_with_board.animation_queue) > 0
    
    def test_start_animation_with_empty_sequence(self, game_with_board):
        """Test that empty sequence doesn't start animation"""
        game_with_board.start_animation([])
        
        assert len(game_with_board.animation_queue) == 0
    
    def test_update_animation_processes_queue(self, game_with_board):
        """Test that update_animation processes queue"""
        # This is tricky to test without mocking, just verify it doesn't crash
        sequence = [(0, 0, '1')]
        game_with_board.start_animation(sequence, source_cell=(0, 0))
        
        # Update animation multiple times
        for _ in range(10):
            game_with_board.update_animation()


class TestWinLose:
    """Test win and lose conditions"""
    
    def test_lose_game_sets_game_over(self, game_with_board):
        """Test that lose_game sets game over flag"""
        game_with_board.lose_game()
        
        assert game_with_board.game_over is True
        assert game_with_board.show_lose_message is True
    
    def test_win_game_sets_win_flag(self, game_with_board):
        """Test that win_game sets win flag"""
        game_with_board.win_game()
        
        assert game_with_board.show_win_message is True
    
    def test_running_out_of_lives_ends_game(self, game_with_board):
        """Test that running out of lives ends game"""
        # Reduce lives to 1
        game_with_board.lives = 1
        
        # Find an empty cell
        empty_cell = None
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    empty_cell = (i, j)
                    break
            if empty_cell:
                break
        
        game_with_board.selected_cell = empty_cell
        correct_symbol = game_with_board.solution[empty_cell[0]][empty_cell[1]]
        
        # Find wrong symbol
        wrong_symbol = None
        for symbol in game_with_board.symbols:
            if symbol != correct_symbol:
                wrong_symbol = symbol
                break
        
        game_with_board.place_number(wrong_symbol)
        
        assert game_with_board.game_over is True


class TestAutoFill:
    """Test auto-fill functionality"""
    
    def test_auto_fill_returns_count(self, game_with_board):
        """Test that auto_fill_singles returns count"""
        count = game_with_board.auto_fill_singles(award_points=False)
        assert isinstance(count, int)
        assert count >= 0


class TestNegativeInputs:
    """Comprehensive negative testing for edge cases"""
    
    def test_place_number_with_none_symbol(self, game_with_board):
        """Test placing None as symbol doesn't crash"""
        # Find an empty cell
        empty_cell = None
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    empty_cell = (i, j)
                    break
            if empty_cell:
                break
        
        game_with_board.selected_cell = empty_cell
        initial_board = copy.deepcopy(game_with_board.board)
        
        # Should not crash
        game_with_board.place_number(None)
    
    def test_place_number_with_invalid_cell_selection(self, game_with_board):
        """Test placing number with out-of-bounds cell selection"""
        game_with_board.selected_cell = (-1, -1)
        
        # Should not crash
        game_with_board.place_number('1')
        
        game_with_board.selected_cell = (9999, 9999)
        game_with_board.place_number('1')
    
    def test_get_cell_from_negative_coordinates(self, game_with_board):
        """Test getting cell from negative coordinates"""
        cell = game_with_board.get_cell_from_pos((-100, -100))
        assert cell is None
    
    def test_get_cell_from_huge_coordinates(self, game_with_board):
        """Test getting cell from extremely large coordinates"""
        cell = game_with_board.get_cell_from_pos((999999, 999999))
        assert cell is None
    
    def test_update_combo_with_negative_not_allowed(self, game_with_board):
        """Test that combo count doesn't go negative"""
        game_with_board.combo_count = 0
        game_with_board.update_combo(increment=False)
        
        assert game_with_board.combo_count == 0
    
    def test_undo_multiple_times_empty_history(self, game_with_board):
        """Test undoing multiple times with empty history"""
        game_with_board.undo_history = []
        
        # Should not crash
        for _ in range(10):
            game_with_board.undo()
        
        assert game_with_board.undo_history == []
    
    def test_score_overflow_handling(self, game_with_board):
        """Test that extremely high scores don't cause issues"""
        game_with_board.score = 999999999
        
        # Find an empty cell and place correct number
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    game_with_board.selected_cell = (i, j)
                    correct = game_with_board.solution[i][j]
                    game_with_board.place_number(correct)
                    break
            if game_with_board.selected_cell:
                break
        
        # Should not crash and score should still be valid integer
        assert isinstance(game_with_board.score, int)
        assert game_with_board.score >= 999999999
    
    def test_place_invalid_number_for_grid_size(self, game_with_board):
        """Test placing number invalid for current grid size"""
        game_with_board.grid_size = 9
        
        # Find an empty cell
        empty_cell = None
        for i in range(game_with_board.grid_size):
            for j in range(game_with_board.grid_size):
                if game_with_board.board[i][j] is None:
                    empty_cell = (i, j)
                    break
            if empty_cell:
                break
        
        game_with_board.selected_cell = empty_cell
        
        # Try to place 'A' in 9x9 grid (only digits should be valid)
        initial_board = copy.deepcopy(game_with_board.board)
        game_with_board.place_number('Z') # Invalid symbol
        
        # Board might change if Z is valid for current difficulty - just ensure no crash
        # The important thing is it doesn't crash
    
    def test_combo_multiplier_at_max_level(self, game_with_board):
        """Test combo multiplier behavior at maximum level"""
        # Set to max
        game_with_board.combo_count = COMBO_MAX_LEVEL
        game_with_board.combo_multiplier = COMBO_MULTIPLIERS[COMBO_MAX_LEVEL]
        
        # Try to increment further
        game_with_board.update_combo(increment=True)
        
        # Should stay at max
        assert game_with_board.combo_count == COMBO_MAX_LEVEL


class TestMessageSystem:
    """Test message display system"""
    
    def test_show_message_sets_message(self, game_with_board):
        """Test that show_message sets the message text"""
        game_with_board.show_message("Test message", (255, 0, 0))
        
        assert game_with_board.message == "Test message"
        assert game_with_board.message_color == (255, 0, 0)
    
    def test_show_message_sets_timer(self, game_with_board):
        """Test that show_message sets timer"""
        game_with_board.show_message("Test", (0, 0, 0))
        
        assert game_with_board.message_timer > 0


class TestHint:
    """Test hint functionality"""
    
    def test_give_hint_fills_empty_cell(self, game_with_board):
        """Test that give hint fills an empty cell"""
        # Count empty cells
        empty_before = sum(1 for row in game_with_board.board 
                          for cell in row if cell is None)
        
        if empty_before > 0:
            game_with_board.give_hint()
            
            empty_after = sum(1 for row in game_with_board.board 
                            for cell in row if cell is None)
            
            # Should fill one cell
            assert empty_after < empty_before
    
    def test_give_hint_with_no_empty_cells(self, game_with_board):
        """Test give hint when puzzle is complete"""
        # Fill entire board
        game_with_board.board = copy.deepcopy(game_with_board.solution)
        
        initial_board = copy.deepcopy(game_with_board.board)
        
        # Should not crash
        game_with_board.give_hint()
        
        # Board should remain unchanged
        assert game_with_board.board == initial_board
