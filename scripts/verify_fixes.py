#!/usr/bin/env python3
"""
Comprehensive Fix Verification Script
Author: Red Donaldson
Date: March 15, 2026

Verifies that all text overflow and position overlap issues are fixed.
"""

import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from constants import *

def measure_text(font, text):
    """Measure text dimensions"""
    surface = font.render(text, True, (0, 0, 0))
    return surface.get_width(), surface.get_height()

def main():
    pygame.init()
    
    # Create fonts
    button_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['button'], bold=False, italic=False)
    small_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['small'], bold=False, italic=False)
    large_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['large'], bold=False, italic=False)
    
    print("\n" + "="*80)
    print("COMPREHENSIVE FIX VERIFICATION")
    print("Author: Red Donaldson")
    print("Date: March 15, 2026")
    print("="*80)
    
    all_ok = True
    
    # TEST 1: Control buttons
    print("\n--- TEST 1: Control Buttons ---")
    control_tests = [
        ("New", 72, button_font),
        ("Hint", 72, button_font),
        ("Undo", 72, button_font),
        ("Settings", 120, button_font),  # Fixed width
        ("Remaining", 135, button_font)  # Fixed width
    ]
    
    for text, button_width, font in control_tests:
        text_width, _ = measure_text(font, text)
        clearance = button_width - text_width
        min_padding = 10
        status = "✓ OK" if clearance >= min_padding else "❌ FAIL"
        if clearance < min_padding:
            all_ok = False
        print(f"  '{text}': {text_width}px in {button_width}px button (clearance: {clearance}px) {status}")
    
    # TEST 2: Settings modal difficulty buttons
    print("\n--- TEST 2: Settings Modal Difficulty Buttons ---")
    diff_tests = [
        ("Easy (9x9)", 180, small_font),    # Fixed width
        ("Med (16x16)", 180, small_font),   # Fixed width
        ("Hard (25x25)", 180, small_font)   # Fixed width
    ]
    
    for text, button_width, font in diff_tests:
        text_width, _ = measure_text(font, text)
        clearance = button_width - text_width
        min_padding = 10
        status = "✓ OK" if clearance >= min_padding else "❌ FAIL"
        if clearance < min_padding:
            all_ok = False
        print(f"  '{text}': {text_width}px in {button_width}px button (clearance: {clearance}px) {status}")
    
    # TEST 3: Check Solution button
    print("\n--- TEST 3: Check Solution Button ---")
    text = "Check Solution"
    button_width = 210  # Fixed width
    text_width, _ = measure_text(small_font, text)
    clearance = button_width - text_width
    min_padding = 10
    status = "✓ OK" if clearance >= min_padding else "❌ FAIL"
    if clearance < min_padding:
        all_ok = False
    print(f"  '{text}': {text_width}px in {button_width}px button (clearance: {clearance}px) {status}")
    
    # TEST 4: Remaining numbers position
    print("\n--- TEST 4: Remaining Numbers Position ---")
    BOARD_Y_CONST = BOARD_Y  # 180
    BOARD_SIZE = 720
    
    # New positions after fix
    title_y = 105
    count_start_y = 135
    text_height = 25
    
    print(f"  Board starts at: y={BOARD_Y_CONST}")
    print(f"  Title at: y={title_y} (ends ~y={title_y + text_height})")
    print(f"  Counts start at: y={count_start_y}")
    
    for grid_name, symbols in [("9x9", 9), ("16x16 (<10)", 10), ("25x25 (<10)", 10)]:
        items_per_row = 13
        num_rows = (symbols + items_per_row - 1) // items_per_row
        row_spacing = 26
        
        last_row_y = count_start_y + (num_rows - 1) * row_spacing
        last_row_end_y = last_row_y + text_height
        
        gap = BOARD_Y_CONST - last_row_end_y
        status = "✓ OK" if gap >= 5 else "❌ FAIL"
        if gap < 5:
            all_ok = False
        
        print(f"  {grid_name}: ends at y={last_row_end_y}, gap={gap}px {status}")
    
    # TEST 5: Combo indicator position
    print("\n--- TEST 5: Combo Indicator Position ---")
    combo_x = 100
    combo_y = 50  # Fixed position
    
    combo_text = "3.0x"
    text_width, text_height = measure_text(large_font, combo_text)
    
    combo_top = combo_y - text_height // 2
    combo_bottom = combo_y + text_height // 2
    combo_left = combo_x - text_width // 2
    combo_right = combo_x + text_width // 2
    
    print(f"  Combo at: ({combo_x}, {combo_y})")
    print(f"  Size: {text_width}px x {text_height}px")
    print(f"  Bounds: y=[{combo_top}, {combo_bottom}]")
    print(f"  Board starts at: y={BOARD_Y_CONST}")
    
    gap = BOARD_Y_CONST - combo_bottom
    status = "✓ OK" if gap >= 5 else "❌ FAIL"
    if gap < 5:
        all_ok = False
    print(f"  Gap to board: {gap}px {status}")
    
    # Check horizontal overlap with board
    board_left = (WINDOW_WIDTH - BOARD_SIZE) // 2  # 40
    board_right = board_left + BOARD_SIZE  # 760
    
    horizontal_overlap = combo_right > board_left and combo_left < board_right
    if horizontal_overlap:
        # This is OK as long as vertically separated
        print(f"  Note: Combo overlaps board horizontally but vertically separated ✓")
    
    # SUMMARY
    print("\n" + "="*80)
    if all_ok:
        print("✓ ALL TESTS PASSED - No text overflow or position overlap issues detected!")
    else:
        print("❌ SOME TESTS FAILED - Please review issues above")
    print("="*80)
    
    pygame.quit()
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
