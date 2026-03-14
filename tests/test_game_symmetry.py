"""
Quick test to verify symmetry works in actual game initialization
Author: Red Donaldson
Date: March 14, 2026
"""

import sys
sys.path.insert(0, 'src')

from game_logic import generate_complete_sudoku, remove_numbers
from constants import DIFFICULTY_SETTINGS


def test_game_initialization(difficulty):
    """Test that game initialization creates symmetric puzzles"""
    settings = DIFFICULTY_SETTINGS[difficulty]
    
    print(f"\nTesting {difficulty.upper()} difficulty:")
    print(f"Grid: {settings['grid_size']}x{settings['grid_size']}")
    print(f"Cells to remove: {settings['cells_to_remove']}")
    
    # Generate puzzle
    solution = generate_complete_sudoku(
        settings['grid_size'], 
        settings['box_size'], 
        settings['symbols']
    )
    
    # Create initial board (with removed cells)
    initial_board = [row[:] for row in solution]
    remove_numbers(initial_board, settings['grid_size'], settings['cells_to_remove'])
    
    # Count givens
    given_count = sum(1 for row in initial_board for cell in row if cell is not None)
    total_cells = settings['grid_size'] ** 2
    
    print(f"Given cells: {given_count}/{total_cells}")
    print(f"Empty cells: {total_cells - given_count}")
    
    # Check symmetry
    grid_size = settings['grid_size']
    is_symmetric = True
    
    for i in range(grid_size):
        for j in range(grid_size):
            sym_i = grid_size - 1 - i
            sym_j = grid_size - 1 - j
            
            cell_filled = initial_board[i][j] is not None
            sym_filled = initial_board[sym_i][sym_j] is not None
            
            if cell_filled != sym_filled:
                is_symmetric = False
                break
        if not is_symmetric:
            break
    
    if is_symmetric:
        print("✅ Symmetry: PASS")
    else:
        print("❌ Symmetry: FAIL")
    
    return is_symmetric


def main():
    print("="*60)
    print("Game Initialization Symmetry Test")
    print("="*60)
    
    results = []
    for difficulty in ['easy', 'medium', 'hard']:
        passed = test_game_initialization(difficulty)
        results.append((difficulty, passed))
    
    print("\n" + "="*60)
    print("SUMMARY:")
    for difficulty, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {difficulty.upper()}: {status}")
    
    all_passed = all(passed for _, passed in results)
    if all_passed:
        print("\n✅ All game initializations produce symmetric puzzles!")
    else:
        print("\n❌ Some tests failed")
    print("="*60)


if __name__ == "__main__":
    main()
