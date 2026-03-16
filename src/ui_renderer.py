"""
Sudoku Game UI Renderer
Author: Red Donaldson  
Date: March 13, 2026
"""

import pygame

# Handle both package and direct imports
try:
    from .constants import *
except ImportError:
    from constants import *


def draw_main_menu(game):
    """Draw the main menu screen"""
    game.screen.fill(MENU_BG)
    
    # Draw title
    title_text = game.title_font.render("Sudoku Flash", True, MENU_TITLE_COLOR)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
    game.screen.blit(title_text, title_rect)
    
    # Draw subtitle
    subtitle_text = game.medium_font.render("Choose Your Difficulty", True, MENU_SUBTITLE_COLOR)
    subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 180))
    game.screen.blit(subtitle_text, subtitle_rect)
    
    # Draw difficulty buttons with descriptions
    difficulty_buttons = [
        ('menu_easy', 'Easy', '9x9 Grid', '3 Lives', MENU_BUTTON_EASY, MENU_BUTTON_HOVER_EASY),
        ('menu_medium', 'Medium', '16x16 Grid', '4 Lives', MENU_BUTTON_MEDIUM, MENU_BUTTON_HOVER_MEDIUM),
        ('menu_hard', 'Hard', '25x25 Grid', '5 Lives', MENU_BUTTON_HARD, MENU_BUTTON_HOVER_HARD)
    ]
    
    for key, title, grid_desc, lives_desc, color, hover_color in difficulty_buttons:
        button = game.buttons[key]
        is_hovering = button.collidepoint(game.mouse_pos)
        button_color = hover_color if is_hovering else color
        
        # Draw button with shadow for depth
        shadow_rect = button.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(game.screen, (100, 100, 100), shadow_rect, border_radius=12)
        pygame.draw.rect(game.screen, button_color, button, border_radius=12)
        pygame.draw.rect(game.screen, BLACK, button, 3, border_radius=12)
        
        # Draw title
        title_surface = game.large_font.render(title, True, WHITE)
        title_rect = title_surface.get_rect(center=(button.centerx, button.centery - 30))
        game.screen.blit(title_surface, title_rect)
        
        # Draw grid size
        grid_surface = game.medium_font.render(grid_desc, True, WHITE)
        grid_rect = grid_surface.get_rect(center=(button.centerx, button.centery + 5))
        game.screen.blit(grid_surface, grid_rect)
        
        # Draw lives count
        lives_surface = game.small_font.render(lives_desc, True, WHITE)
        lives_rect = lives_surface.get_rect(center=(button.centerx, button.centery + 35))
        game.screen.blit(lives_surface, lives_rect)
    
    # Draw "How to Play" button
    how_to_play_button = game.buttons['menu_howtoplay']
    is_hovering = how_to_play_button.collidepoint(game.mouse_pos)
    button_color = MENU_BUTTON_HOVER_SECONDARY if is_hovering else MENU_BUTTON_SECONDARY
    
    pygame.draw.rect(game.screen, button_color, how_to_play_button, border_radius=8)
    pygame.draw.rect(game.screen, BLACK, how_to_play_button, 2, border_radius=8)
    
    howto_text = game.medium_font.render("How to Play", True, WHITE)
    howto_rect = howto_text.get_rect(center=how_to_play_button.center)
    game.screen.blit(howto_text, howto_rect)
    
    # Draw version/author info at bottom
    version_text = game.small_font.render("v2.0 | Created by Red Donaldson", True, MENU_SUBTITLE_COLOR)
    version_rect = version_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
    game.screen.blit(version_text, version_rect)
    
    # Draw instructions modal if open
    if game.show_instructions:
        draw_instructions_modal(game)
    
    pygame.display.flip()


