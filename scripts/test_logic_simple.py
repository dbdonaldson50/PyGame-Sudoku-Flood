#!/usr/bin/env python3
"""
Simple diagnostic to check remaining digits logic
Author: Red Donaldson
Date: March 14, 2026
"""

def simulate_draw_remaining_check(grid_size, total_remaining):
    """Simulate the check in draw_remaining_numbers"""
    print(f"\nTesting: grid_size={grid_size}, total_remaining={total_remaining}")
    print(f"  Condition: grid_size > 9 = {grid_size > 9}")
    print(f"  Condition: total_remaining >= 10 = {total_remaining >= 10}")  
    print(f"  Combined: (grid_size > 9 and total_remaining >= 10) = {grid_size > 9 and total_remaining >= 10}")
    
    if grid_size > 9 and total_remaining >= 10:
        print(f"  Result: RETURN (don't draw on-screen text)")
        return True  # Should not draw
    else:
        print(f"  Result: DRAW on-screen text")
        return False  # Should draw

def simulate_button_check(grid_size):
    """Simulate the check in draw_control_buttons"""
    print(f"\nButton check for grid_size={grid_size}:")
    print(f"  Condition: grid_size > 9 = {grid_size > 9}")
    
    if grid_size > 9:
        print(f"  Result: ADD 'remaining' button to button_data")
        return True
    else:
        print(f"  Result: DON'T add 'remaining' button")
        return False

print("="*60)
print("REMAINING DIGITS LOGIC TEST")
print("="*60)

# Test 9x9 grid (should always show text, no button)
print("\n--- 9x9 Grid Tests ---")
simulate_draw_remaining_check(9, 5)
simulate_draw_remaining_check(9, 10)
simulate_draw_remaining_check(9, 40)
simulate_button_check(9)

# Test 16x16 grid 
print("\n--- 16x16 Grid Tests ---")
simulate_draw_remaining_check(16, 5)    # Near end: show text
simulate_draw_remaining_check(16, 9)    # Near end: show text
simulate_draw_remaining_check(16, 10)   # Should hide text
simulate_draw_remaining_check(16, 100)  # Early game: hide text
simulate_draw_remaining_check(16, 190)  # Start: hide text
simulate_button_check(16)

# Test 25x25 grid
print("\n--- 25x25 Grid Tests ---")
simulate_draw_remaining_check(25, 5)    # Near end: show text
simulate_draw_remaining_check(25, 9)    # Near end: show text
simulate_draw_remaining_check(25, 10)   # Should hide text
simulate_draw_remaining_check(25, 200)  # Early game: hide text
simulate_draw_remaining_check(25, 520)  # Start: hide text
simulate_button_check(25)

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print("\nExpected behavior:")
print("- 9x9: Always show text, no button")
print("- 16x16/25x25: Show button, hide text unless < 10 remaining")
print("="*60)
