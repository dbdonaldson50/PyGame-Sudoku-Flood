#!/usr/bin/env python3
"""
Button Text Measurement Script
Author: Red Donaldson
Date: March 15, 2026

Measures actual text widths for all button texts to identify overflow issues.
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
    return surface.get_width(), surface.get_height()

def main():
    pygame.init()
    
    # Create fonts
    button_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['button'], bold=False, italic=False)
    small_font = pygame.font.SysFont(FONT_NAME, FONT_SIZES['small'], bold=False, italic=False)
    
    print("\n" + "="*80)
    print("BUTTON TEXT OVERFLOW DIAGNOSTIC")
    print("="*80)
    
    # Control buttons (currently 72px wide)
    print("\n--- CONTROL BUTTONS (Current width: 72px) ---")
    control_buttons = ["New", "Hint", "Undo", "Settings", "Remaining"]
    current_width = 72
    
    for text in control_buttons:
        width, height = measure_text_width(button_font, text)
        clearance = current_width - width
        status = "✓ OK" if clearance >= 10 else "⚠️ OVERFLOW!"
        print(f"  '{text}': {width}px wide (clearance: {clearance}px) {status}")
    
    # Settings modal difficulty buttons (currently 140px wide)
    print("\n--- SETTINGS MODAL DIFFICULTY BUTTONS (Current width: 140px) ---")
    diff_buttons = ["Easy (9x9)", "Med (16x16)", "Hard (25x25)"]
    current_width = 140
    
    for text in diff_buttons:
        width, height = measure_text_width(small_font, text)
        clearance = current_width - width
        status = "✓ OK" if clearance >= 10 else "⚠️ OVERFLOW!"
        print(f"  '{text}': {width}px wide (clearance: {clearance}px) {status}")
    
    # Check Solution button (currently 140px wide)
    print("\n--- CHECK SOLUTION BUTTON (Current width: 140px) ---")
    text = "Check Solution"
    width, height = measure_text_width(small_font, text)
    clearance = current_width - width
    status = "✓ OK" if clearance >= 10 else "⚠️ OVERFLOW!"
    print(f"  '{text}': {width}px wide (clearance: {clearance}px) {status}")
    
    # Recommendations
    print("\n" + "="*80)
    print("RECOMMENDATIONS:")
    print("="*80)
    
    # Calculate needed widths
    settings_width, _ = measure_text_width(button_font, "Settings")
    needed_settings = settings_width + 20  # 10px padding on each side
    
    remaining_width, _ = measure_text_width(button_font, "Remaining")
    needed_remaining = remaining_width + 20
    
    check_width, _ = measure_text_width(small_font, "Check Solution")
    needed_check = check_width + 20
    
    med_width, _ = measure_text_width(small_font, "Med (16x16)")
    needed_med = med_width + 20
    
    hard_width, _ = measure_text_width(small_font, "Hard (25x25)")
    needed_hard = hard_width + 20
    
    print(f"1. Settings button should be at least: {needed_settings}px")
    print(f"2. Remaining button should be at least: {needed_remaining}px")
    print(f"3. Check Solution button should be at least: {needed_check}px")
    print(f"4. Med (16x16) button should be at least: {needed_med}px")
    print(f"5. Hard (25x25) button should be at least: {needed_hard}px")
    
    pygame.quit()

if __name__ == "__main__":
    main()
