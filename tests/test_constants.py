"""
Test Suite for Constants Module
Author: Red Donaldson
Date: March 13, 2026

Tests validate that all constants are properly defined and 
have expected values for different difficulty levels.
"""

import pytest
from src.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BOARD_Y,
    WHITE,
    BLACK,
    FONT_NAME,
    FONT_SIZES,
    DIFFICULTY_SETTINGS,
    ANIMATION_SPEED,
    FPS
)


class TestWindowConstants:
    """Test window-related constants"""
    
    def test_window_dimensions_positive(self):
        """Test that window dimensions are positive integers"""
        assert WINDOW_WIDTH > 0
        assert WINDOW_HEIGHT > 0
        assert isinstance(WINDOW_WIDTH, int)
        assert isinstance(WINDOW_HEIGHT, int)
    
    def test_window_dimensions_reasonable(self):
        """Test that window dimensions are reasonable sizes"""
        assert 600 <= WINDOW_WIDTH <= 2000
        assert 600 <= WINDOW_HEIGHT <= 2000
    
    def test_board_y_position(self):
        """Test that board Y position is within window"""
        assert 0 <= BOARD_Y < WINDOW_HEIGHT


class TestColorConstants:
    """Test color definitions"""
    
    def test_colors_are_tuples(self):
        """Test that colors are RGB tuples"""
        colors = [WHITE, BLACK]
        for color in colors:
            assert isinstance(color, tuple)
            assert len(color) == 3
    
    def test_color_values_in_range(self):
        """Test that color values are in valid RGB range"""
        colors = [WHITE, BLACK]
        for color in colors:
            for value in color:
                assert 0 <= value <= 255
    
    def test_basic_colors_correct(self):
        """Test that basic colors have correct values"""
        assert WHITE == (255, 255, 255)
        assert BLACK == (0, 0, 0)


class TestFontConstants:
    """Test font-related constants"""
    
    def test_font_name_is_string(self):
        """Test that font name is a string"""
        assert isinstance(FONT_NAME, str)
        assert len(FONT_NAME) > 0
    
    def test_font_sizes_dictionary(self):
        """Test that font sizes are properly defined"""
        assert isinstance(FONT_SIZES, dict)
        
        required_sizes = ['title', 'large', 'medium', 'small', 'button']
        for size_name in required_sizes:
            assert size_name in FONT_SIZES
            assert isinstance(FONT_SIZES[size_name], int)
            assert FONT_SIZES[size_name] > 0
    
    def test_font_sizes_order(self):
        """Test that font sizes follow logical ordering"""
        assert FONT_SIZES['title'] > FONT_SIZES['large']
        assert FONT_SIZES['large'] > FONT_SIZES['medium']
        assert FONT_SIZES['medium'] > FONT_SIZES['small']


