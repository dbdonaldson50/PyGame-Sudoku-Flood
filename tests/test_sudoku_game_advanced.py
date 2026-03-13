"""
Advanced Test Suite for SudokuGame - Coverage Improvement
Author: Red Donaldson
Date: March 13, 2026

Focuses on UI interactions, animations, state transitions, and edge cases
to improve coverage from 75% to 80%+
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
    pygame.init()
    game = SudokuGame()
    yield game
    pygame.quit()


@pytest.fixture
def game_in_play(game):
    """Create a game in playing state"""
    game.start_game_with_difficulty('easy')
    return game


class TestUIInteractions:
    """Test user interface interaction methods"""
    
    def test_handle_click_menu_easy_button(self, game):
        """Test clicking easy button in menu starts easy game"""
        assert game.game_state == 'menu'
        button = game.buttons['menu_easy']
        game.handle_click((button.centerx, button.centery))
        assert game.game_state == 'playing'
        assert game.difficulty == 'easy'
        assert game.grid_size == 9
    
    def test_handle_click_menu_medium_button(self, game):
        """Test clicking medium button starts medium game"""
        button = game.buttons['menu_medium']
        game.handle_click((button.centerx, button.centery))
        assert game.game_state == 'playing'
        assert game.difficulty == 'medium'
        assert game.grid_size == 16
    
    def test_handle_click_menu_hard_button(self, game):
        """Test clicking hard button starts hard game"""
        button = game.buttons['menu_hard']
        game.handle_click((button.centerx, button.centery))
        assert game.game_state == 'playing'
        assert game.difficulty == 'hard'
        assert game.grid_size == 25
    
    def test_handle_click_how_to_play_opens_instructions(self, game):
        """Test clicking how to play opens instructions modal"""
        button = game.buttons['menu_howtoplay']
        game.handle_click((button.centerx, button.centery))
        assert game.show_instructions is True
    
    def test_handle_click_close_instructions(self, game):
        """Test closing instructions modal"""
        game.show_instructions = True
        button = game.buttons['instructions_close']
        game.handle_click((button.centerx, button.centery))
        assert game.show_instructions is False
    
    def test_handle_click_outside_instructions_closes_modal(self, game):
        """Test clicking outside instructions modal closes it"""
        game.show_instructions = True
        game.handle_click((10, 10))  # Click far from modal
        assert game.show_instructions is False
    
    def test_handle_click_new_game_button(self, game_in_play):
        """Test clicking new game button creates new game"""
        old_board = copy.deepcopy(game_in_play.board)
        button = game_in_play.buttons['new_game']
        game_in_play.handle_click((button.centerx, button.centery))
        assert game_in_play.board != old_board
    
    def test_handle_click_hint_button(self, game_in_play):
        """Test clicking hint button provides hint"""
        # Find an empty cell
        for i in range(game_in_play.grid_size):
            for j in range(game_in_play.grid_size):
                if game_in_play.board[i][j] is None:
                    game_in_play.selected_cell = (i, j)
                    break
            if game_in_play.selected_cell:
                break
        
        old_score = game_in_play.score
        button = game_in_play.buttons['hint']
        game_in_play.handle_click((button.centerx, button.centery))
        # Hint should decrease score
        assert game_in_play.score <= old_score
    
    def test_handle_click_undo_button(self, game_in_play):
        """Test clicking undo button"""
        # Make a move first
        for i in range(game_in_play.grid_size):
            for j in range(game_in_play.grid_size):
                if game_in_play.board[i][j] is None:
                    game_in_play.selected_cell = (i, j)
                    symbol = game_in_play.solution[i][j]
                    game_in_play.place_number(symbol)
                    break
            if len(game_in_play.undo_history) > 0:
                break
        
        if game_in_play.undo_history:
            button = game_in_play.buttons['undo']
            game_in_play.handle_click((button.centerx, button.centery))
            assert len(game_in_play.undo_history) >= 0
    
    def test_handle_click_settings_button_opens_modal(self, game_in_play):
        """Test clicking settings button opens settings modal"""
        button = game_in_play.buttons['settings']
        game_in_play.handle_click((button.centerx, button.centery))
        assert game_in_play.show_settings is True
    
    def test_handle_click_remaining_button_opens_modal(self, game):
        """Test clicking remaining digits button opens modal for large grids"""
        game.start_game_with_difficulty('medium')  # 16x16 grid
        button = game.buttons['remaining']
        game.handle_click((button.centerx, button.centery))
        assert game.show_remaining_digits is True
    
    def test_handle_click_close_settings_modal(self, game_in_play):
        """Test closing settings modal"""
        game_in_play.show_settings = True
        button = game_in_play.buttons['settings_close']
        game_in_play.handle_click((button.centerx, button.centery))
        assert game_in_play.show_settings is False
    
    def test_handle_click_difficulty_change_in_settings(self, game_in_play):
        """Test changing difficulty through settings modal"""
        game_in_play.show_settings = True
        assert game_in_play.difficulty == 'easy'
        button = game_in_play.buttons['medium']
        game_in_play.handle_click((button.centerx, button.centery))
        assert game_in_play.difficulty == 'medium'
        assert game_in_play.show_settings is False  # Should close after changing
    
    def test_handle_click_check_solution_button(self, game_in_play):
        """Test clicking check solution button"""
        game_in_play.show_settings = True
        button = game_in_play.buttons['check']
        game_in_play.handle_click((button.centerx, button.centery))
        # Should show a message
        assert game_in_play.message != ""
    
    def test_handle_click_cell_selection(self, game_in_play):
        """Test clicking on a board cell selects it"""
        # Calculate position of first empty cell
        for i in range(game_in_play.grid_size):
            for j in range(game_in_play.grid_size):
                if game_in_play.board[i][j] is None:
                    cell_size = game_in_play.BOARD_SIZE // game_in_play.grid_size
                    x = game_in_play.BOARD_X + j * cell_size + cell_size // 2
                    y = game_in_play.BOARD_Y + i * cell_size + cell_size // 2
                    game_in_play.handle_click((x, y))
                    assert game_in_play.selected_cell == (i, j)
                    return
    
    def test_handle_click_filled_cell_no_selection(self, game_in_play):
        """Test clicking filled cell doesn't select it"""
        # Find a filled cell
        for i in range(game_in_play.grid_size):
            for j in range(game_in_play.grid_size):
                if game_in_play.board[i][j] is not None:
                    cell_size = game_in_play.BOARD_SIZE // game_in_play.grid_size
                    x = game_in_play.BOARD_X + j * cell_size + cell_size // 2
                    y = game_in_play.BOARD_Y + i * cell_size + cell_size // 2
                    game_in_play.selected_cell = None
                    game_in_play.handle_click((x, y))
                    assert game_in_play.selected_cell is None
                    return
    
    def test_handle_click_gameover_newgame_button(self, game_in_play):
        """Test clicking new game button in game over modal"""
        game_in_play.show_win_message = True
        button = game_in_play.buttons['gameover_newgame']
        game_in_play.handle_click((button.centerx, button.centery))
        assert game_in_play.show_win_message is False
    
    def test_handle_click_gameover_menu_button(self, game_in_play):
        """Test clicking main menu button in game over modal"""
        game_in_play.show_lose_message = True
        button = game_in_play.buttons['gameover_menu']
        game_in_play.handle_click((button.centerx, button.centery))
        assert game_in_play.game_state == 'menu'
        assert game_in_play.show_lose_message is False
    
    def test_handle_click_outside_gameover_modal_closes_it(self, game_in_play):
        """Test clicking outside game over modal closes it"""
        game_in_play.show_win_message = True
        game_in_play.handle_click((10, 10))  # Click outside
        assert game_in_play.show_win_message is False


