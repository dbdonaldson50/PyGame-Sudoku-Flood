#!/usr/bin/env python3
"""
Comprehensive Text Overlap Test
Author: Red Donaldson
Date: March 14, 2026

Automated test to verify NO text overlaps anywhere in the game.
Tests all grid sizes and edge cases.
"""

import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from constants import *
import sudoku_game

def check_bounds_overlap(bounds1, bounds2, name1, name2):
    """Check if two rectangular bounds overlap"""
    x1_min, x1_max, y1_min, y1_max = bounds1
    x2_min, x2_max, y2_min, y2_max = bounds2
    
    # Check for overlap
    x_overlap = not (x1_max < x2_min or x2_max < x1_min)
    y_overlap = not (y1_max < y2_min or y2_max < y1_min)
    
    if x_overlap and y_overlap:
        print(f"  ❌ OVERLAP DETECTED: {name1} overlaps with {name2}")
        print(f"     {name1}: x=[{x1_min}, {x1_max}], y=[{y1_min}, {y1_max}]")
        print(f"     {name2}: x=[{x2_min}, {x2_max}], y=[{y2_min}, {y2_max}]")
        return True
    return False

def test_remaining_numbers_layout(game, grid_size):
    """Test remaining numbers display doesn't overlap"""
    print(f"\n  Testing Remaining Numbers ({grid_size}x{grid_size}):")
    
    # Simulate the layout logic from draw_remaining_numbers
    y_pos = 150  # Fixed: updated from 155
    x_pos = 80
    items_per_row = 9 if grid_size == 9 else 13
    spacing = 55
    
    # Get max count width
    count_text = game.small_font.render("A:99", True, (0, 0, 0))
    text_width = count_text.get_width()
    text_height = count_text.get_height()
    
    # For large grids (16x16, 25x25), only show when < 10 items remaining
    # This is the actual behavior in draw_remaining_numbers()
    if grid_size > 9:
        # Test worst case: 9 items (just under the 10 item threshold)
        # All will fit in one row since items_per_row=13
        symbol_count = 9
        print(f"    Note: Large grids show remaining numbers only when < 10 items remain")
    else:
        symbol_count = grid_size
    
    # Track all bounds
    bounds_list = []
    
    for idx in range(symbol_count):
        # Calculate bounds for this item
        x_min = x_pos
        x_max = x_pos + text_width
        y_min = y_pos
        y_max = y_pos + text_height
        
        bounds_list.append((x_min, x_max, y_min, y_max, f"Item_{idx}"))
        
        # Move to next position
        x_pos += spacing
        if (idx + 1) % items_per_row == 0:
            x_pos = 80
            y_pos += 26
    
    # Check for overlaps
    overlap_found = False
    for i in range(len(bounds_list)):
        for j in range(i + 1, len(bounds_list)):
            b1 = bounds_list[i][:4]
            b2 = bounds_list[j][:4]
            if check_bounds_overlap(b1, b2, bounds_list[i][4], bounds_list[j][4]):
                overlap_found = True
    
    # Check if last item goes off screen
    if bounds_list:
        last_x_max = bounds_list[-1][1]
        if last_x_max > WINDOW_WIDTH - 80:
            print(f"  ⚠️  Warning: Last item extends to x={last_x_max}, close to edge (window width: {WINDOW_WIDTH})")
    
    # Check if any row overlaps with board area
    board_top = BOARD_Y
    for bounds in bounds_list:
        if bounds[3] > board_top - 3:  # 3px minimum gap
            print(f"  ⚠️  Warning: Item {bounds[4]} at y={bounds[3]} is too close to board at y={board_top}")
            overlap_found = True
    
    if not overlap_found:
        print(f"  ✓ No overlaps detected")
    
    return not overlap_found

def test_remaining_modal_layout(game, grid_size):
    """Test remaining digits modal layout"""
    print(f"\n  Testing Remaining Digits Modal ({grid_size}x{grid_size}):")
    
    if grid_size <= 9:
        print(f"  ℹ️  Modal not used for {grid_size}x{grid_size} grids")
        return True
    
    modal_width = 500
    modal_x = (WINDOW_WIDTH - modal_width) // 2
    modal_y = (WINDOW_HEIGHT - 400) // 2
    
    y_pos = modal_y + 130
    x_start = modal_x + 30
    
    if grid_size == 16:
        items_per_row = 6  # Fixed: updated from 8
        spacing_x = 70
        spacing_y = 37
    else:  # 25
        items_per_row = 6  # Fixed: updated from 10
        spacing_x = 70
        spacing_y = 34
    
    # Get text dimensions
    test_text = game.small_font.render("A: 99", True, (0, 0, 0))
    text_width = test_text.get_width()
    text_height = test_text.get_height()
    
    # Track all bounds
    bounds_list = []
    symbol_count = 16 if grid_size == 16 else 24
    x_pos = x_start
    
    for idx in range(symbol_count):
        x_min = x_pos
        x_max = x_pos + text_width
        y_min = y_pos
        y_max = y_pos + text_height
        
        bounds_list.append((x_min, x_max, y_min, y_max, f"Symbol_{idx}"))
        
        x_pos += spacing_x
        if (idx + 1) % items_per_row == 0:
            x_pos = x_start
            y_pos += spacing_y
    
    # Check for overlaps
    overlap_found = False
    for i in range(len(bounds_list)):
        for j in range(i + 1, len(bounds_list)):
            # Skip items on different rows (they won't overlap)
            row_i = i // items_per_row
            row_j = j // items_per_row
            if abs(row_i - row_j) > 1:
                continue
            
            b1 = bounds_list[i][:4]
            b2 = bounds_list[j][:4]
            if check_bounds_overlap(b1, b2, bounds_list[i][4], bounds_list[j][4]):
                overlap_found = True
    
    # Check if items exceed modal bounds
    modal_right = modal_x + modal_width
    modal_bottom = modal_y + 400
    
    for bounds in bounds_list:
        if bounds[1] > modal_right - 30:  # 30px margin
            print(f"  ⚠️  Warning: {bounds[4]} extends beyond modal right edge")
            overlap_found = True
        if bounds[3] > modal_bottom - 60:  # 60px margin for close button
            print(f"  ⚠️  Warning: {bounds[4]} extends beyond modal bottom")
            overlap_found = True
    
    if not overlap_found:
        print(f"  ✓ No overlaps detected")
    
    return not overlap_found

