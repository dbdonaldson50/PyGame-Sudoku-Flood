"""
Verify 180° Rotational Symmetry in Puzzle Generation
Author: Red Donaldson
Date: March 14, 2026

This script verifies that the puzzle generation creates patterns with
180° rotational symmetry where given digits are placed symmetrically.
"""

import sys
sys.path.insert(0, 'src')

from game_logic import generate_complete_sudoku, remove_numbers
from constants import DIFFICULTY_SETTINGS

# Get settings for 9x9 grid (easy difficulty)
GRID_SIZE = DIFFICULTY_SETTINGS['easy']['grid_size']
BOX_SIZE = DIFFICULTY_SETTINGS['easy']['box_size']
SYMBOLS = DIFFICULTY_SETTINGS['easy']['symbols']


def visualize_pattern(board, grid_size):
    """Visualize the pattern of given digits (X = given, . = empty)"""
    print("\nPattern visualization (X = given digit, . = empty cell):")
    print("=" * (grid_size * 2 + 1))
    
    for i in range(grid_size):
        row = ""
        for j in range(grid_size):
            if board[i][j] is not None:
                row += "X "
            else:
                row += ". "
        print(row)
    
    print("=" * (grid_size * 2 + 1))


def check_180_symmetry(board, grid_size):
    """Check if the pattern has 180° rotational symmetry"""
    symmetry_violations = []
    
    for i in range(grid_size):
        for j in range(grid_size):
            # Calculate symmetric position
            sym_i = grid_size - 1 - i
            sym_j = grid_size - 1 - j
            
            # Check if pattern matches (both given or both empty)
            cell_has_value = board[i][j] is not None
            sym_has_value = board[sym_i][sym_j] is not None
            
            if cell_has_value != sym_has_value:
                symmetry_violations.append((i, j, sym_i, sym_j))
    
    return symmetry_violations


def test_symmetry_generation(difficulty_name, cells_to_remove):
    """Test puzzle generation for a specific difficulty level"""
    print(f"\n{'='*60}")
    print(f"Testing {difficulty_name} difficulty ({cells_to_remove} cells removed)")
    print('='*60)
    
    # Generate complete board
    board = generate_complete_sudoku(GRID_SIZE, BOX_SIZE, SYMBOLS)
    
    # Remove numbers to create puzzle
    remove_numbers(board, GRID_SIZE, cells_to_remove)
    
    # Count given cells
    given_count = sum(1 for row in board for cell in row if cell is not None)
    print(f"Given cells: {given_count} / {GRID_SIZE * GRID_SIZE}")
    
    # Visualize the pattern
    visualize_pattern(board, GRID_SIZE)
    
    # Check symmetry
    violations = check_180_symmetry(board, GRID_SIZE)
    
    if violations:
        print(f"\n❌ SYMMETRY FAILED: {len(violations)} violations found")
        print("First few violations:")
        for i, (r1, c1, r2, c2) in enumerate(violations[:5]):
            print(f"  Cell ({r1},{c1}) != Cell ({r2},{c2})")
    else:
        print(f"\n✅ SYMMETRY VERIFIED: Pattern has perfect 180° rotational symmetry!")
    
    return len(violations) == 0


def main():
    """Run symmetry verification tests"""
    print("180° Rotational Symmetry Verification")
    print("=" * 60)
    
    # Test different difficulty levels
    test_cases = [
        ("Easy", 30),
        ("Medium", 40),
        ("Hard", 50),
        ("Expert", 60),
    ]
    
    all_passed = True
    for difficulty, cells_to_remove in test_cases:
        passed = test_symmetry_generation(difficulty, cells_to_remove)
        all_passed = all_passed and passed
    
    print(f"\n{'='*60}")
    if all_passed:
        print("✅ ALL TESTS PASSED: Symmetric puzzle generation working correctly!")
    else:
        print("❌ SOME TESTS FAILED: Check symmetry implementation")
    print('='*60)


if __name__ == "__main__":
    main()
