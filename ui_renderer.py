"""
Sudoku Game UI Renderer
Author: Red Donaldson  
Date: March 13, 2026
"""

import pygame
from constants import *


def draw_game_screen(game):
    """Draw the complete game screen"""
    game.screen.fill(WHITE)
    
    # Draw title
    draw_title(game)
    
    # Draw game info (lives, score, timer)
    draw_game_info(game)
    
    # Draw temporary messages
    draw_temporary_message(game)
    
    # Draw board
    draw_board(game)
    
    # Draw laser animation effect
    draw_laser_effect(game)
    
    # Draw control buttons
    draw_control_buttons(game)
    
    # Draw confirm/clear buttons for larger grids
    if game.grid_size != 9:
        draw_cell_buttons(game)
    
    # Draw settings modal if open
    if game.show_settings:
        draw_settings_modal(game)
    
    # Draw game over modal if game is over
    if game.show_win_message or game.show_lose_message:
        draw_game_over_modal(game)
    
    pygame.display.flip()


def draw_title(game):
    """Draw the game title"""
    title_text = game.title_font.render("Sudoku Game", True, PURPLE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 40))
    game.screen.blit(title_text, title_rect)


def draw_game_info(game):
    """Draw lives, score, and timer"""
    info_y = 90
    
    # Lives
    lives_text = game.medium_font.render(f"Lives: {game.lives}", True, DARK_RED)
    game.screen.blit(lives_text, (80, info_y))
    
    # Score
    score_text = game.medium_font.render(f"Score: {game.score}", True, DARK_GREEN)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, info_y + 12))
    game.screen.blit(score_text, score_rect)
    
    # Timer
    minutes = game.seconds // 60
    seconds = game.seconds % 60
    timer_text = game.medium_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, BLACK)
    timer_rect = timer_text.get_rect(right=WINDOW_WIDTH - 80, centery=info_y + 12)
    game.screen.blit(timer_text, timer_rect)