def test_game_info_area(game):
    """Test Lives, Score, Timer, Combo don't overlap"""
    print(f"\n  Testing Game Info Area:")
    
    info_y = 90
    
    # Lives
    lives_text = game.medium_font.render("Lives: 5", True, (0, 0, 0))
    lives_bounds = (80, 80 + lives_text.get_width(), info_y, info_y + lives_text.get_height())
    
    # Score (centered)
    score_text = game.medium_font.render("Score: 99999", True, (0, 0, 0))
    score_width = score_text.get_width()
    score_x = (WINDOW_WIDTH - score_width) // 2
    score_bounds = (score_x, score_x + score_width, info_y, info_y + score_text.get_height())
    
    # Timer (right aligned)
    timer_text = game.medium_font.render("Time: 99:59", True, (0, 0, 0))
    timer_width = timer_text.get_width()
    timer_x = WINDOW_WIDTH - 80 - timer_width
    timer_bounds = (timer_x, timer_x + timer_width, info_y, info_y + timer_text.get_height())
    
    # Combo indicator (below Lives)
    combo_text = game.large_font.render("3.0x", True, (0, 0, 0))
    combo_label = game.small_font.render("COMBO!", True, (0, 0, 0))
    combo_x = 100
    combo_y = 160
    combo_width = max(combo_text.get_width(), combo_label.get_width())
    combo_height = combo_text.get_height() + combo_label.get_height() + 10
    combo_bounds = (combo_x - combo_width//2, combo_x + combo_width//2, 
                   combo_y - 20, combo_y + combo_height)
    
    # Check all pairs for overlap
    elements = [
        (lives_bounds, "Lives"),
        (score_bounds, "Score"),
        (timer_bounds, "Timer"),
        (combo_bounds, "Combo")
    ]
    
    overlap_found = False
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            if check_bounds_overlap(elements[i][0], elements[j][0], 
                                   elements[i][1], elements[j][1]):
                overlap_found = True
    
    if not overlap_found:
        print(f"  ✓ No overlaps detected")
    
    return not overlap_found

def test_button_layout(game):
    """Test button text fits within buttons"""
    print(f"\n  Testing Button Layout:")
    
    button_width = 72
    button_height = 35
    labels = ['New', 'Hint', 'Undo', 'Set', 'Nums']
    
    all_fit = True
    for label in labels:
        text = game.button_font.render(label, True, (0, 0, 0))
        text_width = text.get_width()
        text_height = text.get_height()
        
        # Check if text fits with 2px padding on each side
        if text_width > button_width - 4:
            print(f"  ❌ '{label}' ({text_width}px) too wide for button ({button_width}px)")
            all_fit = False
        elif text_height > button_height - 4:
            print(f"  ❌ '{label}' ({text_height}px) too tall for button ({button_height}px)")
            all_fit = False
    
    if all_fit:
        print(f"  ✓ All button text fits")
    
    return all_fit

def run_all_tests():
    """Run all overlap tests"""
    print("\n" + "="*80)
    print("SUDOKU FLASH - COMPREHENSIVE OVERLAP TEST")
    print("Author: Red Donaldson")
    print("Date: March 14, 2026")
    print("="*80)
    
    pygame.init()
    
    # Create a mock game object with just fonts
    class MockGame:
        def __init__(self):
            self.title_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['title'], bold=False, italic=False)
            self.large_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['large'], bold=False, italic=False)
            self.medium_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['medium'], bold=False, italic=False)
            self.small_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['small'], bold=False, italic=False)
            self.button_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['button'], bold=False, italic=False)
    
    game = MockGame()
    
    all_passed = True
    
    # Test each grid size
    print("\n" + "="*80)
    print("TESTING REMAINING NUMBERS LAYOUT")
    print("="*80)
    for grid_size in [9, 16, 25]:
        if not test_remaining_numbers_layout(game, grid_size):
            all_passed = False
    
    print("\n" + "="*80)
    print("TESTING REMAINING DIGITS MODAL LAYOUT")
    print("="*80)
    for grid_size in [16, 25]:
        if not test_remaining_modal_layout(game, grid_size):
            all_passed = False
    
    print("\n" + "="*80)
    print("TESTING GAME INFO AREA")
    print("="*80)
    if not test_game_info_area(game):
        all_passed = False
    
    print("\n" + "="*80)
    print("TESTING BUTTON LAYOUT")
    print("="*80)
    if not test_button_layout(game):
        all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("✅ ALL TESTS PASSED - NO OVERLAPS DETECTED")
    else:
        print("❌ SOME TESTS FAILED - OVERLAPS DETECTED")
    print("="*80)
    
    pygame.quit()
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
