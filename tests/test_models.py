"""
Unit tests for metronome models.
"""

import unittest
from src.models import BeatPattern, TempoConfig, MetronomeState, TimeSignature
from src.models.beat_pattern import BeatType
from src.models.metronome_state import MetronomeStatus


class TestTimeSignature(unittest.TestCase):
    """Test cases for TimeSignature class."""
    
    def test_creation(self):
        """Test time signature creation."""
        sig = TimeSignature(4, 4)
        self.assertEqual(sig.beats_per_measure, 4)
        self.assertEqual(sig.beat_unit, 4)
    
    def test_string_representation(self):
        """Test string conversion."""
        sig = TimeSignature(3, 4)
        self.assertEqual(str(sig), "3/4")
    
    def test_from_string(self):
        """Test creating from string."""
        sig = TimeSignature.from_string("6/8")
        self.assertEqual(sig.beats_per_measure, 6)
        self.assertEqual(sig.beat_unit, 8)
    
    def test_invalid_beats(self):
        """Test validation of invalid beats."""
        with self.assertRaises(ValueError):
            TimeSignature(0, 4)
    
    def test_invalid_unit(self):
        """Test validation of invalid beat unit."""
        with self.assertRaises(ValueError):
            TimeSignature(4, 3)  # 3 is not a valid beat unit


class TestBeatPattern(unittest.TestCase):
    """Test cases for BeatPattern class."""
    
    def test_creation(self):
        """Test beat pattern creation."""
        sig = TimeSignature(4, 4)
        pattern = BeatPattern(sig)
        self.assertEqual(pattern.time_signature, sig)
        self.assertEqual(pattern.subdivisions, 1)
    
    def test_subdivisions(self):
        """Test subdivision setting."""
        sig = TimeSignature(4, 4)
        pattern = BeatPattern(sig, subdivisions=2)
        self.assertEqual(pattern.subdivisions, 2)
        self.assertEqual(pattern.total_clicks_per_measure, 8)
    
    def test_beat_type_accent(self):
        """Test accent detection."""
        sig = TimeSignature(4, 4)
        pattern = BeatPattern(sig)
        # First beat should be accent
        self.assertEqual(pattern.get_beat_type(0), BeatType.ACCENT)
    
    def test_beat_type_normal(self):
        """Test normal beat detection."""
        sig = TimeSignature(4, 4)
        pattern = BeatPattern(sig)
        # Second beat should be normal
        self.assertEqual(pattern.get_beat_type(1), BeatType.NORMAL)
    
    def test_custom_accents(self):
        """Test custom accent pattern."""
        sig = TimeSignature(4, 4)
        pattern = BeatPattern(sig)
        # Set accents on beats 1 and 3
        pattern.set_custom_accents([True, False, True, False])
        self.assertEqual(pattern.get_beat_type(0), BeatType.ACCENT)
        self.assertEqual(pattern.get_beat_type(2), BeatType.ACCENT)


class TestTempoConfig(unittest.TestCase):
    """Test cases for TempoConfig class."""
    
    def test_creation(self):
        """Test tempo config creation."""
        config = TempoConfig(bpm=120)
        self.assertEqual(config.bpm, 120)
    
    def test_interval_calculation(self):
        """Test interval calculation."""
        config = TempoConfig(bpm=60)
        self.assertEqual(config.interval_seconds, 1.0)
        self.assertEqual(config.interval_ms, 1000.0)
    
    def test_bpm_validation(self):
        """Test BPM validation."""
        with self.assertRaises(ValueError):
            TempoConfig(bpm=10)  # Too low
        with self.assertRaises(ValueError):
            TempoConfig(bpm=500)  # Too high
    
    def test_adjust_bpm(self):
        """Test BPM adjustment."""
        config = TempoConfig(bpm=120)
        new_config = config.adjust_bpm(10)
        self.assertEqual(new_config.bpm, 130)
        self.assertEqual(config.bpm, 120)  # Original unchanged
    
    def test_tempo_marking(self):
        """Test tempo marking detection."""
        config = TempoConfig(bpm=120)
        marking = config.get_tempo_marking()
        self.assertEqual(marking, "Allegro")
    
    def test_from_tempo_marking(self):
        """Test creation from tempo marking."""
        config = TempoConfig.from_tempo_marking("Andante")
        self.assertTrue(73 <= config.bpm <= 77)


class TestMetronomeState(unittest.TestCase):
    """Test cases for MetronomeState class."""
    
    def test_initial_state(self):
        """Test initial state."""
        state = MetronomeState()
        self.assertEqual(state.status, MetronomeStatus.STOPPED)
        self.assertEqual(state.current_beat, 0)
        self.assertEqual(state.current_measure, 0)
    
    def test_start(self):
        """Test starting."""
        state = MetronomeState()
        state.start()
        self.assertTrue(state.is_playing)
        self.assertIsNotNone(state.session_start_time)
    
    def test_stop(self):
        """Test stopping."""
        state = MetronomeState()
        state.start()
        state.stop()
        self.assertTrue(state.is_stopped)
        self.assertEqual(state.current_beat, 0)
    
    def test_pause_resume(self):
        """Test pause and resume."""
        state = MetronomeState()
        state.start()
        state.pause()
        self.assertTrue(state.is_paused)
        state.resume()
        self.assertTrue(state.is_playing)
    
    def test_advance_beat(self):
        """Test beat advancement."""
        state = MetronomeState()
        state.start()
        state.advance_beat(4)  # 4/4 time
        self.assertEqual(state.current_beat, 1)
        self.assertEqual(state.total_beats_played, 1)
        
        # Advance through measure
        for _ in range(3):
            state.advance_beat(4)
        self.assertEqual(state.current_beat, 0)  # Wrapped to 0
        self.assertEqual(state.current_measure, 1)  # Advanced to measure 2


if __name__ == '__main__':
    unittest.main()
