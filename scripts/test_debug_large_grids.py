#!/usr/bin/env python3
"""
Test script to run game and capture debug output for large grids
Author: Red Donaldson
Date: March 14, 2026
"""

import sys
import pygame
import time

# Run the game module
if __name__ == "__main__":
    # Import as module to avoid relative import issues
    sys.path.insert(0, '/Users/david.donaldson/Library/CloudStorage/OneDrive-Slalom/Desktop/Idea')
    from src.sudoku_game import SudokuGame
    
    print("="*60)
    print("STARTING GAME TEST FOR LARGE GRIDS")
    print("="*60)
    print("\nInitializing game...")
    
    game = SudokuGame()
    
    print(f"\nInitial state:")
    print(f"  game_state: {game.game_state}")
    print(f"  grid_size: {game.grid_size}")
    print(f"  difficulty: {game.difficulty}")
    
    # Start a medium (16x16) game
    print(f"\nStarting MEDIUM (16x16) game...")
    game.start_game_with_difficulty('medium')
    
    print(f"\nAfter starting medium game:")
    print(f"  game_state: {game.game_state}")
    print(f"  grid_size: {game.grid_size}")
    print(f"  difficulty: {game.difficulty}")
    print(f"  'remaining' button in buttons? {'remaining' in game.buttons}")
    if 'remaining' in game.buttons:
        rect = game.buttons['remaining']
        print(f"  Button position: ({rect.x}, {rect.y}), size: {rect.width}x{rect.height}")
    
    # Draw one frame to trigger the debug output
    print(f"\n{'='*60}")
    print("DRAWING FIRST FRAME (should see debug output below)")
    print(f"{'='*60}\n")
    
    game.draw()
    
    print(f"\n{'='*60}")
    print("FRAME DRAWN - Check debug output above")
    print(f"{'='*60}")
    
    # Now test with hard (25x25)
    print(f"\n\nStarting HARD (25x25) game...")
    game.start_game_with_difficulty('hard')
    
    print(f"\nAfter starting hard game:")
    print(f"  game_state: {game.game_state}")
    print(f"  grid_size: {game.grid_size}")
    print(f"  difficulty: {game.difficulty}")
    
    print(f"\n{'='*60}")
    print("DRAWING SECOND FRAME (should see debug output below)")
    print(f"{'='*60}\n")
    
    game.draw()
    
    print(f"\n{'='*60}")
    print("FRAME DRAWN - Check debug output above")
    print(f"{'='*60}")
    
    pygame.quit()
    print("\n\nTest complete!")
