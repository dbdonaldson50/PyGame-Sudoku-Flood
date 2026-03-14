#!/usr/bin/env python3
"""
Visual verification tool for remaining digits modal
Author: Red Donaldson  
Date: March 14, 2026

This script starts the game and provides visual verification prompts
"""

import pygame
import sys
import os

sys.path.insert(0, 'src')

def run_visual_verification():
    """Run the game with verification prompts"""
    print("=" * 70)
    print("REMAINING DIGITS MODAL - VISUAL VERIFICATION")
    print("=" * 70)
    print("\nThis will start the Sudoku game for visual verification.")
    print("Follow the instructions to verify the modal functionality.\n")
    
    input("Press Enter to start the game...")
    
    # Import after pygame is initialized
    from src.sudoku_game import SudokuGame
    from src.ui_renderer import render_menu, draw_game_screen
    
    pygame.init()
    game = SudokuGame()
    running = True
    
    # State tracking for verification
    verification_stage = 0
    messages = [
        "STAGE 1: You should see the main menu. Select MEDIUM or HARD difficulty.",
        "STAGE 2: Look at the bottom of the screen. Do you see 5 buttons?",
        "STAGE 3: The 5th button (rightmost) should be ORANGE and say 'Digits'.",
        "STAGE 4: Click the 'Digits' button to open the modal.",
        "STAGE 5: You should see a modal with 'Remaining Digits' title.",
        "STAGE 6: Click the X button or outside the modal to close it.",
        "Verification complete! Press ESC to exit."
    ]
    
    # Print first message
    print(f"\n{messages[verification_stage]}")
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                game.mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if game.game_state == 'menu':
                        # Check menu clicks
                        if game.buttons['menu_easy'].collidepoint(event.pos):
                            game.start_game_with_difficulty('easy')
                            print("\n⚠️  You selected EASY (9x9). The 'Digits' button won't appear.")
                            print("Please restart and select MEDIUM or HARD.")
                        elif game.buttons['menu_medium'].collidepoint(event.pos):
                            game.start_game_with_difficulty('medium')
                            verification_stage = 1
                            print(f"\n✅ Good! You're now on a 16x16 grid.")
                            print(f"{messages[verification_stage]}")
                        elif game.buttons['menu_hard'].collidepoint(event.pos):
                            game.start_game_with_difficulty('hard')
                            verification_stage = 1
                            print(f"\n✅ Good! You're now on a 25x25 grid.")
                            print(f"{messages[verification_stage]}")
                        elif game.buttons['menu_howtoplay'].collidepoint(event.pos):
                            game.show_instructions = True
                    elif game.game_state == 'playing':
                        # Track modal interactions
                        if game.grid_size > 9:
                            if 'remaining' in game.buttons and game.buttons['remaining'].collidepoint(event.pos):
                                if not game.show_remaining_digits:
                                    verification_stage = 4
                                    print(f"\n✅ Modal opened successfully!")
                                    print(f"{messages[verification_stage]}")
                        
                        if game.show_remaining_digits:
                            if game.buttons['remaining_close'].collidepoint(event.pos):
                                verification_stage = 6
                                print(f"\n✅ Modal closed via X button!")
                                print(f"{messages[verification_stage]}")
                            elif not game.buttons['remaining_modal'].collidepoint(event.pos):
                                verification_stage = 6
                                print(f"\n✅ Modal closed via outside click!")
                                print(f"{messages[verification_stage]}")
                        
                        game.handle_click(event.pos)
                    
                    # Handle instruction modal
                    if game.show_instructions:
                        if game.buttons['instructions_close'].collidepoint(event.pos):
                            game.show_instructions = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif game.game_state == 'playing':
                    game.handle_key(event.key)
            elif event.type == game.timer_event:
                if game.game_state == 'playing' and not game.game_over:
                    game.seconds += 1
        
        # Render
        if game.game_state == 'menu':
            render_menu(game)
        else:
            draw_game_screen(game)
        
        # Update display
        game.clock.tick(60)
    
    pygame.quit()
    
    print("\n" + "=" * 70)
    print("Visual verification ended.")
    print("=" * 70)
    print("\nDid you successfully:")
    print("  1. See the orange 'Digits' button on 16x16/25x25 grid?")
    print("  2. Click it to open the modal?")
    print("  3. See the remaining digit counts in the modal?")
    print("  4. Close the modal?")
    print("\nIf YES to all: ✅ Feature is working correctly!")
    print("If NO to any: ❌ Please report the specific issue.\n")


if __name__ == '__main__':
    try:
        run_visual_verification()
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
