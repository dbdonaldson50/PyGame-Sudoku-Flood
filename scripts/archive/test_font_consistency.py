#!/usr/bin/env python3
"""Test font character width consistency"""

import sys
sys.path.insert(0, 'src')
import pygame
from constants import FONT_NAME, FONT_SIZES

pygame.init()

# Test the font we're now using
font = pygame.font.SysFont(FONT_NAME, 28, bold=False, italic=False)
print(f'Testing font: {FONT_NAME}')

# Test character widths
test_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
widths = {}
for char in test_chars:
    width = font.size(char)[0]
    widths[char] = width

unique_widths = set(widths.values())
print(f'\nCharacter width analysis:')
print(f'Unique widths: {sorted(unique_widths)}')
print(f'Min: {min(widths.values())}px, Max: {max(widths.values())}px')

if len(unique_widths) == 1:
    print(f'✅ PERFECT: All characters are exactly {list(unique_widths)[0]}px wide')
else:
    print(f'⚠️  WARNING: Characters have {len(unique_widths)} different widths')

pygame.quit()
print('\n✅ Font consistency test complete')
