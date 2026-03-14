#!/usr/bin/env python3
"""Test cell size and font fit to diagnose overlap issue"""

import sys
sys.path.insert(0, 'src')
import pygame
from constants import FONT_NAME

pygame.init()

# Test each grid size with updated font sizes
board_size = 720
grid_configs = [
    (9, 38, 3),   # grid_size, font_size, box_size (reduced from 40)
    (16, 26, 4),  # (reduced from 28)
    (25, 17, 5)   # (reduced from 20)
]

print("Cell Size and Font Fit Analysis")
print("=" * 60)

for grid_size, font_size, box_size in grid_configs:
    cell_size = board_size // grid_size
    
    # Create font
    font = pygame.font.SysFont(FONT_NAME, font_size, bold=False, italic=False)
    
    # Test character sizes
    test_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_width = 0
    max_height = 0
    
    for char in test_chars:
        width, height = font.size(char)
        max_width = max(max_width, width)
        max_height = max(max_height, height)
    
    # Calculate fit
    width_fit = (max_width / cell_size) * 100
    height_fit = (max_height / cell_size) * 100
    
    print(f"\n{grid_size}x{grid_size} Grid:")
    print(f"  Cell size: {cell_size}px")
    print(f"  Font size: {font_size}")
    print(f"  Max char width: {max_width}px ({width_fit:.1f}% of cell)")
    print(f"  Max char height: {max_height}px ({height_fit:.1f}% of cell)")
    
    if width_fit > 90 or height_fit > 90:
        print(f"  ⚠️  WARNING: Characters may overlap (>90% of cell)")
        recommended_size = int(font_size * 0.80)
        print(f"  💡 Recommended: Reduce font to ~{recommended_size}")
    elif width_fit > 80 or height_fit > 80:
        print(f"  ⚠️  TIGHT: Characters are using >80% of cell")
        recommended_size = int(font_size * 0.85)
        print(f"  💡 Recommended: Consider reducing to ~{recommended_size}")
    else:
        print(f"  ✅ OK: Characters fit comfortably")

pygame.quit()