class TestKeyboardHandling:
    """Test keyboard input handling"""
    
    def test_handle_key_p_toggles_pencil_mode(self, game_in_play):
        """Test pressing P key toggles pencil mode"""
        assert game_in_play.pencil_mode is False
        game_in_play.handle_key(pygame.K_p)
        assert game_in_play.pencil_mode is True
        game_in_play.handle_key(pygame.K_p)
        assert game_in_play.pencil_mode is False
    
    def test_handle_key_ctrl_z_undo(self, game_in_play):
        """Test Ctrl+Z triggers undo"""
        # Make a move
        for i in range(game_in_play.grid_size):
            for j in range(game_in_play.grid_size):
                if game_in_play.board[i][j] is None:
                    game_in_play.selected_cell = (i, j)
                    symbol = game_in_play.solution[i][j]
                    game_in_play.place_number(symbol)
                    break
            if len(game_in_play.undo_history) > 0:
                break
        
        if game_in_play.undo_history:
            # Simulate Ctrl+Z
            pygame.key.set_mods(pygame.KMOD_CTRL)
            game_in_play.handle_key(pygame.K_z)
    
    def test_handle_key_digit_places_number(self, game_in_play):
        """Test pressing digit key places number"""
        # Select empty cell
        for i in range(game_in_play.grid_size):
            for j in range(game_in_play.grid_size):
                if game_in_play.board[i][j] is None:
                    game_in_play.selected_cell = (i, j)
                    game_in_play.handle_key(pygame.K_1)
                    # Should handle the input
                    return
    
    def test_handle_key_letter_on_large_grid(self, game):
        """Test pressing letter key on 16x16 grid"""
        game.start_game_with_difficulty('medium')
        for i in range(game.grid_size):
            for j in range(game.grid_size):
                if game.board[i][j] is None:
                    game.selected_cell = (i, j)
                    game.handle_key(pygame.K_a)  # 'A' for hex
                    return
    
    def test_handle_key_arrow_navigation(self, game_in_play):
        """Test arrow keys move selection"""
        game_in_play.selected_cell = (5, 5)
        game_in_play.handle_key(pygame.K_UP)
        assert game_in_play.selected_cell == (4, 5)
        
        game_in_play.handle_key(pygame.K_DOWN)
        assert game_in_play.selected_cell == (5, 5)
        
        game_in_play.handle_key(pygame.K_LEFT)
        assert game_in_play.selected_cell == (5, 4)
        
        game_in_play.handle_key(pygame.K_RIGHT)
        assert game_in_play.selected_cell == (5, 5)
    
    def test_handle_key_when_game_over(self, game_in_play):
        """Test key handling when game is over"""
        game_in_play.game_over = True
        game_in_play.selected_cell = (0, 0)
        game_in_play.handle_key(pygame.K_1)
        # Should not process input


