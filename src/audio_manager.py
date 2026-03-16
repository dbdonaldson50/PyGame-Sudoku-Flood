#!/usr/bin/env python3
"""
Audio Manager for Sudoku Flash
Handles background music and sound effects with volume control
Author: Red Donaldson
Date: March 16, 2026
"""

import pygame
import os
import json


class AudioManager:
    """Manages all audio playback for the game"""
    
    def __init__(self):
        """Initialize the audio system"""
        # Initialize pygame mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Volume settings (0.0 to 1.0)
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.sound_enabled = True
        
        # Sound effect channels
        self.sfx_channels = {}
        
        # Load settings
        self.load_settings()
        
        # Paths
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        self.sounds_dir = os.path.join(self.assets_dir, 'sounds')
        self.music_dir = os.path.join(self.assets_dir, 'music')
        
        # Sound effects dictionary
        self.sounds = {}
        
        # Music state
        self.current_music = None
        self.music_loaded = False
        
        # Load all audio assets
        self.load_sounds()
        self.load_music()
        
        # Apply volume settings
        self.update_volumes()
    
    def load_sounds(self):
        """Load all sound effects"""
        sound_files = {
            'correct': 'correct.wav',
            'wrong': 'wrong.wav',
            'hint': 'hint.wav',
            'undo': 'undo.wav',
            'button': 'button.wav',
            'win': 'win.wav',
            'combo': 'combo.wav'
        }
        
        for sound_name, filename in sound_files.items():
            filepath = os.path.join(self.sounds_dir, filename)
            if os.path.exists(filepath):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                except pygame.error as e:
                    print(f"Warning: Could not load sound {filename}: {e}")
            else:
                print(f"Warning: Sound file not found: {filepath}")
    
    def load_music(self):
        """Load background music"""
        music_file = os.path.join(self.music_dir, 'background.ogg')
        if os.path.exists(music_file):
            try:
                pygame.mixer.music.load(music_file)
                self.music_loaded = True
                self.current_music = 'background'
            except pygame.error as e:
                print(f"Warning: Could not load music: {e}")
                self.music_loaded = False
        else:
            print(f"Warning: Music file not found: {music_file}")
            self.music_loaded = False
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if not self.sound_enabled:
            return
        
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].set_volume(self.sfx_volume)
                self.sounds[sound_name].play()
            except pygame.error as e:
                print(f"Warning: Could not play sound {sound_name}: {e}")
    
    def play_music(self, fade_ms=1000):
        """Start playing background music with fade in"""
        if not self.sound_enabled or not self.music_loaded:
            return
        
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1, fade_ms=fade_ms)  # Loop indefinitely
                pygame.mixer.music.set_volume(self.music_volume)
        except pygame.error as e:
            print(f"Warning: Could not play music: {e}")
    
    def stop_music(self, fade_ms=1000):
        """Stop background music with fade out"""
        if pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.fadeout(fade_ms)
            except pygame.error as e:
                print(f"Warning: Could not stop music: {e}")
    
    def pause_music(self):
        """Pause background music"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Resume background music"""
        pygame.mixer.music.unpause()
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        self.save_settings()
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        # Update all loaded sounds
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
        self.save_settings()
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.play_music(fade_ms=500)
        else:
            self.stop_music(fade_ms=500)
        self.save_settings()
        return self.sound_enabled
    
    def update_volumes(self):
        """Apply current volume settings to all audio"""
        pygame.mixer.music.set_volume(self.music_volume)
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def save_settings(self):
        """Save audio settings to file"""
        settings = {
            'music_volume': self.music_volume,
            'sfx_volume': self.sfx_volume,
            'sound_enabled': self.sound_enabled
        }
        
        try:
            settings_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'audio_settings.json')
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save audio settings: {e}")
    
    def load_settings(self):
        """Load audio settings from file"""
        try:
            settings_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'audio_settings.json')
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    self.music_volume = settings.get('music_volume', 0.5)
                    self.sfx_volume = settings.get('sfx_volume', 0.7)
                    self.sound_enabled = settings.get('sound_enabled', True)
        except Exception as e:
            print(f"Warning: Could not load audio settings: {e}")
            # Use defaults
            self.music_volume = 0.5
            self.sfx_volume = 0.7
            self.sound_enabled = True
    
    def cleanup(self):
        """Clean up audio resources"""
        pygame.mixer.music.stop()
        pygame.mixer.quit()
