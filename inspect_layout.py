#!/usr/bin/env python3
"""
Visual inspection tool to verify button and text positioning
Author: Red Donaldson
Date: March 14, 2026
"""

import sys
sys.path.insert(0, '/Users/david.donaldson/Library/CloudStorage/OneDrive-Slalom/Desktop/Idea')

from src.sudoku_game import SudokuGame
import pygame

def inspect_layout(game, difficulty_name):
    """Print detailed layout information"""
    print(f"\n{'='*70}")
    print(f"LAYOUT INSPECTION: {difficulty_name} ({game.grid_size}x{game.grid_size})")
    print(f"{'='*70}")
    
    print(f"\nWindow dimensions: {game.WINDOW_WIDTH}x{game.WINDOW_HEIGHT}")
    print(f"\nBoard settings:")
    print(f"  BOARD_SIZE: {game.BOARD_SIZE}")
    print(f"  BOARD_X: {game.BOARD_X}")
    print(f"  BOARD_Y: {game.BOARD_Y}")
    print(f"  Board spans: x=[{game.BOARD_X}, {game.BOARD_X + game.BOARD_SIZE}], y=[{game.BOARD_Y}, {game.BOARD_Y + game.BOARD_SIZE}]")
    
    print(f"\nControl buttons:")
    for key in ['new_game', 'hint', 'undo', 'settings', 'remaining']:
        if key in game.buttons:
            rect = game.buttons[key]
            visible = "✅ VISIBLE" if rect.y + rect.height <= game.WINDOW_HEIGHT and rect.x + rect.width <= game.WINDOW_WIDTH else "❌ OFF-SCREEN"
            print(f"  {key:12s}: pos=({rect.x:3d}, {rect.y:3d}), size=({rect.width:2d}x{rect.height:2d}), right_edge={rect.x + rect.width:3d} {visible}")
        else:
            print(f"  {key:12s}: ❌ NOT IN buttons dict")
    
    # Check if buttons overlap or are too close to edge
    if 'remaining' in game.buttons:
        rect = game.buttons['remaining']
        if rect.x + rect.width > game.WINDOW_WIDTH:
            print(f"\n  ⚠️  WARNING: 'remaining' button extends beyond window right edge!")
            print(f"      Right edge at {rect.x + rect.width}, window width is {game.WINDOW_WIDTH}")
        if rect.y + rect.height > game.WINDOW_HEIGHT:
            print(f"\n  ⚠️  WARNING: 'remaining' button extends beyond window bottom edge!")
            print(f"      Bottom edge at {rect.y + rect.height}, window height is {game.WINDOW_HEIGHT}")
    
    print(f"\nRemaining numbers text area:")
    print(f"  Title position: (80, 135)")
    print(f"  Counts start:   (80, 155)")
    print(f"  Items per row:  {9 if game.grid_size == 9 else (8 if game.grid_size == 16 else 13)}")
    
    if game.grid_size == 25:
        rows_needed = (25 + 12) // 13  # ceil(25/13) = 2
        last_row_y = 155 + (rows_needed - 1) * 20
        print(f"  Rows needed:    {rows_needed}")
        print(f"  Last row y:     {last_row_y}")
        print(f"  Board starts:   y={game.BOARD_Y}")
        gap = game.BOARD_Y - last_row_y
        print(f"  Gap to board:   {gap} pixels")
        if gap < 5:
            print(f"  ⚠️  WARNING: Very small gap between text and board!")
    
    # Calculate how many digits are remaining
    total_remaining = 0
    for symbol in game.symbols:
        total_needed = game.grid_size
        placed = sum(1 for i in range(game.grid_size) for j in range(game.grid_size) 
                     if game.solution[i][j] == symbol and game.board[i][j] == symbol)
        total_remaining += (total_needed - placed)
    
    print(f"\nRemaining digits logic:")
    print(f"  grid_size: {game.grid_size}")
    print(f"  total_remaining: {total_remaining}")
    print(f"  Condition (grid_size > 9): {game.grid_size > 9}")
    print(f"  Condition (total_remaining >= 10): {total_remaining >= 10}")
    print(f"  Should hide text? {game.grid_size > 9 and total_remaining >= 10}")
    print(f"  Should show button? {game.grid_size > 9}")
    
    if game.grid_size > 9 and total_remaining >= 10:
        print(f"  → On-screen text: ❌ HIDDEN (correct)")
        print(f"  → Button: ✅ SHOULD BE VISIBLE")
    elif game.grid_size > 9 and total_remaining < 10:
        print(f"  → On-screen text: ✅ SHOWN (endgame)")
        print(f"  → Button: ✅ SHOULD BE VISIBLE")
    else:
        print(f"  → On-screen text: ✅ SHOWN (9x9 grid)")
        print(f"  → Button: ❌ SHOULD NOT BE VISIBLE")

def main():
    print("SUDOKU GAME LAYOUT INSPECTOR")
    print("Testing button and text positioning for all grid sizes\n")
    
    game = SudokuGame()
    
    # Test Easy (9x9)
    game.start_game_with_difficulty('easy')
    inspect_layout(game, "EASY")
    
    # Test Medium (16x16)
    game.start_game_with_difficulty('medium')
    inspect_layout(game, "MEDIUM")
    
    # Test Hard (25x25)
    game.start_game_with_difficulty('hard')
    inspect_layout(game, "HARD")
    
    pygame.quit()
    print(f"\n{'='*70}")
    print("INSPECTION COMPLETE")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