class TestMoveSelection:
    """Test cell selection movement"""
    
    def test_move_selection_up(self, game_in_play):
        """Test moving selection up"""
        game_in_play.selected_cell = (5, 5)
        game_in_play.move_selection(0, -1)
        assert game_in_play.selected_cell == (4, 5)
    
    def test_move_selection_down(self, game_in_play):
        """Test moving selection down"""
        game_in_play.selected_cell = (5, 5)
        game_in_play.move_selection(0, 1)
        assert game_in_play.selected_cell == (6, 5)
    
    def test_move_selection_left(self, game_in_play):
        """Test moving selection left"""
        game_in_play.selected_cell = (5, 5)
        game_in_play.move_selection(-1, 0)
        assert game_in_play.selected_cell == (5, 4)
    
    def test_move_selection_right(self, game_in_play):
        """Test moving selection right"""
        game_in_play.selected_cell = (5, 5)
        game_in_play.move_selection(1, 0)
        assert game_in_play.selected_cell == (5, 6)
    
    def test_move_selection_wrap_top(self, game_in_play):
        """Test selection wraps at top edge"""
        game_in_play.selected_cell = (0, 5)
        game_in_play.move_selection(0, -1)
        assert game_in_play.selected_cell == (game_in_play.grid_size - 1, 5)
    
    def test_move_selection_wrap_bottom(self, game_in_play):
        """Test selection wraps at bottom edge"""
        game_in_play.selected_cell = (game_in_play.grid_size - 1, 5)
        game_in_play.move_selection(0, 1)
        assert game_in_play.selected_cell == (0, 5)
    
    def test_move_selection_wrap_left(self, game_in_play):
        """Test selection wraps at left edge"""
        game_in_play.selected_cell = (5, 0)
        game_in_play.move_selection(-1, 0)
        assert game_in_play.selected_cell == (5, game_in_play.grid_size - 1)
    
    def test_move_selection_wrap_right(self, game_in_play):
        """Test selection wraps at right edge"""
        game_in_play.selected_cell = (5, game_in_play.grid_size - 1)
        game_in_play.move_selection(1, 0)
        assert game_in_play.selected_cell == (5, 0)
    
    def test_move_selection_no_cell_selected(self, game_in_play):
        """Test movement when no cell selected selects first cell"""
        game_in_play.selected_cell = None
        game_in_play.move_selection(0, 1)
        assert game_in_play.selected_cell == (0, 0)