class TestDifficultySettings:
    """Test difficulty settings configuration"""
    
    def test_all_difficulties_present(self):
        """Test that all difficulty levels are defined"""
        assert 'easy' in DIFFICULTY_SETTINGS
        assert 'medium' in DIFFICULTY_SETTINGS
        assert 'hard' in DIFFICULTY_SETTINGS
    
    def test_easy_settings(self):
        """Test easy difficulty settings"""
        easy = DIFFICULTY_SETTINGS['easy']
        
        assert easy['grid_size'] == 9
        assert easy['box_size'] == 3
        assert len(easy['symbols']) == 9
        assert easy['symbols'] == list('123456789')
        assert easy['cells_to_remove'] > 0
        assert easy['lives'] > 0
        assert easy['points_per_cell'] > 0
    
    def test_medium_settings(self):
        """Test medium difficulty settings"""
        medium = DIFFICULTY_SETTINGS['medium']
        
        assert medium['grid_size'] == 16
        assert medium['box_size'] == 4
        assert len(medium['symbols']) == 16
        assert medium['symbols'] == list('0123456789ABCDEF')
        assert medium['cells_to_remove'] > 0
        assert medium['lives'] > 0
        assert medium['points_per_cell'] > 0
    
    def test_hard_settings(self):
        """Test hard difficulty settings"""
        hard = DIFFICULTY_SETTINGS['hard']
        
        assert hard['grid_size'] == 25
        assert hard['box_size'] == 5
        assert len(hard['symbols']) == 25  # A-Z excluding X = 25 letters
        assert 'X' not in hard['symbols']
        assert hard['cells_to_remove'] > 0
        assert hard['lives'] > 0
        assert hard['points_per_cell'] > 0
    
    def test_grid_box_relationship(self):
        """Test that grid_size = box_size^2 for all difficulties"""
        for difficulty, settings in DIFFICULTY_SETTINGS.items():
            grid_size = settings['grid_size']
            box_size = settings['box_size']
            assert grid_size == box_size * box_size
    
    def test_symbols_match_grid_size(self):
        """Test that number of symbols matches grid size"""
        for difficulty, settings in DIFFICULTY_SETTINGS.items():
            assert len(settings['symbols']) == settings['grid_size']
    
    def test_difficulty_progression(self):
        """Test that difficulty increases appropriately"""
        # Grid sizes increase
        assert DIFFICULTY_SETTINGS['easy']['grid_size'] < DIFFICULTY_SETTINGS['medium']['grid_size']
        assert DIFFICULTY_SETTINGS['medium']['grid_size'] < DIFFICULTY_SETTINGS['hard']['grid_size']
        
        # Cells to remove increases
        assert DIFFICULTY_SETTINGS['easy']['cells_to_remove'] < DIFFICULTY_SETTINGS['medium']['cells_to_remove']
        assert DIFFICULTY_SETTINGS['medium']['cells_to_remove'] < DIFFICULTY_SETTINGS['hard']['cells_to_remove']
        
        # Points per cell increases
        assert DIFFICULTY_SETTINGS['easy']['points_per_cell'] < DIFFICULTY_SETTINGS['medium']['points_per_cell']
        assert DIFFICULTY_SETTINGS['medium']['points_per_cell'] < DIFFICULTY_SETTINGS['hard']['points_per_cell']
    
    def test_cells_to_remove_reasonable(self):
        """Test that cells_to_remove is reasonable percentage"""
        for difficulty, settings in DIFFICULTY_SETTINGS.items():
            total_cells = settings['grid_size'] ** 2
            removed = settings['cells_to_remove']
            
            # Should remove between 40% and 90% of cells
            assert 0.4 * total_cells <= removed <= 0.9 * total_cells


class TestAnimationConstants:
    """Test animation-related constants"""
    
    def test_animation_speed_positive(self):
        """Test that animation speed is positive"""
        assert ANIMATION_SPEED > 0
        assert isinstance(ANIMATION_SPEED, int)
    
    def test_fps_reasonable(self):
        """Test that FPS is a reasonable value"""
        assert isinstance(FPS, int)
        assert 30 <= FPS <= 120  # Common FPS range for games
    
    def test_fps_positive(self):
        """Test that FPS is positive"""
        assert FPS > 0


class TestConstantsIntegrity:
    """Test overall constants integrity"""
    
    def test_no_none_values(self):
        """Test that no constants are None"""
        assert WINDOW_WIDTH is not None
        assert WINDOW_HEIGHT is not None
        assert BOARD_Y is not None
        assert ANIMATION_SPEED is not None
        assert FPS is not None
    
    def test_difficulty_settings_completeness(self):
        """Test that all difficulty settings have required keys"""
        required_keys = ['grid_size', 'box_size', 'symbols', 
                        'cells_to_remove', 'lives', 'points_per_cell']
        
        for difficulty, settings in DIFFICULTY_SETTINGS.items():
            for key in required_keys:
                assert key in settings, f"{key} missing from {difficulty}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
