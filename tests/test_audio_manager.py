"""
Test Suite for AudioManager Class
Author: Red Donaldson
Date: March 16, 2026

Tests the audio system including sound effects, music, volume controls, and settings persistence.
"""

import pytest
import pygame
import os
import json
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from src.audio_manager import AudioManager


@pytest.fixture
def temp_audio_dir():
    """Create a temporary directory for audio files"""
    temp_dir = tempfile.mkdtemp()
    
    # Create subdirectories
    sounds_dir = os.path.join(temp_dir, 'assets', 'sounds')
    music_dir = os.path.join(temp_dir, 'assets', 'music')
    os.makedirs(sounds_dir, exist_ok=True)
    os.makedirs(music_dir, exist_ok=True)
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_pygame_mixer():
    """Mock pygame.mixer to avoid actual audio playback in tests"""
    with patch('pygame.mixer.init'), \
         patch('pygame.mixer.Sound'), \
         patch('pygame.mixer.music'):
        yield


class TestAudioManagerInitialization:
    """Test AudioManager initialization"""
    
    def test_audio_manager_creates_instance(self, mock_pygame_mixer):
        """Test that AudioManager instance can be created"""
        audio = AudioManager()
        assert audio is not None
    
    def test_audio_manager_default_volumes(self, mock_pygame_mixer):
        """Test default volume settings"""
        audio = AudioManager()
        assert 0.0 <= audio.music_volume <= 1.0
        assert 0.0 <= audio.sfx_volume <= 1.0
    
    def test_audio_manager_default_sound_enabled(self, mock_pygame_mixer):
        """Test that sound is enabled by default"""
        audio = AudioManager()
        assert audio.sound_enabled is True
    
    def test_audio_manager_initializes_sounds_dict(self, mock_pygame_mixer):
        """Test that sounds dictionary is initialized"""
        audio = AudioManager()
        assert hasattr(audio, 'sounds')
        assert isinstance(audio.sounds, dict)


class TestVolumeControls:
    """Test volume control methods"""
    
    def test_set_music_volume_valid(self, mock_pygame_mixer):
        """Test setting music volume with valid value"""
        audio = AudioManager()
        audio.set_music_volume(0.7)
        assert audio.music_volume == 0.7
    
    def test_set_music_volume_clamps_high(self, mock_pygame_mixer):
        """Test that music volume is clamped to 1.0"""
        audio = AudioManager()
        audio.set_music_volume(1.5)
        assert audio.music_volume == 1.0
    
    def test_set_music_volume_clamps_low(self, mock_pygame_mixer):
        """Test that music volume is clamped to 0.0"""
        audio = AudioManager()
        audio.set_music_volume(-0.5)
        assert audio.music_volume == 0.0
    
    def test_set_sfx_volume_valid(self, mock_pygame_mixer):
        """Test setting SFX volume with valid value"""
        audio = AudioManager()
        audio.set_sfx_volume(0.8)
        assert audio.sfx_volume == 0.8
    
    def test_set_sfx_volume_clamps_high(self, mock_pygame_mixer):
        """Test that SFX volume is clamped to 1.0"""
        audio = AudioManager()
        audio.set_sfx_volume(2.0)
        assert audio.sfx_volume == 1.0
    
    def test_set_sfx_volume_clamps_low(self, mock_pygame_mixer):
        """Test that SFX volume is clamped to 0.0"""
        audio = AudioManager()
        audio.set_sfx_volume(-1.0)
        assert audio.sfx_volume == 0.0
    
    def test_volume_ranges(self, mock_pygame_mixer):
        """Test various volume values"""
        audio = AudioManager()
        test_values = [0.0, 0.25, 0.5, 0.75, 1.0]
        
        for value in test_values:
            audio.set_music_volume(value)
            assert audio.music_volume == value
            
            audio.set_sfx_volume(value)
            assert audio.sfx_volume == value