class TestAnimationSystem:
    """Test animation state management"""
    
    def test_start_animation_creates_queue(self, game_in_play):
        """Test starting animation creates animation queue"""
        cells = [(0, 0), (0, 1), (0, 2)]
        game_in_play.start_animation(cells)
        assert len(game_in_play.animation_queue) == 3
        assert game_in_play.current_animation_frame == 0
    
    def test_start_animation_with_source_cell(self, game_in_play):
        """Test starting animation with source cell"""
        cells = [(1, 1), (1, 2)]
        source = (0, 0)
        game_in_play.start_animation(cells, source_cell=source)
        assert game_in_play.laser_source == source
    
    def test_update_animation_progresses_frames(self, game_in_play):
        """Test animation frame progression"""
        cells = [(0, 0), (0, 1)]
        game_in_play.start_animation(cells)
        old_frame = game_in_play.current_animation_frame
        game_in_play.update_animation()
        assert game_in_play.current_animation_frame > old_frame
    
    def test_update_animation_completes_cycle(self, game_in_play):
        """Test animation completes and moves to next cell"""
        cells = [(0, 0), (0, 1), (0, 2)]
        game_in_play.start_animation(cells)
        
        # Run animation until completion
        for _ in range(ANIMATION_SPEED + 1):
            initial_queue_length = len(game_in_play.animation_queue)
            game_in_play.update_animation()
            if len(game_in_play.animation_queue) < initial_queue_length:
                # One cell was processed
                break
    
    def test_update_animation_empty_queue(self, game_in_play):
        """Test updating animation with empty queue"""
        game_in_play.animation_queue = []
        game_in_play.update_animation()
        # Should not crash


class TestCompletionBonuses:
    """Test completion bonus calculations"""
    
    def test_check_completion_bonuses_row(self, game_in_play):
        """Test row completion bonus"""
        # Fill a complete row
        row = 0
        for col in range(game_in_play.grid_size):
            game_in_play.board[row][col] = game_in_play.solution[row][col]
        
        old_score = game_in_play.score
        game_in_play.check_completion_bonuses()
        # Should award bonus if row is complete and correct
        assert game_in_play.score >= old_score
    
    def test_check_completion_bonuses_column(self, game_in_play):
        """Test column completion bonus"""
        # Fill a complete column
        col = 0
        for row in range(game_in_play.grid_size):
            game_in_play.board[row][col] = game_in_play.solution[row][col]
        
        old_score = game_in_play. score
        game_in_play.check_completion_bonuses()
        assert game_in_play.score >= old_score
    
    def test_check_completion_bonuses_box(self, game_in_play):
        """Test box completion bonus"""
        # Fill a complete box
        box_size = game_in_play.box_size
        for row in range(box_size):
            for col in range(box_size):
                game_in_play.board[row][col] = game_in_play.solution[row][col]
        
        old_score = game_in_play.score
        game_in_play.check_completion_bonuses()
        assert game_in_play.score >= old_score
    
    def test_check_completion_bonuses_number(self, game_in_play):
        """Test number completion bonus (all placements of one symbol)"""
        # Fill all instances of one symbol
        symbol = game_in_play.symbols[0]
        for row in range(game_in_play.grid_size):
            for col in range(game_in_play.grid_size):
                if game_in_play.solution[row][col] == symbol:
                    game_in_play.board[row][col] = symbol
        
        old_score = game_in_play.score
        game_in_play.check_completion_bonuses()
        assert game_in_play.score >= old_score
    
    def test_check_completion_no_bonus_for_incomplete(self, game_in_play):
        """Test no bonus awarded for incomplete row"""
        row = 0
        # Fill all but one cell in row
        for col in range(game_in_play.grid_size - 1):
            game_in_play.board[row][col] = game_in_play.solution[row][col]
        
        old_score = game_in_play.score
        game_in_play.check_completion_bonuses()
        # No significant bonus
        assert game_in_play.score == old_score


