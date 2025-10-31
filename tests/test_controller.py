"""
Unit tests for metronome controller.
"""

import unittest
from unittest.mock import Mock, MagicMock

from src.controllers import MetronomeController
from src.services.audio_service import MockAudioProvider
from src.models import TempoConfig, TimeSignature


# Reuse MockAudioProvider from test_audio_service
class MockAudioProvider:
    """Mock audio provider for testing."""
    
    def initialize(self):
        return True
    
    def load_sound(self, path):
        return Mock()
    
    def play_sound(self, sound):
        return True
    
    def set_volume(self, volume):
        pass
    
    def cleanup(self):
        pass


class TestMetronomeController(unittest.TestCase):
    """Test cases for MetronomeController class."""
    
    def setUp(self):
        """Set up test fixtures."""
        provider = MockAudioProvider()
        self.controller = MetronomeController(audio_provider=provider)
        self.controller.initialize()
    
    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'controller'):
            self.controller.cleanup()
    
    def test_initialization(self):
        """Test controller initialization."""
        self.assertTrue(self.controller._initialized)
    
    def test_bpm_control(self):
        """Test BPM setting and getting."""
        self.controller.set_bpm(140)
        self.assertEqual(self.controller.get_bpm(), 140)
    
    def test_bpm_bounds(self):
        """Test BPM boundary validation."""
        with self.assertRaises(ValueError):
            self.controller.set_bpm(10)  # Too low
        with self.assertRaises(ValueError):
            self.controller.set_bpm(500)  # Too high
    
    def test_increase_decrease_bpm(self):
        """Test BPM increment/decrement."""
        initial_bpm = self.controller.get_bpm()
        self.controller.increase_bpm(10)
        self.assertEqual(self.controller.get_bpm(), initial_bpm + 10)
        
        self.controller.decrease_bpm(5)
        self.assertEqual(self.controller.get_bpm(), initial_bpm + 5)
    
    def test_time_signature(self):
        """Test time signature setting."""
        self.controller.set_time_signature("3/4")
        self.assertEqual(self.controller.get_time_signature(), "3/4")
    
    def test_subdivisions(self):
        """Test subdivision setting."""
        self.controller.set_subdivisions(2)
        self.assertEqual(self.controller.get_subdivisions(), 2)
    
    def test_volume_control(self):
        """Test volume control."""
        self.controller.set_volume(0.7)
        self.assertEqual(self.controller.get_volume(), 0.7)
    
    def test_playback_states(self):
        """Test playback state queries."""
        # Initial state should be stopped
        self.assertTrue(self.controller.is_stopped())
        self.assertFalse(self.controller.is_playing())
        self.assertFalse(self.controller.is_paused())
    
    def test_callbacks(self):
        """Test callback registration."""
        beat_callback = Mock()
        state_callback = Mock()
        
        self.controller.add_beat_callback(beat_callback)
        self.controller.add_state_callback(state_callback)
        
        # Callbacks should be registered
        self.assertIn(beat_callback, self.controller._engine._beat_callbacks)
        self.assertIn(state_callback, self.controller._engine._state_callbacks)
        
        # Remove callbacks
        self.controller.remove_beat_callback(beat_callback)
        self.controller.remove_state_callback(state_callback)
        
        self.assertNotIn(beat_callback, self.controller._engine._beat_callbacks)
        self.assertNotIn(state_callback, self.controller._engine._state_callbacks)
    
    def test_common_signatures(self):
        """Test getting common time signatures."""
        signatures = self.controller.get_common_time_signatures()
        self.assertIn('4/4', signatures)
        self.assertIn('3/4', signatures)
        self.assertIn('6/8', signatures)
    
    def test_tempo_markings(self):
        """Test getting tempo markings."""
        markings = self.controller.get_tempo_markings()
        self.assertIn('Allegro', markings)
        self.assertIn('Andante', markings)
    
    def test_context_manager(self):
        """Test using controller as context manager."""
        provider = MockAudioProvider()
        with MetronomeController(audio_provider=provider) as controller:
            self.assertTrue(controller._initialized)
        # Should be cleaned up after context
        self.assertFalse(controller._initialized)


if __name__ == '__main__':
    unittest.main()