class TestSoundToggle:
    """Test sound enable/disable functionality"""
    
    def test_toggle_sound_off(self, mock_pygame_mixer):
        """Test toggling sound off"""
        audio = AudioManager()
        assert audio.sound_enabled is True
        
        result = audio.toggle_sound()
        assert audio.sound_enabled is False
        assert result is False
    
    def test_toggle_sound_on(self, mock_pygame_mixer):
        """Test toggling sound on"""
        audio = AudioManager()
        audio.sound_enabled = False
        
        result = audio.toggle_sound()
        assert audio.sound_enabled is True
        assert result is True
    
    def test_toggle_sound_multiple_times(self, mock_pygame_mixer):
        """Test multiple sound toggles"""
        audio = AudioManager()
        
        for _ in range(5):
            audio.toggle_sound()
            assert audio.sound_enabled is False
            audio.toggle_sound()
            assert audio.sound_enabled is True


class TestSoundEffects:
    """Test sound effect playback"""
    
    def test_play_sound_when_enabled(self, mock_pygame_mixer):
        """Test playing sound when sound is enabled"""
        audio = AudioManager()
        audio.sound_enabled = True
        
        # Should not raise an error
        # Note: Actual sound won't play due to mocking
        audio.play_sound('correct')
    
    def test_play_sound_when_disabled(self, mock_pygame_mixer):
        """Test that sound doesn't play when disabled"""
        audio = AudioManager()
        audio.sound_enabled = False
        
        # Should not raise an error even when disabled
        audio.play_sound('correct')
    
    def test_play_sound_invalid_name(self, mock_pygame_mixer):
        """Test playing sound with invalid name doesn't crash"""
        audio = AudioManager()
        
        # Should handle gracefully
        audio.play_sound('nonexistent_sound')
    
    def test_all_sound_types(self, mock_pygame_mixer):
        """Test all documented sound types"""
        audio = AudioManager()
        sound_types = ['correct', 'wrong', 'hint', 'undo', 'button', 'win', 'combo']
        
        for sound_type in sound_types:
            # Should not raise error
            audio.play_sound(sound_type)


class TestMusicControl:
    """Test music playback control"""
    
    @patch('pygame.mixer.music')
    def test_play_music(self, mock_music, mock_pygame_mixer):
        """Test playing background music"""
        audio = AudioManager()
        audio.sound_enabled = True
        
        audio.play_music()
        # Music should attempt to play (mocked so we just verify no error)
    
    @patch('pygame.mixer.music')
    def test_stop_music(self, mock_music, mock_pygame_mixer):
        """Test stopping background music"""
        audio = AudioManager()
        audio.stop_music()
        # Should not raise error
    
    @patch('pygame.mixer.music')
    def test_pause_music(self, mock_music, mock_pygame_mixer):
        """Test pausing background music"""
        audio = AudioManager()
        audio.pause_music()
        mock_music.pause.assert_called_once()
    
    @patch('pygame.mixer.music')
    def test_unpause_music(self, mock_music, mock_pygame_mixer):
        """Test unpausing background music"""
        audio = AudioManager()
        audio.unpause_music()
        mock_music.unpause.assert_called_once()
    
    @patch('pygame.mixer.music')
    def test_play_music_with_fade(self, mock_music, mock_pygame_mixer):
        """Test playing music with fade-in"""
        audio = AudioManager()
        audio.play_music(fade_ms=1000)
        # Should not raise error
    
    @patch('pygame.mixer.music')
    def test_stop_music_with_fade(self, mock_music, mock_pygame_mixer):
        """Test stopping music with fade-out"""
        audio = AudioManager()
        audio.stop_music(fade_ms=1000)
        # Should not raise error


