#!/usr/bin/env python3
"""
Position Overlap Diagnostic Script
Author: Red Donaldson
Date: March 15, 2026

Checks if remaining numbers and combo text overlap with the board.
"""

import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from constants import *

def main():
    print("\n" + "="*80)
    print("POSITION OVERLAP DIAGNOSTIC")
    print("="*80)
    
    # Constants
    BOARD_SIZE = 720
    BOARD_X = (WINDOW_WIDTH - BOARD_SIZE) // 2  # = (800 - 720) / 2 = 40
    BOARD_Y_CONST = BOARD_Y  # = 180 from constants
    
    print(f"\nWindow: {WINDOW_WIDTH}px x {WINDOW_HEIGHT}px")
    print(f"Board: {BOARD_SIZE}px x {BOARD_SIZE}px")
    print(f"Board position: x={BOARD_X}, y={BOARD_Y_CONST}")
    print(f"Board bounds: x=[{BOARD_X}, {BOARD_X + BOARD_SIZE}], y=[{BOARD_Y_CONST}, {BOARD_Y_CONST + BOARD_SIZE}]")
    
    # Check remaining numbers position for each grid size
    print("\n" + "="*80)
    print("CHECKING: Remaining Numbers Position")
    print("="*80)
    
    # From draw_remaining_numbers, title is at y=130, counts start at y=165
    # Text height is ~25px, so counts end at y=190 for first row
    remaining_title_y = 130
    remaining_start_y = 165
    remaining_text_height = 25
    
    print(f"\nRemaining Numbers:")
    print(f"  Title position: y={remaining_title_y}")
    print(f"  Count line starts: y={remaining_start_y}")
    print(f"  Text height: {remaining_text_height}px")
    print(f"  Count line ends: y={remaining_start_y + remaining_text_height} (approximately)")
    
    for grid_name, grid_size, symbols in [("9x9", 9, 9), ("16x16", 16, 16), ("25x25", 25, 24)]:
        items_per_row = 9 if grid_size == 9 else 13
        num_rows = (symbols + items_per_row - 1) // items_per_row
        row_spacing = 26
        
        last_row_y = remaining_start_y + (num_rows - 1) * row_spacing
        last_row_end_y = last_row_y + remaining_text_height
        
        gap_to_board = BOARD_Y_CONST - last_row_end_y
        status = "✓ OK" if gap_to_board >= 5 else "⚠️ OVERLAP!"
        
        print(f"\n  {grid_name}:")
        print(f"    Items per row: {items_per_row}")
        print(f"    Number of rows: {num_rows}")
        print(f"    Last row starts at: y={last_row_y}")
        print(f"    Last row ends at: y={last_row_end_y}")
        print(f"    Board starts at: y={BOARD_Y_CONST}")
        print(f"    Gap to board: {gap_to_board}px {status}")
    
    # Check combo indicator position
    print("\n" + "="*80)
    print("CHECKING: Combo Indicator Position")
    print("="*80)
    
    pygame.init()
    large_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['large'], bold=False, italic=False)
    
    # From draw_combo_indicator, combo is at x=100, y=160
    combo_x = 100
    combo_y = 160
    
    # Measure combo text
    combo_text = "3.0x"
    text_surface = large_font.render(combo_text, True, (0, 0, 0))
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    
    # Text is centered at combo_x, combo_y
    combo_left = combo_x - text_width // 2
    combo_right = combo_x + text_width // 2
    combo_top = combo_y - text_height // 2
    combo_bottom = combo_y + text_height // 2
    
    print(f"\nCombo Indicator:")
    print(f"  Position: ({combo_x}, {combo_y}) [center]")
    print(f"  Text: '{combo_text}'")
    print(f"  Size: {text_width}px x {text_height}px")
    print(f"  Bounds: x=[{combo_left}, {combo_right}], y=[{combo_top}, {combo_bottom}]")
    print(f"  Board starts at: y={BOARD_Y_CONST}")
    
    gap_to_board = BOARD_Y_CONST - combo_bottom
    status = "✓ OK" if gap_to_board >= 5 else "⚠️ OVERLAP!"
    print(f"  Gap to board: {gap_to_board}px {status}")
    
    # Check if combo overlaps with board horizontally
    board_left = BOARD_X
    board_right = BOARD_X + BOARD_SIZE
    
    if combo_right > board_left and combo_left < board_right:
        print(f"  ⚠️ WARNING: Combo may overlap with board horizontally!")
        print(f"    Board x range: [{board_left}, {board_right}]")
        print(f"    Combo x range: [{combo_left}, {combo_right}]")
    
    pygame.quit()
    
    print("\n" + "="*80)
    print("DIAGNOSTIC COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
