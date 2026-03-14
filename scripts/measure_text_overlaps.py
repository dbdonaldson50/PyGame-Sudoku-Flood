#!/usr/bin/env python3
"""
Text Overlap Diagnostic Script
Author: Red Donaldson
Date: March 14, 2026

Measures actual Pygame text rendering widths for all UI elements to identify overlaps.
Tests all grid sizes (9x9, 16x16, 25x25) and edge cases.
"""

import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from constants import *

def measure_text_width(font, text):
    """Measure the actual rendered width of text"""
    surface = font.render(text, True, (0, 0, 0))
    return surface.get_width()

def test_remaining_numbers_spacing():
    """Test spacing for remaining numbers display"""
    print("\n" + "="*80)
    print("TESTING: Remaining Numbers Display")
    print("="*80)
    
    pygame.init()
    small_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['small'], bold=False, italic=False)
    
    # Test cases: single digit, double digit, with different symbols
    test_cases = [
        ("9x9", list('123456789'), 55),  # Fixed: increased from 32
        ("16x16", list('0123456789ABCDEF'), 55),  # Fixed: increased from 30
        ("25x25", [chr(i) for i in range(ord('A'), ord('Z')) if chr(i) != 'X'], 55),  # Fixed: increased from 22
    ]
    
    for grid_name, symbols, current_spacing in test_cases:
        print(f"\n{grid_name} Grid (current spacing: {current_spacing}px)")
        print("-" * 60)
        
        # Test single digit counts
        max_width_single = 0
        for symbol in symbols[:3]:
            text = f"{symbol}:5"
            width = measure_text_width(small_font, text)
            max_width_single = max(max_width_single, width)
            print(f"  '{text}' width: {width}px")
        
        # Test double digit counts (edge case)
        max_width_double = 0
        for symbol in symbols[:3]:
            text = f"{symbol}:99"
            width = measure_text_width(small_font, text)
            max_width_double = max(max_width_double, width)
            print(f"  '{text}' width: {width}px")
        
        # Calculate safe spacing (text_width + 2px padding minimum)
        safe_spacing = max_width_double + 2
        overlap_risk = "⚠️ OVERLAP RISK!" if current_spacing < safe_spacing else "✓ OK"
        
        print(f"  Max width (double digit): {max_width_double}px")
        print(f"  Safe spacing needed: {safe_spacing}px")
        print(f"  Current spacing: {current_spacing}px {overlap_risk}")

def test_remaining_modal_spacing():
    """Test spacing for remaining digits modal"""
    print("\n" + "="*80)
    print("TESTING: Remaining Digits Modal")
    print("="*80)
    
    pygame.init()
    small_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['small'], bold=False, italic=False)
    
    test_cases = [
        ("16x16", list('0123456789ABCDEF'), 70, 37, 8),  # Fixed: increased from 58
        ("25x25", [chr(i) for i in range(ord('A'), ord('Z')) if chr(i) != 'X'], 70, 34, 10),  # Fixed: increased from 47
    ]
    
    for grid_name, symbols, h_spacing, v_spacing, items_per_row in test_cases:
        print(f"\n{grid_name} Grid Modal")
        print(f"  Layout: {items_per_row} items per row")
        print(f"  Current spacing: {h_spacing}px horizontal, {v_spacing}px vertical")
        print("-" * 60)
        
        # Test maximum width case
        max_width = 0
        for symbol in symbols:
            text = f"{symbol}: 99"  # Maximum count
            width = measure_text_width(small_font, text)
            max_width = max(max_width, width)
        
        # Get text height
        text_surface = small_font.render("A: 5", True, (0, 0, 0))
        text_height = text_surface.get_height()
        
        safe_h_spacing = max_width + 3  # 3px minimum padding
        safe_v_spacing = text_height + 2  # 2px minimum padding
        
        h_overlap = "⚠️ OVERLAP RISK!" if h_spacing < safe_h_spacing else "✓ OK"
        v_overlap = "⚠️ OVERLAP RISK!" if v_spacing < safe_v_spacing else "✓ OK"
        
        print(f"  Max text width: {max_width}px")
        print(f"  Text height: {text_height}px")
        print(f"  Safe horizontal spacing: {safe_h_spacing}px {h_overlap}")
        print(f"  Safe vertical spacing: {safe_v_spacing}px {v_overlap}")