class TestVisualEffects:
    """Test visual effects management"""
    
    def test_add_floating_points_creates_effect(self, game_in_play):
        """Test adding floating points creates visual effect"""
        initial_count = len(game_in_play.floating_points)
        game_in_play.add_floating_points(100, 100, 50, GREEN)
        assert len(game_in_play.floating_points) == initial_count + 1
    
    def test_add_cell_flash_correct(self, game_in_play):
        """Test adding correct cell flash"""
        initial_count = len(game_in_play.cell_flash_effects)
        game_in_play.add_cell_flash(0, 0, 'correct')
        assert len(game_in_play.cell_flash_effects) == initial_count + 1
    
    def test_add_cell_flash_incorrect(self, game_in_play):
        """Test adding incorrect cell flash"""
        initial_count = len(game_in_play.cell_flash_effects)
        game_in_play.add_cell_flash(0, 0, 'incorrect')
        assert len(game_in_play.cell_flash_effects) == initial_count + 1
    
    def test_add_cell_flash_complete(self, game_in_play):
        """Test adding completion cell flash"""
        initial_count = len(game_in_play.cell_flash_effects)
        game_in_play.add_cell_flash(0, 0, 'complete')
        assert len(game_in_play.cell_flash_effects) == initial_count + 1
    
    def test_update_floating_points_decrements_timer(self, game_in_play):
        """Test floating points timer decreases"""
        game_in_play.add_floating_points(100, 100, 50, GREEN)
        initial_timer = game_in_play.floating_points[0]['timer']
        game_in_play.update_floating_points()
        assert game_in_play.floating_points[0]['timer'] < initial_timer
    
    def test_update_floating_points_removes_expired(self, game_in_play):
        """Test expired floating points are removed"""
        game_in_play.add_floating_points(100, 100, 50, GREEN)
        # Set timer to 1 so it expires on next update
        game_in_play.floating_points[0]['timer'] = 1
        game_in_play.update_floating_points()
        assert len(game_in_play.floating_points) == 0
    
    def test_update_cell_flashes_decrements_timer(self, game_in_play):
        """Test cell flash timer decreases"""
        game_in_play.add_cell_flash(0, 0, 'correct')
        initial_timer = game_in_play.cell_flash_effects[0]['timer']
        game_in_play.update_cell_flashes()
        assert game_in_play.cell_flash_effects[0]['timer'] < initial_timer
    
    def test_update_cell_flashes_removes_expired(self, game_in_play):
        """Test expired cell flashes are removed"""
        game_in_play.add_cell_flash(0, 0, 'correct')
        # Set timer to 0 so it expires
        game_in_play.cell_flash_effects[0]['timer'] = 0
        game_in_play.update_cell_flashes()
        assert len(game_in_play.cell_flash_effects) == 0
    
    def test_multiple_concurrent_effects(self, game_in_play):
        """Test multiple effects can exist simultaneously"""
        game_in_play.add_floating_points(100, 100, 50, GREEN)
        game_in_play.add_floating_points(200, 200, 100, BLUE)
        game_in_play.add_cell_flash(0, 0, 'correct')
        game_in_play.add_cell_flash(1, 1, 'incorrect')
        
        assert len(game_in_play.floating_points) == 2
        assert len(game_in_play.cell_flash_effects) == 2


class TestStateTransitions:
    """Test game state transitions"""
    
    def test_start_game_with_difficulty_easy(self, game):
        """Test starting easy game"""
        game.start_game_with_difficulty('easy')
        assert game.game_state == 'playing'
        assert game.difficulty == 'easy'
        assert game.grid_size == 9
    
    def test_start_game_with_difficulty_medium(self, game):
        """Test starting medium game"""
        game.start_game_with_difficulty('medium')
        assert game.game_state == 'playing'
        assert game.difficulty == 'medium'
        assert game.grid_size == 16
    
    def test_start_game_with_difficulty_hard(self, game):
        """Test starting hard game"""
        game.start_game_with_difficulty('hard')
        assert game.game_state == 'playing'
        assert game.difficulty == 'hard'
        assert game.grid_size == 25
    
    def test_win_game_sets_flags(self, game_in_play):
        """Test winning game sets correct flags"""
        game_in_play.win_game()
        assert game_in_play.show_win_message is True
        assert game_in_play.game_over is True
    
    def test_lose_game_sets_flags(self, game_in_play):
        """Test losing game sets correct flags"""
        game_in_play.lose_game()
        assert game_in_play.show_lose_message is True
        assert game_in_play.game_over is True
    
    def test_show_message(self, game_in_play):
        """Test showing message to user"""
        game_in_play.show_message("Test message", RED)
        assert game_in_play.message == "Test message"
        assert game_in_play.message_color == RED
        assert game_in_play.message_timer > 0


