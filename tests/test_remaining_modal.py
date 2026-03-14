"""
Comprehensive tests for remaining digits modal functionality
Author: Red Donaldson
Date: March 14, 2026
"""

import pytest
import pygame
from src.sudoku_game import SudokuGame


class TestRemainingDigitsModal:
    """Test suite for remaining digits modal functionality on large grids"""
    
    def test_remaining_button_exists_for_16x16(self):
        """Test that remaining button is created for 16x16 grid"""
        game = SudokuGame()
        game.start_game_with_difficulty('medium')  # 16x16
        assert 'remaining' in game.buttons
        assert game.grid_size == 16
    
    def test_remaining_button_exists_for_25x25(self):
        """Test that remaining button is created for 25x25 grid"""
        game = SudokuGame()
        game.start_game_with_difficulty('hard')  # 25x25
        assert 'remaining' in game.buttons
        assert game.grid_size == 25
    
    def test_remaining_button_click_opens_modal_16x16(self):
        """Test clicking remaining button opens modal for 16x16"""
        game = SudokuGame()
        game.start_game_with_difficulty('medium')
        
        assert game.show_remaining_digits is False
        button = game.buttons['remaining']
        game.handle_click((button.centerx, button.centery))
        assert game.show_remaining_digits is True
    
    def test_remaining_button_click_opens_modal_25x25(self):
        """Test clicking remaining button opens modal for 25x25"""
        game = SudokuGame()
        game.start_game_with_difficulty('hard')
        
        assert game.show_remaining_digits is False
        button = game.buttons['remaining']
        game.handle_click((button.centerx, button.centery))
        assert game.show_remaining_digits is True
    
    def test_remaining_modal_close_button(self):
        """Test that clicking close button closes modal"""
        game = SudokuGame()
        game.start_game_with_difficulty('medium')
        game.show_remaining_digits = True
        
        close_button = game.buttons['remaining_close']
        game.handle_click((close_button.centerx, close_button.centery))
        assert game.show_remaining_digits is False
    
    def test_remaining_modal_click_outside_closes(self):
        """Test that clicking outside modal closes it"""
        game = SudokuGame()
        game.start_game_with_difficulty('medium')
        game.show_remaining_digits = True
        
        # Click outside modal (top left corner)
        game.handle_click((50, 50))
        assert game.show_remaining_digits is False
    
    def test_remaining_modal_buttons_exist(self):
        """Test that modal buttons are created"""
        game = SudokuGame()
        assert 'remaining_modal' in game.buttons
        assert 'remaining_close' in game.buttons
    
    def test_grid_size_determines_button_visibility(self):
        """Test that button is only for large grids (functional test would check drawing)"""
        # 9x9 grid
        game = SudokuGame()
        game.start_game_with_difficulty('easy')
        assert game.grid_size == 9
        # Button exists but shouldn't be drawn (would need UI test to verify drawing)
        assert 'remaining' in game.buttons
        
        # 16x16 grid
        game.start_game_with_difficulty('medium')
        assert game.grid_size == 16
        assert 'remaining' in game.buttons
        
        # 25x25 grid
        game.start_game_with_difficulty('hard')
        assert game.grid_size == 25
        assert 'remaining' in game.buttons
    
    def test_remaining_button_click_no_effect_on_9x9(self):
        """Test that clicking remaining button on 9x9 grid does nothing (defensive check)"""
        game = SudokuGame()
        game.start_game_with_difficulty('easy')  # 9x9
        
        assert game.grid_size == 9
        assert game.show_remaining_digits is False
        
        # Try to click button (shouldn't open modal for 9x9)
        button = game.buttons['remaining']
        game.handle_click((button.centerx, button.centery))
        # With defensive check, should not open modal for grid_size <= 9
        assert game.show_remaining_digits is False
    
    def test_modal_state_preserved_across_interactions(self):
        """Test that modal state is properly managed"""
        game = SudokuGame()
        game.start_game_with_difficulty('medium')
        
        # Open modal
        button = game.buttons['remaining']
        game.handle_click((button.centerx, button.centery))
        assert game.show_remaining_digits is True
        
        # Close by clicking outside
        game.handle_click((50, 50))
        assert game.show_remaining_digits is False
        
        # Open again
        game.handle_click((button.centerx, button.centery))
        assert game.show_remaining_digits is True
        
        # Close via close button
        close_button = game.buttons['remaining_close']
        game.handle_click((close_button.centerx, close_button.centery))
        assert game.show_remaining_digits is False
    
    def test_modal_click_inside_stays_open(self):
        """Test that clicking inside modal (not on close) keeps it open"""
        game = SudokuGame()
        game.start_game_with_difficulty('medium')
        game.show_remaining_digits = True
        
        # Click inside modal but not on close button
        modal = game.buttons['remaining_modal']
        game.handle_click((modal.centerx, modal.centery))
        # Should stay open (clicking close button would close it)
        # But clicking inside modal returns early, so it stays open
        # Actually, the logic closes on close button click OR outside click
        # Clicking inside (not on close) should stay open... let me check the code
        # From the code: if inside modal and clicking close -> closes, otherwise returns (stays open)
        assert game.show_remaining_digits is True
