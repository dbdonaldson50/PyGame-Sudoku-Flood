"""
Performance Testing Script for Sudoku Generation Optimization
Author: Red Donaldson
Date: March 13, 2026

Tests generation time for 9x9, 16x16, and 25x25 grids
"""

import time
import sys
from src.constants import DIFFICULTY_SETTINGS
from src.game_logic import generate_complete_sudoku


def test_generation_performance(difficulty_name, num_tests=3):
    """Test puzzle generation performance for a given difficulty"""
    settings = DIFFICULTY_SETTINGS[difficulty_name]
    grid_size = settings['grid_size']
    box_size = settings['box_size']
    symbols = settings['symbols']
    
    print(f"\n{'='*60}")
    print(f"Testing {difficulty_name.upper()} ({grid_size}x{grid_size} grid)")
    print(f"{'='*60}")
    
    times = []
    for test_num in range(1, num_tests + 1):
        print(f"\nTest {test_num}/{num_tests}...", end=" ", flush=True)
        
        start_time = time.time()
        board = generate_complete_sudoku(grid_size, box_size, symbols)
        end_time = time.time()
        
        elapsed = end_time - start_time
        times.append(elapsed)
        
        # Verify board is complete
        complete = all(board[i][j] is not None 
                      for i in range(grid_size) 
                      for j in range(grid_size))
        
        status = "✓" if complete else "✗"
        print(f"{status} {elapsed:.3f}s")
    
    # Calculate statistics
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"\n{'-'*60}")
    print(f"Results for {difficulty_name}:")
    print(f"  Average: {avg_time:.3f}s")
    print(f"  Min:     {min_time:.3f}s")
    print(f"  Max:     {max_time:.3f}s")
    
    # Performance assessment
    if difficulty_name == 'hard':
        if avg_time < 10:
            assessment = "✓ EXCELLENT - Target achieved!"
        elif avg_time < 15:
            assessment = "✓ GOOD - Better than baseline"
        elif avg_time < 25:
            assessment = "→ FAIR - Some improvement"
        else:
            assessment = "✗ POOR - Needs more optimization"
        print(f"  Assessment: {assessment}")
    
    return avg_time, min_time, max_time


def main():
    """Run complete performance test suite"""
    print("\n" + "="*60)
    print("SUDOKU GENERATION PERFORMANCE TEST")
    print("="*60)
    print("\nTarget for 25x25 (Hard): < 10 seconds")
    print("Baseline 25x25 estimate: ~20-30 seconds")
    
    # Increase recursion limit for 25x25
    sys.setrecursionlimit(10000)
    
    # Test all difficulty levels
    results = {}
    
    try:
        # Easy (9x9)
        avg, min_t, max_t = test_generation_performance('easy', num_tests=3)
        results['easy'] = (avg, min_t, max_t)
        
        # Medium (16x16)
        avg, min_t, max_t = test_generation_performance('medium', num_tests=3)
        results['medium'] = (avg, min_t, max_t)
        
        # Hard (25x25) - the critical one
        avg, min_t, max_t = test_generation_performance('hard', num_tests=5)
        results['hard'] = (avg, min_t, max_t)
        
    except KeyboardInterrupt:
        print("\n\n❌ Test interrupted by user")
        return
    except Exception as e:
        print(f"\n\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"\nGeneration Times (Average):")
    print(f"  Easy (9x9):     {results['easy'][0]:.3f}s")
    print(f"  Medium (16x16): {results['medium'][0]:.3f}s")
    print(f"  Hard (25x25):   {results['hard'][0]:.3f}s")
    
    # Calculate speedup estimate
    # Assuming baseline was ~25s (conservative estimate)
    baseline_25x25 = 25.0
    speedup = baseline_25x25 / results['hard'][0]
    improvement = ((baseline_25x25 - results['hard'][0]) / baseline_25x25) * 100
    
    print(f"\nEstimated Performance Improvement for 25x25:")
    print(f"  Baseline (estimated): {baseline_25x25:.1f}s")
    print(f"  Optimized:           {results['hard'][0]:.3f}s")
    print(f"  Speedup:             {speedup:.2f}x faster")
    print(f"  Improvement:         {improvement:.1f}%")
    
    if results['hard'][0] < 10:
        print(f"\n✓ SUCCESS: 25x25 generation under 10 second target!")
    elif results['hard'][0] < baseline_25x25:
        print(f"\n✓ IMPROVED: Faster than baseline, but above 10s target")
    else:
        print(f"\n✗ WARNING: Performance not improved")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