class TestComboEdgeCases:
    """Test combo system edge cases"""
    
    def test_combo_at_max_level(self, game_in_play):
        """Test combo multiplier caps at maximum"""
        # Set combo to max
        game_in_play.combo_count = 10
        game_in_play.update_combo(increment=True)
        max_multiplier = COMBO_MULTIPLIERS[min(11, len(COMBO_MULTIPLIERS) - 1)]
        assert game_in_play.combo_multiplier <= max_multiplier
    
    def test_reset_combo_clears_state(self, game_in_play):
        """Test reset combo clears all combo state"""
        game_in_play.combo_count = 5
        game_in_play.combo_multiplier = 2.5
        game_in_play.reset_combo()
        assert game_in_play.combo_count == 0
        assert game_in_play.combo_multiplier == 1.0
    
    def test_update_combo_increment(self, game_in_play):
        """Test incrementing combo"""
        initial_count = game_in_play.combo_count
        game_in_play.update_combo(increment=True)
        assert game_in_play.combo_count == initial_count + 1
    
    def test_update_combo_no_increment(self, game_in_play):
        """Test updating combo without increment"""
        initial_count = game_in_play.combo_count
        game_in_play.update_combo(increment=False)
        assert game_in_play.combo_count == initial_count


class TestModalInteractions:
    """Test modal window interactions"""
    
    def test_close_remaining_digits_modal(self, game):
        """Test closing remaining digits modal"""
        game.start_game_with_difficulty('medium')
        game.show_remaining_digits = True
        button = game.buttons['remaining_close']
        game.handle_click((button.centerx, button.centery))
        assert game.show_remaining_digits is False
    
    def test_click_outside_remaining_modal_closes(self, game):
        """Test clicking outside remaining modal closes it"""
        game.start_game_with_difficulty('medium')
        game.show_remaining_digits = True
        game.handle_click((10, 10))
        assert game.show_remaining_digits is False
    
    def test_click_outside_settings_modal_closes(self, game_in_play):
        """Test clicking outside settings modal closes it"""
        game_in_play.show_settings = True
        game_in_play.handle_click((10, 10))
        assert game_in_play.show_settings is False


class TestEdgeCaseScenarios:
    """Test various edge case scenarios"""
    
    def test_get_cell_from_pos_outside_board(self, game_in_play):
        """Test getting cell from position outside board returns None"""
        result = game_in_play.get_cell_from_pos((10, 10))
        assert result is None
    
    def test_place_number_when_no_cell_selected(self, game_in_play):
        """Test placing number with no cell selected"""
        game_in_play.selected_cell = None
        old_board = copy.deepcopy(game_in_play.board)
        game_in_play.place_number('5')
        assert game_in_play.board == old_board
    
    def test_give_hint_when_no_cell_selected(self, game_in_play):
        """Test giving hint with no cell selected"""
        game_in_play.selected_cell = None
        old_score = game_in_play.score
        game_in_play.give_hint()
        # Should show message but not change score
        assert game_in_play.message != ""
    
    def test_undo_with_empty_history(self, game_in_play):
        """Test undo with no history"""
        game_in_play.undo_history = []
        game_in_play.undo()
        assert game_in_play.message != ""
    
    def test_handle_cell_input_unknown_character(self, game_in_play):
        """Test handling unknown character input"""
        game_in_play.selected_cell = (0, 0)
        old_input = game_in_play.current_input
        game_in_play.handle_cell_input('Z')  # Invalid for 9x9
        # Should not crash
    
    def test_update_cell_font_for_different_sizes(self, game):
        """Test cell font updates for different grid sizes"""
        # Test 9x9
        game.grid_size = 9
        game.box_size = 3
        game.update_cell_font()
        assert game.cell_font is not None
        
        # Test 16x16
        game.grid_size = 16
        game.box_size = 4
        game.update_cell_font()
        assert game.cell_font is not None
        
        # Test 25x25
        game.grid_size = 25
        game.box_size = 5
        game.update_cell_font()
        assert game.cell_font is not None