def draw_temporary_message(game):
    """Draw temporary messages (not game over messages)"""
    if game.message and game.message_timer > 0 and not game.game_over:
        lines = game.message.split('\n')
        for i, line in enumerate(lines):
            msg_text = game.small_font.render(line, True, game.message_color)
            msg_rect = msg_text.get_rect(center=(WINDOW_WIDTH // 2, 135 + i * 22))
            game.screen.blit(msg_text, msg_rect)
        game.message_timer -= 1


def draw_board(game):
    """Draw the Sudoku board"""
    cell_size = game.BOARD_SIZE // game.grid_size
    
    for i in range(game.grid_size):
        for j in range(game.grid_size):
            x = game.BOARD_X + j * cell_size
            y = BOARD_Y + i * cell_size
            
            # Determine cell color
            if game.selected_cell == (i, j):
                if game.grid_size != 9 and game.cell_input_buffer:
                    color = YELLOW
                else:
                    color = BLUE
            elif game.initial_board[i][j] is not None:
                color = LIGHT_GRAY
            elif game.board[i][j] is not None and game.board[i][j] == game.solution[i][j]:
                color = GREEN
            else:
                color = WHITE
            
            pygame.draw.rect(game.screen, color, (x, y, cell_size, cell_size))
            pygame.draw.rect(game.screen, GRAY, (x, y, cell_size, cell_size), 1)
            
            # Draw number or buffer
            display_text = None
            if game.selected_cell == (i, j) and game.cell_input_buffer and game.grid_size != 9:
                display_text = game.cell_input_buffer
            elif game.board[i][j] is not None:
                display_text = str(game.board[i][j])
            
            if display_text:
                num_text = game.cell_font.render(display_text, True, BLACK)
                num_rect = num_text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
                game.screen.blit(num_text, num_rect)
    
    # Draw thick lines for boxes
    for i in range(0, game.grid_size + 1, game.box_size):
        # Horizontal
        pygame.draw.line(game.screen, BLACK,
                       (game.BOARD_X, BOARD_Y + i * cell_size),
                       (game.BOARD_X + game.BOARD_SIZE, BOARD_Y + i * cell_size), 3)
        # Vertical
        pygame.draw.line(game.screen, BLACK,
                       (game.BOARD_X + i * cell_size, BOARD_Y),
                       (game.BOARD_X + i * cell_size, BOARD_Y + game.BOARD_SIZE), 3)


def draw_laser_effect(game):
    """Draw laser effect between animated cells"""
    if not game.animation_queue or game.laser_source is None:
        return
    
    source_row, source_col = game.laser_source
    target_row, target_col = game.animation_queue[0][0], game.animation_queue[0][1]
    
    source_pos = get_cell_center(game, source_row, source_col)
    target_pos = get_cell_center(game, target_row, target_col)
    
    progress = game.current_animation_frame / ANIMATION_SPEED
    
    laser_x = source_pos[0] + (target_pos[0] - source_pos[0]) * progress
    laser_y = source_pos[1] + (target_pos[1] - source_pos[1]) * progress
    
    laser_color = (100, 200, 255)
    glow_color = (150, 220, 255)
    
    pygame.draw.line(game.screen, glow_color, source_pos, (laser_x, laser_y), 8)
    pygame.draw.line(game.screen, laser_color, source_pos, (laser_x, laser_y), 4)
    
    pygame.draw.circle(game.screen, WHITE, (int(laser_x), int(laser_y)), 6)
    pygame.draw.circle(game.screen, laser_color, (int(laser_x), int(laser_y)), 4)


def get_cell_center(game, row, col):
    """Get the center coordinates of a cell"""
    cell_size = game.BOARD_SIZE // game.grid_size
    x = game.BOARD_X + col * cell_size + cell_size // 2
    y = BOARD_Y + row * cell_size + cell_size // 2
    return (x, y)


def draw_control_buttons(game):
    """Draw control buttons"""
    button_data = [
        ('new_game', 'New Game', DARK_BLUE),
        ('hint', 'Hint', DARK_GREEN),
        ('settings', 'Settings', PURPLE)
    ]
    
    for key, text, color in button_data:
        rect = game.buttons[key]
        pygame.draw.rect(game.screen, color, rect)
        pygame.draw.rect(game.screen, BLACK, rect, 2)
        
        text_surface = game.button_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        game.screen.blit(text_surface, text_rect)


def draw_cell_buttons(game):
    """Draw confirm/clear buttons for multi-character input"""
    # Confirm button
    pygame.draw.rect(game.screen, DARK_GREEN, game.buttons['confirm'])
    pygame.draw.rect(game.screen, BLACK, game.buttons['confirm'], 2)
    confirm_text = game.button_font.render("Confirm", True, WHITE)
    confirm_rect = confirm_text.get_rect(center=game.buttons['confirm'].center)
    game.screen.blit(confirm_text, confirm_rect)
    
    # Clear button
    pygame.draw.rect(game.screen, DARK_RED, game.buttons['clear_cell'])
    pygame.draw.rect(game.screen, BLACK, game.buttons['clear_cell'], 2)
    clear_text = game.button_font.render("Clear", True, WHITE)
    clear_rect = clear_text.get_rect(center=game.buttons['clear_cell'].center)
    game.screen.blit(clear_text, clear_rect)


def draw_settings_modal(game):
    """Draw the settings modal"""
    modal = game.buttons['settings_modal']
    
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    game.screen.blit(overlay, (0, 0))
    
    # Draw modal
    pygame.draw.rect(game.screen, WHITE, modal)
    pygame.draw.rect(game.screen, BLACK, modal, 3)
    
    # Title
    title_text = game.large_font.render("Settings", True, PURPLE)
    title_rect = title_text.get_rect(center=(modal.centerx, modal.top + 40))
    game.screen.blit(title_text, title_rect)
    
    # Difficulty label
    diff_label = game.medium_font.render("Difficulty:", True, BLACK)
    diff_label_rect = diff_label.get_rect(center=(modal.centerx, modal.top + 80))
    game.screen.blit(diff_label, diff_label_rect)
    
    # Difficulty buttons
    difficulties = ['easy', 'medium', 'hard']
    labels = ['Easy (9x9)', 'Med (16x16)', 'Hard (25x25)']
    
    for i, (diff, label) in enumerate(zip(difficulties, labels)):
        button = game.buttons[diff]
        color = DARK_GREEN if game.difficulty == diff else GRAY
        
        pygame.draw.rect(game.screen, color, button)
        pygame.draw.rect(game.screen, BLACK, button, 2)
        
        # Use smaller font for button text
        text_surface = game.small_font.render(label, True, WHITE if game.difficulty == diff else BLACK)
        text_rect = text_surface.get_rect(center=button.center)
        game.screen.blit(text_surface, text_rect)
    
    # Check button
    check_button = game.buttons['check']
    pygame.draw.rect(game.screen, DARK_BLUE, check_button)
    pygame.draw.rect(game.screen, BLACK, check_button, 2)
    
    check_text = game.button_font.render("Check Solution", True, WHITE)
    check_rect = check_text.get_rect(center=check_button.center)
    game.screen.blit(check_text, check_rect)
    
    # Close button
    close_button = game.buttons['settings_close']
    pygame.draw.rect(game.screen, DARK_RED, close_button)
    pygame.draw.rect(game.screen, BLACK, close_button, 2)
    
    close_text = game.medium_font.render("X", True, WHITE)
    close_rect = close_text.get_rect(center=close_button.center)
    game.screen.blit(close_text, close_rect)


def draw_game_over_modal(game):
    """Draw the game over modal"""
    modal = game.buttons['gameover_modal']
    
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    game.screen.blit(overlay, (0, 0))
    
    # Draw modal
    pygame.draw.rect(game.screen, WHITE, modal)
    pygame.draw.rect(game.screen, BLACK, modal, 3)
    
    # Title - Victory or Game Over
    if game.show_win_message:
        title_text = game.large_font.render("Victory!", True, DARK_GREEN)
    else:
        title_text = game.large_font.render("Game Over", True, DARK_RED)
    title_rect = title_text.get_rect(center=(modal.centerx, modal.top + 50))
    game.screen.blit(title_text, title_rect)
    
    # Display game stats
    y_offset = modal.top + 110
    
    # Score
    score_text = game.medium_font.render(f"Final Score: {game.score}", True, BLACK)
    score_rect = score_text.get_rect(center=(modal.centerx, y_offset))
    game.screen.blit(score_text, score_rect)
    
    # Time
    minutes = game.seconds // 60
    seconds = game.seconds % 60
    time_text = game.medium_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, BLACK)
    time_rect = time_text.get_rect(center=(modal.centerx, y_offset + 40))
    game.screen.blit(time_text, time_rect)
    
    # Lives remaining (if won)
    if game.show_win_message:
        lives_text = game.medium_font.render(f"Lives Remaining: {game.lives}", True, BLACK)
        lives_rect = lives_text.get_rect(center=(modal.centerx, y_offset + 80))
        game.screen.blit(lives_text, lives_rect)
    
    # New game button
    newgame_button = game.buttons['gameover_newgame']
    pygame.draw.rect(game.screen, DARK_GREEN, newgame_button)
    pygame.draw.rect(game.screen, BLACK, newgame_button, 2)
    
    newgame_text = game.button_font.render("New Game", True, WHITE)
    newgame_rect = newgame_text.get_rect(center=newgame_button.center)
    game.screen.blit(newgame_text, newgame_rect)