def draw_instructions_modal(game):
    """Draw the how to play instructions modal"""
    modal = game.buttons['instructions_modal']
    
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    game.screen.blit(overlay, (0, 0))
    
    # Draw modal
    pygame.draw.rect(game.screen, WHITE, modal, border_radius=10)
    pygame.draw.rect(game.screen, BLACK, modal, 3, border_radius=10)
    
    # Title
    title_text = game.large_font.render("How to Play", True, PURPLE)
    title_rect = title_text.get_rect(center=(modal.centerx, modal.top + 40))
    game.screen.blit(title_text, title_rect)
    
    # Instructions text
    instructions = [
        "Goal: Fill the entire grid with numbers/symbols",
        "",
        "Rules:",
        "• Each row must contain all symbols once",
        "• Each column must contain all symbols once",
        "• Each box must contain all symbols once",
        "",
        "Controls:",
        "• Click a cell to select it",
        "• Type numbers/letters to fill cells",
        "• Arrow keys to navigate",
        "• P - Toggle Pencil/Pen mode",
        "• Backspace/Delete - Clear cell",
        "• Ctrl/Cmd+Z - Undo last move",
        "• ESC - Return to menu",
        "",
        "Features:",
        "• Auto-fill when only one option remains",
        "• Pencil marks for noting possibilities",
        "• Hints cost 10 points",
    ]
    
    y_offset = modal.top + 90
    for line in instructions:
        if line:
            text_surface = game.small_font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(left=modal.left + 30, top=y_offset)
            game.screen.blit(text_surface, text_rect)
        y_offset += 24  # Slightly increased spacing for better readability
    
    # Close button
    close_button = game.buttons['instructions_close']
    is_hovering = close_button.collidepoint(game.mouse_pos)
    close_color = HOVER_RED if is_hovering else DARK_RED
    
    pygame.draw.rect(game.screen, close_color, close_button, border_radius=5)
    pygame.draw.rect(game.screen, BLACK, close_button, 2, border_radius=5)
    
    close_text = game.medium_font.render("X", True, WHITE)
    close_rect = close_text.get_rect(center=close_button.center)
    game.screen.blit(close_text, close_rect)


def draw_game_screen(game):
    """Draw the complete game screen"""
    game.screen.fill(WHITE)
    
    # Draw title
    draw_title(game)
    
    # Draw game info (lives, score, timer, combo)
    draw_game_info(game)
    
    # Draw temporary messages
    draw_temporary_message(game)
    
    # Draw pencil mode indicator
    draw_pencil_mode_indicator(game)
    
    # Draw remaining numbers count
    draw_remaining_numbers(game)
    
    # Draw board with cell flash effects
    draw_board(game)
    
    # Draw laser animation effect
    draw_laser_effect(game)
    
    # Draw combo indicator
    draw_combo_indicator(game)
    
    # Draw floating points
    draw_floating_points(game)
    
    # Draw control buttons
    draw_control_buttons(game)
    
    # Draw settings modal if open
    if game.show_settings:
        draw_settings_modal(game)
    
    # Draw remaining digits modal if open
    if game.show_remaining_digits:
        draw_remaining_digits_modal(game)
    
    # Draw game over modal if game is over
    if game.show_win_message or game.show_lose_message:
        draw_game_over_modal(game)
    
    pygame.display.flip()


def draw_title(game):
    """Draw the game title"""
    title_text = game.title_font.render("Sudoku Flash", True, PURPLE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 40))
    game.screen.blit(title_text, title_rect)


