#!/usr/bin/env python3
"""
Quick test script to verify remaining digits modal functionality for large grids.
Author: Red Donaldson
"""

import pygame
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import using module notation to avoid relative import issues
import src.sudoku_game as sudoku_module
SudokuGame = sudoku_module.SudokuGame

def test_remaining_button_16x16():
    """Test that the remaining button appears and works for 16x16 grid"""
    pygame.init()
    game = SudokuGame()
    
    # Start a 16x16 game (medium difficulty)
    game.difficulty = 'medium'
    game.game_state = 'playing'
    game.new_game()
    
    print(f"Grid size: {game.grid_size}")
    print(f"Buttons created: {list(game.buttons.keys())}")
    print(f"'remaining' button exists: {'remaining' in game.buttons}")
    print(f"'remaining' button position: {game.buttons['remaining']}")
    print(f"show_remaining_digits flag: {game.show_remaining_digits}")
    
    # Simulate clicking the remaining button
    button_rect = game.buttons['remaining']
    click_pos = button_rect.center
    print(f"\nSimulating click at: {click_pos}")
    
    # Call handle_click
    game.handle_click(click_pos)
    
    print(f"After click, show_remaining_digits flag: {game.show_remaining_digits}")
    print(f"Expected: True")
    
    if game.show_remaining_digits:
        print("\n✓ SUCCESS: Modal flag is set correctly!")
    else:
        print("\n✗ FAILURE: Modal flag was not set!")
    
    pygame.quit()

def test_remaining_button_25x25():
    """Test that the remaining button appears and works for 25x25 grid"""
    pygame.init()
    game = SudokuGame()
    
    # Start a 25x25 game (hard difficulty)
    game.difficulty = 'hard'
    game.game_state = 'playing'
    game.new_game()
    
    print(f"\nGrid size: {game.grid_size}")
    print(f"'remaining' button exists: {'remaining' in game.buttons}")
    print(f"show_remaining_digits flag: {game.show_remaining_digits}")
    
    # Simulate clicking the remaining button
    button_rect = game.buttons['remaining']
    click_pos = button_rect.center
    print(f"Simulating click at: {click_pos}")
    
    # Call handle_click
    game.handle_click(click_pos)
    
    print(f"After click, show_remaining_digits flag: {game.show_remaining_digits}")
    
    if game.show_remaining_digits:
        print("✓ SUCCESS: Modal flag is set correctly!")
    else:
        print("✗ FAILURE: Modal flag was not set!")
    
    pygame.quit()

if __name__ == '__main__':
    print("Testing Remaining Digits Modal Functionality")
    print("=" * 50)
    print("\nTest 1: 16x16 Grid")
    print("-" * 50)
    test_remaining_button_16x16()
    
    print("\n" + "=" * 50)
    print("\nTest 2: 25x25 Grid")
    print("-" * 50)
    test_remaining_button_25x25()
    
    print("\n" + "=" * 50)
    print("\nTests completed!")