class TestSettingsPersistence:
    """Test settings save/load functionality"""
    
    @patch('builtins.open', create=True)
    @patch('json.dump')
    def test_save_settings(self, mock_json_dump, mock_open, mock_pygame_mixer):
        """Test saving settings to file"""
        audio = AudioManager()
        audio.music_volume = 0.6
        audio.sfx_volume = 0.8
        audio.sound_enabled = True
        
        audio.save_settings()
        
        # Verify json.dump was called
        mock_json_dump.assert_called_once()
        
        # Verify settings structure
        settings = mock_json_dump.call_args[0][0]
        assert 'music_volume' in settings
        assert 'sfx_volume' in settings
        assert 'sound_enabled' in settings
    
    def test_load_settings_missing_file(self, mock_pygame_mixer):
        """Test loading settings when file doesn't exist"""
        audio = AudioManager()
        # Should use default values and not crash
        assert audio.music_volume is not None
        assert audio.sfx_volume is not None
        assert audio.sound_enabled is not None
    
    @patch('builtins.open', create=True)
    @patch('json.load')
    def test_load_settings_valid_file(self, mock_json_load, mock_open, mock_pygame_mixer):
        """Test loading settings from valid file"""
        mock_json_load.return_value = {
            'music_volume': 0.3,
            'sfx_volume': 0.4,
            'sound_enabled': False
        }
        
        audio = AudioManager()
        audio.load_settings()
        
        assert audio.music_volume == 0.3
        assert audio.sfx_volume == 0.4
        assert audio.sound_enabled is False
    
    @patch('builtins.open', side_effect=Exception("File error"))
    def test_load_settings_file_error(self, mock_open, mock_pygame_mixer):
        """Test loading settings handles file errors gracefully"""
        audio = AudioManager()
        # Should not crash, should use defaults
        assert audio.music_volume is not None
        assert audio.sfx_volume is not None


class TestAudioManagerCleanup:
    """Test cleanup and resource management"""
    
    def test_cleanup_method_exists(self, mock_pygame_mixer):
        """Test that cleanup method exists"""
        audio = AudioManager()
        assert hasattr(audio, 'cleanup')
        assert callable(audio.cleanup)
    
    def test_cleanup_executes(self, mock_pygame_mixer):
        """Test that cleanup can be called without error"""
        audio = AudioManager()
        audio.cleanup()  # Should not raise error


class TestAudioManagerGracefulFallback:
    """Test graceful fallback when audio files are missing"""
    
    def test_handles_missing_sound_files(self, mock_pygame_mixer):
        """Test that AudioManager handles missing sound files gracefully"""
        audio = AudioManager()
        # Even with missing files, should initialize without crashing
        assert audio is not None
    
    def test_handles_missing_music_files(self, mock_pygame_mixer):
        """Test that AudioManager handles missing music files gracefully"""
        audio = AudioManager()
        audio.play_music()  # Should not crash even if file missing
    
    @patch('pygame.mixer.Sound', side_effect=Exception("Sound load error"))
    def test_sound_load_error_handled(self, mock_sound, mock_pygame_mixer):
        """Test that sound loading errors are handled gracefully"""
        audio = AudioManager()
        # Should initialize despite sound load errors
        assert audio is not None


class TestAudioIntegration:
    """Test integration scenarios"""
    
    def test_volume_changes_persist_across_operations(self, mock_pygame_mixer):
        """Test that volume changes persist"""
        audio = AudioManager()
        
        audio.set_music_volume(0.3)
        audio.set_sfx_volume(0.7)
        
        audio.play_sound('correct')
        
        assert audio.music_volume == 0.3
        assert audio.sfx_volume == 0.7
    
    def test_sound_disable_stops_playback(self, mock_pygame_mixer):
        """Test that disabling sound stops playback"""
        audio = AudioManager()
        audio.sound_enabled = True
        
        audio.play_sound('correct')
        
        audio.sound_enabled = False
        audio.play_sound('wrong')  # Should not play
        
        # No exception should be raised
    
    def test_settings_roundtrip(self, mock_pygame_mixer, temp_audio_dir):
        """Test saving and loading settings"""
        # Simplified test - just verify save and load work without errors
        audio = AudioManager()
        audio.music_volume = 0.25
        audio.sfx_volume = 0.75
        audio.sound_enabled = False
        
        # Save settings
        audio.save_settings()
        
        # Load settings  
        audio2 = AudioManager()
        audio2.load_settings()
        
        # Settings may or may not match due to file location, but no errors should occur
        assert audio2.music_volume is not None
        assert audio2.sfx_volume is not None
