"""
Unit tests for audio service.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

from src.services.audio_service import (
    AudioService,
    IAudioProvider,
    PygameAudioProvider,
    SoundType
)


class MockAudioProvider(IAudioProvider):
    """Mock audio provider for testing."""
    
    def __init__(self):
        self.initialized = False
        self.sounds = {}
        self.volume = 1.0
        self.play_count = 0
    
    def initialize(self) -> bool:
        self.initialized = True
        return True
    
    def load_sound(self, sound_path: Path):
        sound = Mock()
        self.sounds[str(sound_path)] = sound
        return sound
    
    def play_sound(self, sound) -> bool:
        self.play_count += 1
        return True
    
    def set_volume(self, volume: float):
        self.volume = volume
    
    def cleanup(self):
        self.initialized = False
        self.sounds.clear()


class TestAudioService(unittest.TestCase):
    """Test cases for AudioService class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.provider = MockAudioProvider()
        self.service = AudioService(self.provider)
    
    def test_initialization(self):
        """Test service initialization."""
        result = self.service.initialize()
        self.assertTrue(result)
        self.assertTrue(self.provider.initialized)
    
    def test_volume_control(self):
        """Test volume setting."""
        self.service.initialize()
        self.service.set_volume(0.5)
        self.assertEqual(self.service.get_volume(), 0.5)
        self.assertEqual(self.provider.volume, 0.5)
    
    def test_mute_unmute(self):
        """Test mute functionality."""
        self.service.initialize()
        self.assertFalse(self.service.is_muted())
        
        self.service.mute()
        self.assertTrue(self.service.is_muted())
        
        self.service.unmute()
        self.assertFalse(self.service.is_muted())
    
    def test_toggle_mute(self):
        """Test mute toggle."""
        self.service.initialize()
        self.service.toggle_mute()
        self.assertTrue(self.service.is_muted())
        self.service.toggle_mute()
        self.assertFalse(self.service.is_muted())
    
    def test_cleanup(self):
        """Test cleanup."""
        self.service.initialize()
        self.service.cleanup()
        self.assertFalse(self.provider.initialized)


class TestPygameAudioProvider(unittest.TestCase):
    """Test cases for PygameAudioProvider class."""
    
    @patch('src.services.audio_service.pygame')
    def test_initialization(self, mock_pygame):
        """Test pygame provider initialization."""
        provider = PygameAudioProvider()
        result = provider.initialize()
        self.assertTrue(result)
        mock_pygame.mixer.init.assert_called_once()
    
    @patch('src.services.audio_service.pygame')
    def test_initialization_failure(self, mock_pygame):
        """Test initialization failure handling."""
        mock_pygame.mixer.init.side_effect = Exception("Init failed")
        provider = PygameAudioProvider()
        result = provider.initialize()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
