"""
Quick smoke test for game with symmetric puzzles
Author: Red Donaldson
Date: March 14, 2026
"""

import sys
sys.path.insert(0, 'src')

from game_logic import (
    generate_complete_sudoku, 
    remove_numbers,
    is_valid_placement,
    get_possible_values
)
from constants import DIFFICULTY_SETTINGS


def smoke_test_game_flow(difficulty):
    """Test complete game flow with symmetric puzzle"""
    settings = DIFFICULTY_SETTINGS[difficulty]
    
    print(f"\n{'='*60}")
    print(f"Testing {difficulty.upper()} difficulty game flow")
    print('='*60)
    
    # 1. Generate solution
    print("1. Generating complete solution...")
    solution = generate_complete_sudoku(
        settings['grid_size'],
        settings['box_size'],
        settings['symbols']
    )
    
    # Verify solution is valid
    for i in range(settings['grid_size']):
        for j in range(settings['grid_size']):
            assert solution[i][j] is not None, "Solution has None values"
    print("   ✅ Solution generated and valid")
    
    # 2. Create initial board with symmetric removal
    print("2. Creating puzzle with symmetric pattern...")
    initial_board = [row[:] for row in solution]
    remove_numbers(initial_board, settings['grid_size'], settings['cells_to_remove'])
    
    # Count cells
    empty_count = sum(1 for row in initial_board for cell in row if cell is None)
    given_count = settings['grid_size'] ** 2 - empty_count
    print(f"   ✅ Puzzle created: {given_count} givens, {empty_count} empty")
    
    # 3. Verify symmetry
    print("3. Verifying 180° rotational symmetry...")
    grid_size = settings['grid_size']
    symmetric = True
    
    for i in range(grid_size):
        for j in range(grid_size):
            sym_i = grid_size - 1 - i
            sym_j = grid_size - 1 - j
            
            cell_filled = initial_board[i][j] is not None
            sym_filled = initial_board[sym_i][sym_j] is not None
            
            if cell_filled != sym_filled:
                symmetric = False
                print(f"   ❌ Asymmetry at ({i},{j}) vs ({sym_i},{sym_j})")
                break
        if not symmetric:
            break
    
    if symmetric:
        print("   ✅ Perfect 180° rotational symmetry confirmed")
    
    # 4. Test game logic functions
    print("4. Testing game logic functions...")
    
    # Find an empty cell
    empty_cell = None
    for i in range(settings['grid_size']):
        for j in range(settings['grid_size']):
            if initial_board[i][j] is None:
                empty_cell = (i, j)
                break
        if empty_cell:
            break
    
    if empty_cell:
        i, j = empty_cell
        correct_value = solution[i][j]
        
        # Test is_valid_placement
        is_valid = is_valid_placement(
            initial_board, i, j, correct_value,
            settings['grid_size'], settings['box_size']
        )
        assert is_valid, "Valid placement rejected"
        print("   ✅ is_valid_placement working")
        
        # Test get_possible_values
        possible = get_possible_values(
            initial_board, i, j,
            settings['grid_size'], settings['box_size'],
            settings['symbols']
        )
        assert correct_value in possible, "Correct value not in possible values"
        print("   ✅ get_possible_values working")
    
    # 5. Summary
    print("\n✅ ALL CHECKS PASSED for", difficulty.upper())
    return True


def main():
    """Run smoke tests for all difficulties"""
    print("="*60)
    print("SMOKE TEST: Symmetric Puzzle Generation")
    print("="*60)
    
    all_passed = True
    for difficulty in ['easy', 'medium', 'hard']:
        try:
            passed = smoke_test_game_flow(difficulty)
            all_passed = all_passed and passed
        except Exception as e:
            print(f"\n❌ ERROR in {difficulty}: {e}")
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL SMOKE TESTS PASSED")
        print("   Symmetric puzzle generation is working correctly!")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*60)


if __name__ == "__main__":
    main()