def test_combo_indicator_overlap():
    """Test if combo indicator overlaps with Lives text"""
    print("\n" + "="*80)
    print("TESTING: Combo Indicator vs Lives Text")
    print("="*80)
    
    pygame.init()
    large_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['large'], bold=False, italic=False)
    medium_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['medium'], bold=False, italic=False)
    small_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['small'], bold=False, italic=False)
    
    # Lives text position
    lives_x = 80
    lives_y = 90
    lives_text = "Lives: 5"
    lives_width = measure_text_width(medium_font, lives_text)
    lives_height = medium_font.get_height()
    
    # Combo indicator position (fixed: moved down from 145)
    combo_x = 100
    combo_y = 160  # Fixed: increased from 145 to avoid overlap
    combo_text = "3.0x"
    combo_width = measure_text_width(large_font, combo_text)
    combo_label = "COMBO!"
    combo_label_width = measure_text_width(small_font, combo_label)
    
    print(f"\nLives Display:")
    print(f"  Position: ({lives_x}, {lives_y})")
    print(f"  Text: '{lives_text}'")
    print(f"  Width: {lives_width}px, Height: {lives_height}px")
    print(f"  Bounds: x=[{lives_x}, {lives_x + lives_width}], y=[{lives_y}, {lives_y + lives_height}]")
    
    print(f"\nCombo Indicator:")
    print(f"  Position: ({combo_x}, {combo_y})")
    print(f"  Text: '{combo_text}' + '{combo_label}'")
    print(f"  Width: {max(combo_width, combo_label_width)}px")
    print(f"  Bounds: x=[{combo_x - combo_width//2}, {combo_x + combo_width//2}], y=[{combo_y - 20}, {combo_y + 45}]")
    
    # Check for overlap
    lives_bottom = lives_y + lives_height
    combo_top = combo_y - 20  # Approximate top of combo text
    
    vertical_gap = combo_top - lives_bottom
    status = "⚠️ OVERLAP RISK!" if vertical_gap < 5 else "✓ OK"
    
    print(f"\nVertical gap: {vertical_gap}px {status}")

def test_cell_digit_fit():
    """Test if cell digits fit within cell boundaries"""
    print("\n" + "="*80)
    print("TESTING: Cell Digit Fit (Main Numbers)")
    print("="*80)
    
    pygame.init()
    
    test_cases = [
        ("9x9", 9, 720, 38),
        ("16x16", 16, 720, 26),
        ("25x25", 25, 720, 17),
    ]
    
    for grid_name, grid_size, board_size, font_size in test_cases:
        cell_size = board_size // grid_size
        cell_font = pygame.font.SysFont(FONT_NAME, font_size, bold=False, italic=False)
        
        print(f"\n{grid_name} Grid")
        print(f"  Cell size: {cell_size}px x {cell_size}px")
        print(f"  Font size: {font_size}px")
        print("-" * 60)
        
        # Test all possible symbols
        if grid_size == 9:
            symbols = list('123456789')
        elif grid_size == 16:
            symbols = list('0123456789ABCDEF')
        else:
            symbols = [chr(i) for i in range(ord('A'), ord('Z')) if chr(i) != 'X']
        
        max_width = 0
        max_height = 0
        for symbol in symbols:
            width = measure_text_width(cell_font, str(symbol))
            height = cell_font.get_height()
            max_width = max(max_width, width)
            max_height = max(max_height, height)
        
        # Check if text fits with 2px padding on each side (4px total)
        width_fit = cell_size - max_width - 4
        height_fit = cell_size - max_height - 4
        
        width_status = "⚠️ TOO WIDE!" if width_fit < 0 else "✓ OK"
        height_status = "⚠️ TOO TALL!" if height_fit < 0 else "✓ OK"
        
        print(f"  Max character width: {max_width}px")
        print(f"  Max character height: {max_height}px")
        print(f"  Horizontal clearance: {width_fit}px {width_status}")
        print(f"  Vertical clearance: {height_fit}px {height_status}")

