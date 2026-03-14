#!/usr/bin/env python3
"""
Diagnostic script to test large grid button rendering
Author: Red Donaldson
Date: March 14, 2026
"""

import pygame
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import with proper module path
import constants
from game_logic import GameLogic
from ui_renderer import draw_control_buttons

# Need to import SudokuGame after fixing path
import importlib
spec = importlib.util.spec_from_file_location("sudoku_game", "src/sudoku_game.py")
sudoku_game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sudoku_game)
SudokuGame = sudoku_game.SudokuGame

def test_large_grid_buttons():
    """Test button rendering for 16x16 and 25x25 grids"""
    pygame.init()
    
    for grid_size in [16, 25]:
        print(f"\n{'='*60}")
        print(f"Testing {grid_size}x{grid_size} Grid")
        print(f"{'='*60}")
        
        # Create game with specified grid size
        game = SudokuGame()
        game.grid_size = grid_size
        
        print(f"✓ Game created with grid_size: {game.grid_size}")
        print(f"✓ Condition 'game.grid_size > 9' evaluates to: {game.grid_size > 9}")
        
        # Check if buttons dictionary has 'remaining' key
        if 'remaining' in game.buttons:
            print(f"✓ 'remaining' button exists in game.buttons")
            rect = game.buttons['remaining']
            print(f"  Position: ({rect.x}, {rect.y})")
            print(f"  Size: {rect.width}x{rect.height}")
            
            # Check if button is within window bounds
            if rect.x >= 0 and rect.x + rect.width <= game.WINDOW_WIDTH:
                print(f"✓ Button is within horizontal window bounds (0-{game.WINDOW_WIDTH})")
            else:
                print(f"✗ Button is OFF-SCREEN! x={rect.x}, right edge={rect.x + rect.width}")
        else:
            print(f"✗ 'remaining' button NOT found in game.buttons")
        
        # Test the draw_control_buttons logic
        print(f"\nTesting draw_control_buttons logic:")
        print(f"  Condition check: game.grid_size > 9 = {game.grid_size > 9}")
        
        # Manually simulate what draw_control_buttons does
        button_data = [
            ('new_game', 'New', None, None),
            ('hint', 'Hint', None, None),
            ('undo', 'Undo', None, None),
            ('settings', 'Settings', None, None)
        ]
        
        if game.grid_size > 9:
            button_data.append(('remaining', 'Digits', None, None))
            print(f"✓ 'remaining' button WOULD be added to button_data")
        else:
            print(f"✗ 'remaining' button would NOT be added to button_data")
        
        print(f"  Total buttons in button_data: {len(button_data)}")
        print(f"  Button keys: {[key for key, _, _, _ in button_data]}")
        
        # Test remaining numbers display logic
        print(f"\nTesting draw_remaining_numbers logic:")
        print(f"  Condition: grid_size > 9 = {game.grid_size > 9}")
        
        # For the logic: if game.grid_size > 9 and total_remaining >= 10:
        #     return  # Don't draw anything
        # This means:
        # - If grid_size > 9 AND total_remaining >= 10: hide text
        # - If grid_size <= 9: always show text
        # - If grid_size > 9 AND total_remaining < 10: show text
        
        for total_remaining in [5, 10, 50, 100]:
            should_hide = game.grid_size > 9 and total_remaining >= 10
            print(f"  With total_remaining={total_remaining}: should {'HIDE' if should_hide else 'SHOW'} on-screen text")
    
    pygame.quit()

if __name__ == "__main__":
    test_large_grid_buttons()
