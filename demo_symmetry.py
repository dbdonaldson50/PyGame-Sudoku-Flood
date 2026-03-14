"""
Visual Demonstration of 180° Rotational Symmetry
Author: Red Donaldson
Date: March 14, 2026

Shows side-by-side comparison of the puzzle pattern rotated 180°
to visually demonstrate the symmetry.
"""

import sys
sys.path.insert(0, 'src')

from game_logic import generate_complete_sudoku, remove_numbers
from constants import DIFFICULTY_SETTINGS


def print_board_pattern(board, grid_size, title=""):
    """Print board pattern with border"""
    if title:
        print(f"\n{title}")
    print("  " + "".join([str(i % 10) for i in range(grid_size)]))
    print("  " + "=" * grid_size)
    
    for i, row in enumerate(board):
        row_str = str(i % 10) + "|"
        for cell in row:
            row_str += "█" if cell is not None else "·"
        print(row_str)


def rotate_180(board, grid_size):
    """Create a 180° rotated version of the board pattern"""
    rotated = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    
    for i in range(grid_size):
        for j in range(grid_size):
            sym_i = grid_size - 1 - i
            sym_j = grid_size - 1 - j
            rotated[sym_i][sym_j] = board[i][j]
    
    return rotated


def demonstrate_symmetry():
    """Show visual demonstration of 180° symmetry"""
    print("="*70)
    print("  180° ROTATIONAL SYMMETRY DEMONSTRATION")
    print("="*70)
    print("\n  Legend: █ = Given digit  · = Empty cell")
    
    # Use 9x9 for clear visualization
    settings = DIFFICULTY_SETTINGS['easy']
    
    # Generate puzzle
    solution = generate_complete_sudoku(
        settings['grid_size'], 
        settings['box_size'], 
        settings['symbols']
    )
    
    initial_board = [row[:] for row in solution]
    remove_numbers(initial_board, settings['grid_size'], 40)  # Medium difficulty
    
    print("\n" + "="*70)
    print("ORIGINAL PUZZLE PATTERN")
    print("="*70)
    print_board_pattern(initial_board, settings['grid_size'])
    
    print("\n" + "="*70)
    print("SAME PUZZLE ROTATED 180°")
    print("="*70)
    rotated = rotate_180(initial_board, settings['grid_size'])
    print_board_pattern(rotated, settings['grid_size'])
    
    # Verify they match
    matches = True
    for i in range(settings['grid_size']):
        for j in range(settings['grid_size']):
            orig_filled = initial_board[i][j] is not None
            rot_filled = rotated[i][j] is not None
            if orig_filled != rot_filled:
                matches = False
                break
    
    print("\n" + "="*70)
    if matches:
        print("✅ VERIFIED: The patterns are identical!")
        print("   This confirms perfect 180° rotational symmetry.")
    else:
        print("❌ ERROR: Patterns don't match (should not happen)")
    print("="*70)
    
    print("\n📝 HOW TO VERIFY:")
    print("   1. Compare position (0,0) with (8,8) - both should be █ or both ·")
    print("   2. Compare position (0,1) with (8,7) - pattern should match")
    print("   3. Center cell (4,4) maps to itself")
    print("   4. Rotate the pattern 180° - it should look identical!")
    print()


if __name__ == "__main__":
    demonstrate_symmetry()
