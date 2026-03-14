#!/usr/bin/env python3
"""
Diagnostic tool for remaining digits modal functionality
Author: Red Donaldson
Date: March 14, 2026

This script verifies that all components of the remaining digits modal are working correctly.
"""

def check_code_integrity():
    """Check that all necessary code is present"""
    import os
    
    print("=" * 70)
    print("REMAINING DIGITS MODAL - CODE INTEGRITY CHECK")
    print("=" * 70)
    
    issues = []
    checks_passed = []
    
    # Check 1: Verify draw_control_buttons conditionally adds button
    print("\n1. Checking draw_control_buttons() in ui_renderer.py...")
    with open('src/ui_renderer.py', 'r') as f:
        content = f.read()
        if 'if game.grid_size > 9:' in content and "'remaining', 'Digits'" in content:
            checks_passed.append("✓ Remaining button is conditionally added for large grids")
        else:
            issues.append("✗ draw_control_buttons() may not be adding remaining button correctly")
    
    # Check 2: Verify button is created in create_buttons
    print("2. Checking create_buttons() in sudoku_game.py...")
    with open('src/sudoku_game.py', 'r') as f:
        content = f.read()
        if "self.buttons['remaining']" in content:
            checks_passed.append("✓ Remaining button is created in create_buttons()")
        else:
            issues.append("✗ Remaining button may not be created in create_buttons()")
    
    # Check 3: Verify handle_click handles the button
    print("3. Checking handle_click() in sudoku_game.py...")
    with open('src/sudoku_game.py', 'r') as f:
        content = f.read()
        if "elif self.buttons['remaining'].collidepoint(pos)" in content and \
           "self.show_remaining_digits = True" in content:
            checks_passed.append("✓ Button click handler sets show_remaining_digits flag")
        else:
            issues.append("✗ Button click handler may not be working correctly")
    
    # Check 4: Verify draw_remaining_numbers hides counts for large grids
    print("4. Checking draw_remaining_numbers() logic...")
    with open('src/ui_renderer.py', 'r') as f:
        content = f.read()
        if "if game.grid_size > 9 and total_remaining >= 10:" in content and \
           "return  # Don't draw anything" in content:
            checks_passed.append("✓ On-screen counts are hidden when >= 10 remaining for large grids")
        else:
            issues.append("✗ draw_remaining_numbers() may not be hiding counts correctly")
    
    # Check 5: Verify draw_remaining_digits_modal exists and is called
    print("5. Checking draw_remaining_digits_modal() rendering...")
    with open('src/ui_renderer.py', 'r') as f:
        content = f.read()
        if "def draw_remaining_digits_modal(game):" in content:
            checks_passed.append("✓ draw_remaining_digits_modal() function exists")
        else:
            issues.append("✗ draw_remaining_digits_modal() function is missing!")
        
        if "if game.show_remaining_digits:" in content and \
           "draw_remaining_digits_modal(game)" in content:
            checks_passed.append("✓ Modal is rendered when show_remaining_digits is True")
        else:
            issues.append("✗ Modal may not be called in draw_game_screen()")
    
    # Check 6: Verify modal buttons are created
    print("6. Checking modal button creation...")
    with open('src/sudoku_game.py', 'r') as f:
        content = f.read()
        if "self.buttons['remaining_modal']" in content and \
           "self.buttons['remaining_close']" in content:
            checks_passed.append("✓ Remaining modal and close button are created")
        else:
            issues.append("✗ Modal buttons may not be created")
    
    # Check 7: Verify BUTTON_ORANGE constant exists
    print("7. Checking color constants...")
    with open('src/constants.py', 'r') as f:
        content = f.read()
        if "BUTTON_ORANGE" in content:
            checks_passed.append("✓ BUTTON_ORANGE constant exists")
        else:
            issues.append("✗ BUTTON_ORANGE constant is missing")
    
    # Print results
    print("\n" + "=" * 70)
    print("CHECKS PASSED:")
    print("=" * 70)
    for check in checks_passed:
        print(check)
    
    if issues:
        print("\n" + "=" * 70)
        print("ISSUES FOUND:")
        print("=" * 70)
        for issue in issues:
            print(issue)
        print("\n⚠️ CODE INTEGRITY CHECK FAILED - Issues found!")
        return False
    else:
        print("\n" + "=" * 70)
        print("✅ ALL CHECKS PASSED - Code appears intact!")
        print("=" * 70)
        return True


def print_usage_instructions():
    """Print instructions for users"""
    print("\n" + "=" * 70)
    print("HOW TO USE THE REMAINING DIGITS MODAL")
    print("=" * 70)
    print("""
For 16x16 and 25x25 grids:

1. Start a game with Medium (16x16) or Hard (25x25) difficulty
2. Look at the bottom of the screen for control buttons
3. You should see 5 buttons: [New] [Hint] [Undo] [Settings] [Digits]
4. Click the [Digits] button to open the remaining digits modal
5. The modal shows all digits and their remaining counts
6. Click the X button or click outside the modal to close it

IMPORTANT NOTES:
- The [Digits] button ONLY appears for 16x16 and 25x25 grids
- For 9x9 grids, remaining counts are shown directly on screen
- For large grids, counts are shown on screen only when < 10 total remaining
- Otherwise, you must click the [Digits] button to see the modal

If you don't see the [Digits] button:
1. Make sure you're on Medium (16x16) or Hard (25x25) difficulty
2. Try starting a new game
3. Check that you're running the latest version of the code
""")


if __name__ == '__main__':
    success = check_code_integrity()
    print_usage_instructions()
    
    if not success:
        print("\n⚠️  Please review the issues above and fix any problems found.")
        exit(1)
    else:
        print("\nIf you're still experiencing issues:")
        print("1. Make sure you've started a NEW game after updating the code")
        print("2. Check that you're on Medium or Hard difficulty")
        print("3. Verify the button is visible at the bottom of the screen")
        print("4. Try clicking the [Digits] button to open the modal")
        exit(0)
