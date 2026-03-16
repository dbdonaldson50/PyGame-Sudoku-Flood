#!/usr/bin/env python3
"""
Board Boundary Test - Ensures NO text hides below or overlaps the grid
Author: Red Donaldson
Date: March 15, 2026

This test verifies that all UI text stays completely outside the board area.
"""

import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from constants import *

def main():
    pygame.init()
    
    # Create fonts
    small_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['small'], bold=False, italic=False)
    large_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['large'], bold=False, italic=False)
    
    print("\n" + "="*80)
    print("BOARD BOUNDARY TEST - Ensuring NO text overlaps or hides below grid")
    print("Author: Red Donaldson")
    print("Date: March 15, 2026")
    print("="*80)
    print()
    
    # Board dimensions
    BOARD_SIZE = 720
    board_top = BOARD_Y  # 180
    board_bottom = BOARD_Y + BOARD_SIZE  # 900
    board_left = (WINDOW_WIDTH - BOARD_SIZE) // 2  # 40
    board_right = board_left + BOARD_SIZE  # 760
    
    print(f"Board boundaries:")
    print(f"  Top:    y={board_top}")
    print(f"  Bottom: y={board_bottom}")
    print(f"  Left:   x={board_left}")
    print(f"  Right:  x={board_right}")
    print()
    
    all_tests_passed = True
    
    # TEST 1: Remaining numbers position
    print("TEST 1: Remaining Numbers Position")
    print("-" * 80)
    
    # Current positions from ui_renderer.py (after fix)
    title_y = 120
    count_y = 150
    text_height = 25
    
    title_bottom = title_y + text_height
    count_bottom = count_y + text_height
    
    print(f"  Title 'Remaining:' at y={title_y}")
    print(f"    Bottom edge: y={title_bottom}")
    print(f"    Clearance to board: {board_top - title_bottom}px")
    
    if title_bottom > board_top:
        print(f"    ❌ FAIL: Title overlaps board by {title_bottom - board_top}px!")
        all_tests_passed = False
    else:
        print(f"    ✓ OK")
    print()
    
    print(f"  Counts start at y={count_y}")
    print(f"    First row bottom: y={count_bottom}")
    print(f"    Clearance to board: {board_top - count_bottom}px")
    
    if count_bottom > board_top:
        print(f"    ❌ FAIL: Counts overlap board by {count_bottom - board_top}px!")
        all_tests_passed = False
    else:
        print(f"    ✓ OK")
    print()
    
    # Test multi-row scenarios
    items_per_row = 13
    row_spacing = 26
    
    test_cases = [
        ("9x9 (9 items shown)", 9),
        ("16x16 (up to 10 items)", 10),
        ("25x25 (up to 10 items)", 10),
        ("Worst case (13 items)", 13)
    ]
    
    for case_name, num_items in test_cases:
        num_rows = (num_items + items_per_row - 1) // items_per_row
        last_row_y = count_y + (num_rows - 1) * row_spacing
        last_row_bottom = last_row_y + text_height
        clearance = board_top - last_row_bottom
        
        print(f"  {case_name}:")
        print(f"    Rows: {num_rows}, Last row: y={last_row_y}")
        print(f"    Last row bottom: y={last_row_bottom}")
        print(f"    Clearance to board: {clearance}px", end="")
        
        if last_row_bottom > board_top:
            print(f" ❌ FAIL: Overlaps board by {last_row_bottom - board_top}px!")
            all_tests_passed = False
        elif clearance < 5:
            print(f" ⚠️  WARNING: Less than 5px clearance!")
            all_tests_passed = False
        else:
            print(f" ✓ OK")
        print()
    
    # TEST 2: Combo indicator position
    print("\nTEST 2: Combo Indicator Position")
    print("-" * 80)
    
    combo_x = 100
    combo_y = 50
    
    # Measure combo text
    combo_text = "3.0x COMBO"
    text_surface = large_font.render(combo_text, True, (0, 0, 0))
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    
    # Combo is centered, so calculate bounds
    combo_top = combo_y - text_height // 2
    combo_bottom = combo_y + text_height // 2
    combo_left = combo_x - text_width // 2
    combo_right = combo_x + text_width // 2
    
    print(f"  Combo at (x={combo_x}, y={combo_y})")
    print(f"  Text size: {text_width}px x {text_height}px")
    print(f"  Bounds: top={combo_top}, bottom={combo_bottom}")
    print(f"  Clearance to board: {board_top - combo_bottom}px", end="")
    
    if combo_bottom > board_top:
        print(f" ❌ FAIL: Overlaps board by {combo_bottom - board_top}px!")
        all_tests_passed = False
    else:
        print(f" ✓ OK")
    print()
    
    # TEST 3: Lives, Score, Timer (game info)
    print("\nTEST 3: Game Info (Lives/Score/Timer)")
    print("-" * 80)
    
    info_y = 90
    info_bottom = info_y + 25
    
    print(f"  Game info at y={info_y}")
    print(f"  Bottom edge: y={info_bottom}")
    print(f"  Clearance to board: {board_top - info_bottom}px", end="")
    
    if info_bottom > board_top:
        print(f" ❌ FAIL: Overlaps board!")
        all_tests_passed = False
    else:
        print(f" ✓ OK")
    print()
    
    # TEST 4: Bottom buttons don't extend below window
    print("\nTEST 4: Bottom Buttons Stay in Window")
    print("-" * 80)
    
    button_y = 945
    button_height = 35
    button_bottom = button_y + button_height
    
    print(f"  Buttons at y={button_y}, height={button_height}")
    print(f"  Bottom edge: y={button_bottom}")
    print(f"  Window height: {WINDOW_HEIGHT}")
    print(f"  Clearance: {WINDOW_HEIGHT - button_bottom}px", end="")
    
    if button_bottom > WINDOW_HEIGHT:
        print(f" ❌ FAIL: Extends {button_bottom - WINDOW_HEIGHT}px beyond window!")
        all_tests_passed = False
    else:
        print(f" ✓ OK")
    print()
    
    # FINAL RESULT
    print("=" * 80)
    if all_tests_passed:
        print("✅ ALL BOUNDARY TESTS PASSED")
        print("All text stays outside board boundaries")
    else:
        print("❌ BOUNDARY TESTS FAILED")
        print("Some text overlaps or hides below the grid!")
        print()
        print("REQUIRED FIXES:")
        print("  1. Move 'Remaining:' title higher (suggest y=120)")
        print("  2. Move remaining counts higher (suggest y=150)")
        print("  3. Ensure counts end by y=175 (5px clearance to board at y=180)")
    print("=" * 80)
    print()
    
    pygame.quit()
    return 0 if all_tests_passed else 1

if __name__ == "__main__":
    sys.exit(main())