def draw_game_info(game):
    """Draw lives, score, and timer
    
    FIX: Removed redundant combo display from here - Red Donaldson, March 15, 2026
    Combo is now ONLY shown via draw_combo_indicator() with pulsing glow effect.
    This eliminates duplicate display and reduces visual clutter.
    """
    info_y = 90
    
    # Lives
    lives_text = game.medium_font.render(f"Lives: {game.lives}", True, DARK_RED)
    game.screen.blit(lives_text, (80, info_y))
    
    # Score (center)
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
    """Draw temporary messages as toast notifications (not game over messages)"""
    if game.message and game.message_timer > 0 and not game.game_over:
        lines = game.message.split('\n')
        
        # Calculate dimensions for background
        max_width = max(game.small_font.render(line, True, BLACK).get_width() for line in lines)
        bg_width = max_width + 40
        bg_height = 20 + len(lines) * 25
        bg_x = (WINDOW_WIDTH - bg_width) // 2
        bg_y = 75  # Position between game info (y=90) and remaining text (y=120)
        
        # Draw semi-transparent background
        bg_rect = pygame.Rect(bg_x, bg_y, bg_width, bg_height)
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill((255, 255, 255, 230))  # White with slight transparency
        game.screen.blit(bg_surface, (bg_x, bg_y))
        
        # Draw border
        pygame.draw.rect(game.screen, game.message_color, bg_rect, 3, border_radius=8)
        
        # Draw message text
        for i, line in enumerate(lines):
            msg_text = game.small_font.render(line, True, game.message_color)
            msg_rect = msg_text.get_rect(center=(WINDOW_WIDTH // 2, bg_y + 10 + i * 25 + 12))
            game.screen.blit(msg_text, msg_rect)
        
        game.message_timer -= 1


def draw_board(game):
    """Draw the Sudoku board with cell flash effects"""
    cell_size = game.BOARD_SIZE // game.grid_size
    
    # Get selected cell value for highlighting
    selected_value = None
    if game.selected_cell:
        row, col = game.selected_cell
        selected_value = game.board[row][col]
    
    for i in range(game.grid_size):
        for j in range(game.grid_size):
            x = game.BOARD_X + j * cell_size
            y = BOARD_Y + i * cell_size
            
            # Check if this cell has a flash effect
            flash_color = None
            for flash_data in game.cell_flash_effects:
                if flash_data['row'] == i and flash_data['col'] == j:
                    # Calculate alpha based on timer (fade out effect)
                    alpha = int(255 * (flash_data['timer'] / FLASH_DURATION))
                    flash_color = flash_data['color']
                    break
            
            # Determine cell color
            if flash_color:
                # Flash effect takes priority
                color = flash_color
            elif game.selected_cell == (i, j):
                color = BLUE
            elif game.initial_board[i][j] is not None:
                color = LIGHT_GRAY
            elif selected_value and game.board[i][j] == selected_value and selected_value is not None:
                # Highlight cells with same number as selected
                color = HIGHLIGHT_NUMBER
            elif game.board[i][j] is not None and game.board[i][j] == game.solution[i][j]:
                color = GREEN
            else:
                color = WHITE
            
            pygame.draw.rect(game.screen, color, (x, y, cell_size, cell_size))
            pygame.draw.rect(game.screen, GRAY, (x, y, cell_size, cell_size), 1)
            
            # Draw enhanced glow for selected cell
            if game.selected_cell == (i, j):
                for thickness in range(GLOW_INTENSITY, 0, -1):
                    alpha_color = SELECTED_GLOW
                    pygame.draw.rect(game.screen, alpha_color, (x, y, cell_size, cell_size), thickness)
            
            # Draw number, pencil marks, or nothing
            if game.board[i][j] is not None:
                # Draw the placed number
                display_text = str(game.board[i][j])
                num_text = game.cell_font.render(display_text, True, BLACK)
                num_rect = num_text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
                game.screen.blit(num_text, num_rect)
            elif game.pencil_marks[i][j]:
                # Draw pencil marks
                draw_pencil_marks(game, i, j, x, y, cell_size)
    
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


def draw_pencil_marks(game, row, col, x, y, cell_size):
    """Draw pencil marks in a cell"""
    marks = sorted(game.pencil_marks[row][col])
    if not marks:
        return
    
    # Determine grid layout based on grid size
    if game.grid_size == 9:
        # 3x3 grid for pencil marks (positions 1-9)
        cols_per_row = 3
    elif game.grid_size == 16:
        # 4x4 grid for hex (0-F)
        cols_per_row = 4
    else:  # 25
        # 5x5 grid for alphabet
        cols_per_row = 5
    
    # Calculate spacing
    mark_spacing_x = cell_size // cols_per_row
    mark_spacing_y = cell_size // cols_per_row
    
    # Draw each pencil mark
    for idx, mark in enumerate(marks):
        # Calculate position in grid
        if game.grid_size == 9:
            # For 9x9, marks 1-9 map to positions 0-8
            try:
                mark_num = int(mark) - 1
            except:
                mark_num = idx
        elif game.grid_size == 16:
            # For 16x16, hex 0-F map to positions 0-15
            if mark.isdigit():
                mark_num = int(mark)
            else:
                mark_num = ord(mark) - ord('A') + 10
        else:
            # For 25x25, A-Y map to positions
            mark_num = ord(mark) - ord('A')
        
        mark_row = mark_num // cols_per_row
        mark_col = mark_num % cols_per_row
        
        # Calculate pixel position
        mark_x = x + mark_col * mark_spacing_x + mark_spacing_x // 2
        mark_y = y + mark_row * mark_spacing_y + mark_spacing_y // 2
        
        # Draw the mark
        mark_text = game.pencil_font.render(str(mark), True, (100, 100, 100))  # Dark gray for visibility
        mark_rect = mark_text.get_rect(center=(mark_x, mark_y))
        game.screen.blit(mark_text, mark_rect)


def draw_pencil_mode_indicator(game):
    """Draw pencil mode indicator"""
    mode_text = "[P] Pencil Mode" if game.pencil_mode else "[P] Pen Mode"
    mode_color = PURPLE if game.pencil_mode else BLACK
    text = game.small_font.render(mode_text, True, mode_color)
    text_rect = text.get_rect(right=WINDOW_WIDTH - 80, top=135)
    game.screen.blit(text, text_rect)


def draw_remaining_numbers(game):
    """Draw remaining numbers count for each symbol"""
    # Calculate remaining count for each symbol
    remaining = {}
    total_remaining = 0
    for symbol in game.symbols:
        total_needed = game.grid_size
        placed = sum(1 for i in range(game.grid_size) for j in range(game.grid_size) 
                     if game.solution[i][j] == symbol and game.board[i][j] == symbol)
        remaining[symbol] = total_needed - placed
        total_remaining += remaining[symbol]
    
    # For large grids (16x16, 25x25), only show on screen when < 10 digits remaining
    # Otherwise hide them (user can click "Remaining" button to see modal)
    if game.grid_size > 9 and total_remaining >= 10:
        return  # Don't draw anything, user must open modal
    
    # Draw title
    # FIX: Position to ensure NO overlap with board at y=180 - Red Donaldson, March 15, 2026
    # Lives text at y=90 (height ~25px) ends around y=115
    # Title at y=120 (height ~25px) ends at y=145, provides 5px gap after Lives
    # Board starts at y=180, all text MUST end before that
    title_text = game.small_font.render("Remaining:", True, BLACK)
    title_rect = title_text.get_rect(left=80, top=120)
    game.screen.blit(title_text, title_rect)
    
    # Draw counts in compact format with proper spacing for Courier New
    # FIX: Position at y=150 to ensure text never hides below grid - Red Donaldson, March 15, 2026
    # Title ends at ~y=145, counts at y=150 provide 5px gap
    # With text height 25px, first row ends at y=175
    # Board starts at y=180, providing 5px clearance - NO OVERLAP
    # Verified by scripts/test_board_boundaries.py
    y_pos = 150
    x_pos = 80
    # FIX: Adjusted items_per_row to fit all items in fewer rows - Red Donaldson, March 15, 2026
    # With spacing=55px, starting at x=80, and window width=800:
    # Available width: 800 - 80 = 720px
    # Items per row: 720 / 55 = 13.09, so 13 items max per row
    # 9x9: 9 items fit in one row (ends at y=160, board at y=180, 20px clearance ✓)
    # For 16x16 or 25x25 with < 10 remaining: fits in one row (ends at y=160 ✓)
    # Even if we show up to 13 items: still one row (ends at y=160 ✓)
    items_per_row = 13  # Use 13 for all grid sizes to minimize rows
    # FIX: Increased spacing to 55px minimum to prevent overlap (text width 52px + 3px padding)
    # Diagnostic showed actual text width: "X:99" = 52px, so 55px ensures no overlap
    spacing = 55
    
    for idx, symbol in enumerate(game.symbols):
        count = remaining[symbol]
        
        # Color code: gray if complete, black otherwise
        color = GRAY if count == 0 else BLACK
        
        # Format as "1:5" (symbol:count)
        count_text = game.small_font.render(f"{symbol}:{count}", True, color)
        count_rect = count_text.get_rect(left=x_pos, top=y_pos)
        game.screen.blit(count_text, count_rect)
        
        # Move to next position
        x_pos += spacing
        if (idx + 1) % items_per_row == 0:
            x_pos = 80
            y_pos += 26  # FIX: Increased from 22 to provide better vertical spacing (text height 25px + 1px gap minimum)



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
    """Draw control buttons with hover effects"""
    button_data = [
        ('new_game', 'New', DARK_BLUE, HOVER_BLUE),
        ('hint', 'Hint', DARK_GREEN, HOVER_GREEN),
        ('undo', 'Undo', UNDO_COLOR, (180, 180, 180)),
        ('settings', 'Settings', PURPLE, HOVER_PURPLE),
        ('remaining', 'Remaining', BUTTON_ORANGE, HOVER_ORANGE)
    ]
    
    for key, text, color, hover_color in button_data:
        # Skip "Remaining" button for small grids (9x9)
        if key == 'remaining' and game.grid_size <= 9:
            continue
            
        # Defensive check: ensure button exists before trying to access it
        if key not in game.buttons:
            print(f"Warning: Button '{key}' not found in game.buttons")
            continue
            
        rect = game.buttons[key]
        
        # Check if mouse is hovering over button
        is_hovering = rect.collidepoint(game.mouse_pos)
        button_color = hover_color if is_hovering else color
        
        pygame.draw.rect(game.screen, button_color, rect)
        pygame.draw.rect(game.screen, BLACK, rect, 2)
        
        text_surface = game.button_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        game.screen.blit(text_surface, text_rect)


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
        is_hovering = button.collidepoint(game.mouse_pos)
        
        # Determine button color
        if game.difficulty == diff:
            color = HOVER_GREEN if is_hovering else DARK_GREEN
        else:
            color = LIGHT_GRAY if is_hovering else GRAY
        
        pygame.draw.rect(game.screen, color, button)
        pygame.draw.rect(game.screen, BLACK, button, 2)
        
        # Use smaller font for button text
        text_color = WHITE if game.difficulty == diff else BLACK
        text_surface = game.small_font.render(label, True, text_color)
        text_rect = text_surface.get_rect(center=button.center)
        game.screen.blit(text_surface, text_rect)
    
    # FIX: Removed "Check Solution" button - Red Donaldson, March 15, 2026
    # REASON: Redundant with lives system which provides instant feedback.
    # With instant wrong-answer penalties, players already know their status.
    # "Check Solution" serves no gameplay purpose when lives system is active.
    # This simplifies the settings modal and removes conflicting game mechanics.
    
    # Close button
    close_button = game.buttons['settings_close']
    is_close_hovering = close_button.collidepoint(game.mouse_pos)
    close_color = HOVER_RED if is_close_hovering else DARK_RED
    
    pygame.draw.rect(game.screen, close_color, close_button)
    pygame.draw.rect(game.screen, BLACK, close_button, 2)
    
    close_text = game.medium_font.render("X", True, WHITE)
    close_rect = close_text.get_rect(center=close_button.center)
    game.screen.blit(close_text, close_rect)


def draw_remaining_digits_modal(game):
    """Draw the remaining digits modal for large grids"""
    modal = game.buttons['remaining_modal']
    
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    game.screen.blit(overlay, (0, 0))
    
    # Draw modal
    pygame.draw.rect(game.screen, WHITE, modal, border_radius=10)
    pygame.draw.rect(game.screen, BLACK, modal, 3, border_radius=10)
    
    # Title
    title_text = game.large_font.render("Remaining Digits", True, BUTTON_ORANGE)
    title_rect = title_text.get_rect(center=(modal.centerx, modal.top + 40))
    game.screen.blit(title_text, title_rect)
    
    # Calculate remaining count for each symbol
    remaining = {}
    total_remaining = 0
    for symbol in game.symbols:
        total_needed = game.grid_size
        placed = sum(1 for i in range(game.grid_size) for j in range(game.grid_size) 
                     if game.solution[i][j] == symbol and game.board[i][j] == symbol)
        remaining[symbol] = total_needed - placed
        total_remaining += remaining[symbol]
    
    # Display total remaining
    total_text = game.medium_font.render(f"Total Remaining: {total_remaining}", True, DARK_GREEN)
    total_rect = total_text.get_rect(center=(modal.centerx, modal.top + 85))
    game.screen.blit(total_text, total_rect)
    
    # Draw counts in grid format
    y_pos = modal.top + 130
    x_start = modal.left + 30
    
    # Determine layout based on grid size with spacing for Courier New
    # FIX: Increased horizontal spacing to 70px to prevent overlap (text width 65px + 5px padding)
    # BUT reduced items_per_row to fit within modal width (500px)
    # Modal usable width: 500 - 60 (margins) = 440px
    # With spacing=70px: 440 / 70 = 6.28, so 6 items per row maximum
    # Diagnostic showed actual text width: "X: 99" = 65px, so 70px ensures no overlap
    if game.grid_size == 16:
        items_per_row = 6  # Reduced from 8 to fit in modal (6 * 70 = 420px < 440px)
        spacing_x = 70  # Increased from 58 to prevent overlap
        spacing_y = 37  # Vertical spacing is OK
    else:  # 25x25
        items_per_row = 6  # Reduced from 10 to fit in modal
        spacing_x = 70  # Increased from 47 to prevent overlap
        spacing_y = 34  # Vertical spacing is OK
    
    x_pos = x_start
    
    for idx, symbol in enumerate(game.symbols):
        count = remaining[symbol]
        
        # Color code: gray if complete, dark green if low, black otherwise
        if count == 0:
            color = GRAY
        elif count <= 2:
            color = DARK_RED  # Nearly complete
        elif count <= 5:
            color = BUTTON_ORANGE  # Getting close
        else:
            color = BLACK
        
        # Format as "A: 5" (symbol: count)
        count_text = game.small_font.render(f"{symbol}: {count}", True, color)
        count_rect = count_text.get_rect(left=x_pos, top=y_pos)
        game.screen.blit(count_text, count_rect)
        
        # Move to next position
        x_pos += spacing_x
        if (idx + 1) % items_per_row == 0:
            x_pos = x_start
            y_pos += spacing_y
    
    # Close button
    close_button = game.buttons['remaining_close']
    is_close_hovering = close_button.collidepoint(game.mouse_pos)
    close_color = HOVER_RED if is_close_hovering else DARK_RED
    
    pygame.draw.rect(game.screen, close_color, close_button, border_radius=5)
    pygame.draw.rect(game.screen, BLACK, close_button, 2, border_radius=5)
    
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
    is_hovering = newgame_button.collidepoint(game.mouse_pos)
    button_color = HOVER_GREEN if is_hovering else DARK_GREEN
    
    pygame.draw.rect(game.screen, button_color, newgame_button)
    pygame.draw.rect(game.screen, BLACK, newgame_button, 2)
    
    newgame_text = game.small_font.render("New Game", True, WHITE)
    newgame_rect = newgame_text.get_rect(center=newgame_button.center)
    game.screen.blit(newgame_text, newgame_rect)
    
    # Return to Menu button
    menu_button = game.buttons['gameover_menu']
    is_menu_hovering = menu_button.collidepoint(game.mouse_pos)
    menu_color = HOVER_PURPLE if is_menu_hovering else PURPLE
    
    pygame.draw.rect(game.screen, menu_color, menu_button)
    pygame.draw.rect(game.screen, BLACK, menu_button, 2)
    
    menu_text = game.small_font.render("Main Menu", True, WHITE)
    menu_rect = menu_text.get_rect(center=menu_button.center)
    game.screen.blit(menu_text, menu_rect)


def draw_floating_points(game):
    """Draw floating point animations"""
    for point_data in game.floating_points:
        x = int(point_data['x'])
        y = int(point_data['y'])
        points = point_data['points']
        color = point_data['color']
        timer = point_data['timer']
        
        # Calculate alpha based on timer (fade out effect)
        alpha = int(255 * (timer / FLOATING_TEXT_DURATION))
        alpha = max(50, min(255, alpha))  # Clamp between 50-255
        
        # Create text with shadow for better visibility
        point_text = f"+{points}"
        
        # Shadow
        shadow_surface = game.medium_font.render(point_text, True, BLACK)
        shadow_rect = shadow_surface.get_rect(center=(x + 2, y + 2))
        shadow_surface.set_alpha(alpha // 2)
        game.screen.blit(shadow_surface, shadow_rect)
        
        # Main text
        text_surface = game.medium_font.render(point_text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        text_surface.set_alpha(alpha)
        game.screen.blit(text_surface, text_rect)


def draw_combo_indicator(game):
    """Draw combo streak indicator with pulsing glow effect"""
    if game.combo_count <= 0:
        return
    
    # FIX: Position moved up to y=50 to avoid overlap with board and other UI - Red Donaldson, March 15, 2026
    # Previous position y=160 caused overlap: text extends to y=182, but board starts at y=180
    # New position y=50 places combo in clear area above Lives/Score/Timer (which start at y=90)
    # This provides good visual separation and ensures no board overlap
    x = 100
    y = 50
    
    combo_idx = min(game.combo_count, COMBO_MAX_LEVEL)
    combo_color = COMBO_COLORS[combo_idx]
    
    # Draw combo text - no scaling to maintain character size consistency
    combo_text = f"{game.combo_multiplier:.1f}x"
    text_surface = game.large_font.render(combo_text, True, combo_color)
    text_rect = text_surface.get_rect(center=(x, y))
    
    # Draw pulsing glow effect using alpha instead of scaling
    glow_alpha = int(50 + 50 * abs((game.seconds * 3) % 20 - 10) / 10)
    glow_surface = game.large_font.render(combo_text, True, (255, 255, 255))
    glow_surface.set_alpha(glow_alpha)
    
    # Draw multiple glow layers at same size for pulse effect
    for offset in range(1, 3):
        glow_rect = text_surface.get_rect(center=(x + offset, y + offset))
        game.screen.blit(glow_surface, glow_rect)
        glow_rect = text_surface.get_rect(center=(x - offset, y - offset))
        game.screen.blit(glow_surface, glow_rect)
    
    # Draw main text
    game.screen.blit(text_surface, text_rect)
    
    # Draw "COMBO!" label below
    label_surface = game.small_font.render("COMBO!", True, combo_color)
    label_rect = label_surface.get_rect(center=(x, y + 25))
    game.screen.blit(label_surface, label_rect)