def test_pencil_marks_fit():
    """Test if pencil marks fit within cells"""
    print("\n" + "="*80)
    print("TESTING: Pencil Marks Fit")
    print("="*80)
    
    pygame.init()
    
    test_cases = [
        ("9x9", 9, 3, 720),
        ("16x16", 16, 4, 720),
        ("25x25", 25, 5, 720),
    ]
    
    for grid_name, grid_size, box_size, board_size in test_cases:
        cell_size = board_size // grid_size
        pencil_slot_size = cell_size / box_size
        pencil_size = int(pencil_slot_size * 0.62)
        
        pencil_font = pygame.font.SysFont(FONT_NAME, pencil_size, bold=False, italic=False)
        
        print(f"\n{grid_name} Grid")
        print(f"  Cell size: {cell_size}px x {cell_size}px")
        print(f"  Pencil mark grid: {box_size}x{box_size}")
        print(f"  Slot size: {pencil_slot_size:.1f}px")
        print(f"  Pencil font size: {pencil_size}px")
        print("-" * 60)
        
        # Test worst case symbol
        test_symbol = 'W' if grid_size == 25 else 'M'
        width = measure_text_width(pencil_font, test_symbol)
        height = pencil_font.get_height()
        
        slot_width_fit = pencil_slot_size - width
        slot_height_fit = pencil_slot_size - height
        
        width_status = "⚠️ TOO WIDE!" if slot_width_fit < 0 else "✓ OK"
        height_status = "⚠️ TOO TALL!" if slot_height_fit < 0 else "✓ OK"
        
        print(f"  Test symbol '{test_symbol}': {width}px x {height}px")
        print(f"  Horizontal fit: {slot_width_fit:.1f}px {width_status}")
        print(f"  Vertical fit: {slot_height_fit:.1f}px {height_status}")

def test_button_text_fit():
    """Test if button text fits within button bounds"""
    print("\n" + "="*80)
    print("TESTING: Button Text Fit")
    print("="*80)
    
    pygame.init()
    button_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['button'], bold=False, italic=False)
    
    # Button dimensions (from sudoku_game.py)
    button_width = 72
    button_height = 35
    
    button_labels = ['New', 'Hint', 'Undo', 'Set', 'Nums']  # Fixed: shortened "Settings" and "Digits"
    
    print(f"\nButton size: {button_width}px x {button_height}px")
    print("-" * 60)
    
    for label in button_labels:
        width = measure_text_width(button_font, label)
        height = button_font.get_height()
        
        width_clearance = button_width - width - 4  # 2px padding each side
        height_clearance = button_height - height - 4
        
        width_status = "⚠️ TOO WIDE!" if width_clearance < 0 else "✓ OK"
        height_status = "⚠️ TOO TALL!" if height_clearance < 0 else "✓ OK"
        
        print(f"  '{label}': {width}px x {height}px")
        print(f"    H-clearance: {width_clearance}px {width_status}")
        print(f"    V-clearance: {height_clearance}px {height_status}")

def test_floating_points():
    """Test floating points text visibility"""
    print("\n" + "="*80)
    print("TESTING: Floating Points Display")
    print("="*80)
    
    pygame.init()
    medium_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['medium'], bold=False, italic=False)
    
    test_points = ['+5', '+10', '+15', '+50', '+100', '+250']
    
    print(f"\nFloating point text sizes:")
    print("-" * 60)
    
    max_width = 0
    for points in test_points:
        width = measure_text_width(medium_font, points)
        height = medium_font.get_height()
        max_width = max(max_width, width)
        print(f"  '{points}': {width}px x {height}px")
    
    print(f"\n  Maximum width: {max_width}px")
    print(f"  Note: Floating points should not overlap with cells or other UI")
    print(f"        Current implementation centers text at animation position")

def main():
    """Run all diagnostic tests"""
    print("\n" + "="*80)
    print("SUDOKU FLASH - TEXT OVERLAP DIAGNOSTIC")
    print("Author: Red Donaldson")
    print("Date: March 14, 2026")
    print("="*80)
    print("\nThis script measures actual Pygame text rendering to identify overlaps.")
    print("Font: Courier New (monospace)")
    
    try:
        test_remaining_numbers_spacing()
        test_remaining_modal_spacing()
        test_combo_indicator_overlap()
        test_cell_digit_fit()
        test_pencil_marks_fit()
        test_button_text_fit()
        test_floating_points()
        
        print("\n" + "="*80)
        print("DIAGNOSTIC COMPLETE")
        print("="*80)
        print("\nLegend:")
        print("  ✓ OK - No overlap risk detected")
        print("  ⚠️ OVERLAP RISK! - Spacing too tight, overlaps likely")
        print("\nReview results above to identify areas needing fixes.")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
