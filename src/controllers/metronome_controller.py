"""
Main controller for coordinating metronome functionality.

This controller acts as a facade, coordinating between the engine,
audio service, and UI components.
"""

import logging
from typing import Optional, Callable
from pathlib import Path

from ..models import BeatPattern, TempoConfig, MetronomeState, TimeSignature
from ..services import MetronomeEngine, AudioService, IAudioProvider, PygameAudioProvider
from ..services.audio_service import SoundType

logger = logging.getLogger(__name__)


class MetronomeController:
    """
    Main controller for the metronome application.
    
    This class provides a high-level API for controlling the metronome,
    managing configuration, and coordinating between components.
    It follows the Facade pattern to simplify interaction with the system.
    """
    
    def __init__(
        self,
        audio_provider: Optional[IAudioProvider] = None,
        sounds_dir: Optional[Path] = None
    ):
        """
        Initialize the metronome controller.
        
        Args:
            audio_provider: Audio provider implementation (defaults to Pygame)
            sounds_dir: Directory containing sound files
        """
        # Initialize audio service
        provider = audio_provider or PygameAudioProvider()
        self._audio_service = AudioService(provider, sounds_dir)
        
        # Initialize with defaults
        self._tempo_config = TempoConfig(bpm=TempoConfig.DEFAULT_BPM)
        self._beat_pattern = BeatPattern(BeatPattern.COMMON_SIGNATURES['4/4'])
        
        # Initialize engine
        self._engine = MetronomeEngine(
            self._audio_service,
            self._tempo_config,
            self._beat_pattern
        )
        
        self._initialized = False
    
    # ========== Initialization ==========
    
    def initialize(self) -> bool:
        """
        Initialize the controller and all services.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        if self._initialized:
            logger.warning("Controller already initialized")
            return True
        
        if not self._audio_service.initialize():
            logger.error("Failed to initialize audio service")
            return False
        
        self._initialized = True
        logger.info("Metronome controller initialized successfully")
        return True
    
    # ========== Playback Control ==========
    
    def start(self):
        """Start the metronome."""
        if not self._initialized:
            raise RuntimeError("Controller not initialized. Call initialize() first.")
        self._engine.start()
    
    def stop(self):
        """Stop the metronome."""
        self._engine.stop()
    
    def pause(self):
        """Pause the metronome."""
        self._engine.pause()
    
    def toggle_playback(self):
        """Toggle between play and pause."""
        if self._engine.state.is_playing:
            self.pause()
        elif self._engine.state.is_paused:
            self.start()
        else:
            self.start()
    
    # ========== Tempo Control ==========
    
    def set_bpm(self, bpm: int):
        """
        Set the tempo in beats per minute.
        
        Args:
            bpm: Beats per minute
            
        Raises:
            ValueError: If BPM is out of valid range
        """
        tempo_config = TempoConfig(bpm=bpm)
        self._tempo_config = tempo_config
        self._engine.tempo_config = tempo_config
        logger.info(f"BPM set to {bpm}")
    
    def get_bpm(self) -> int:
        """Get the current BPM."""
        return self._tempo_config.bpm
    
    def increase_bpm(self, delta: int = 1):
        """
        Increase the BPM by a specified amount.
        
        Args:
            delta: Amount to increase (default 1)
        """
        new_config = self._tempo_config.adjust_bpm(delta)
        self.set_bpm(new_config.bpm)
    
    def decrease_bpm(self, delta: int = 1):
        """
        Decrease the BPM by a specified amount.
        
        Args:
            delta: Amount to decrease (default 1)
        """
        new_config = self._tempo_config.adjust_bpm(-delta)
        self.set_bpm(new_config.bpm)
    
    def set_tempo_marking(self, marking: str):
        """
        Set tempo using an Italian tempo marking.
        
        Args:
            marking: Tempo marking (e.g., "Allegro", "Andante")
            
        Raises:
            ValueError: If marking is not recognized
        """
        tempo_config = TempoConfig.from_tempo_marking(marking)
        self._tempo_config = tempo_config
        self._engine.tempo_config = tempo_config
        logger.info(f"Tempo set to {marking} ({tempo_config.bpm} BPM)")
    
    def tap_tempo(self):
        """
        Record a tap for tap tempo calculation.
        
        Call this method multiple times to calculate BPM from tapping.
        """
        calculated_bpm = self._engine.tap_tempo()
        if calculated_bpm:
            self._tempo_config = TempoConfig(bpm=calculated_bpm)
            logger.info(f"Tap tempo: {calculated_bpm} BPM")
    
    def get_tempo_info(self) -> str:
        """
        Get formatted tempo information.
        
        Returns:
            String with BPM and tempo marking
        """
        return str(self._tempo_config)
    
    # ========== Time Signature Control ==========
    
    def set_time_signature(self, signature: str):
        """
        Set the time signature.
        
        Args:
            signature: Time signature in format "4/4", "3/4", etc.
            
        Raises:
            ValueError: If signature format is invalid
        """
        time_sig = TimeSignature.from_string(signature)
        self._beat_pattern = BeatPattern(time_sig, self._beat_pattern.subdivisions)
        self._engine.beat_pattern = self._beat_pattern
        logger.info(f"Time signature set to {signature}")
    
    def get_time_signature(self) -> str:
        """Get the current time signature as a string."""
        return str(self._beat_pattern.time_signature)
    
    def set_subdivisions(self, subdivisions: int):
        """
        Set the number of subdivisions per beat.
        
        Args:
            subdivisions: Number of subdivisions (1-4)
            
        Raises:
            ValueError: If subdivisions value is invalid
        """
        self._beat_pattern.subdivisions = subdivisions
        self._engine.beat_pattern = self._beat_pattern
        logger.info(f"Subdivisions set to {subdivisions}")
    
    def get_subdivisions(self) -> int:
        """Get the current number of subdivisions."""
        return self._beat_pattern.subdivisions
    
    def set_custom_accents(self, accent_pattern: list):
        """
        Set a custom accent pattern.
        
        Args:
            accent_pattern: List of booleans for each beat
            
        Raises:
            ValueError: If pattern length is invalid
        """
        self._beat_pattern.set_custom_accents(accent_pattern)
        self._engine.beat_pattern = self._beat_pattern
        logger.info(f"Custom accent pattern set: {accent_pattern}")
    
    # ========== Audio Control ==========
    
    def set_volume(self, volume: float):
        """
        Set the playback volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self._audio_service.set_volume(volume)
    
    def get_volume(self) -> float:
        """Get the current volume level."""
        return self._audio_service.get_volume()
    
    def toggle_mute(self):
        """Toggle mute on/off."""
        self._audio_service.toggle_mute()
    
    def is_muted(self) -> bool:
        """Check if audio is muted."""
        return self._audio_service.is_muted()
    
    # ========== State Information ==========
    
    def get_state(self) -> MetronomeState:
        """Get the current metronome state."""
        return self._engine.state
    
    def is_playing(self) -> bool:
        """Check if metronome is currently playing."""
        return self._engine.state.is_playing
    
    def is_stopped(self) -> bool:
        """Check if metronome is stopped."""
        return self._engine.state.is_stopped
    
    def is_paused(self) -> bool:
        """Check if metronome is paused."""
        return self._engine.state.is_paused
    
    def get_current_beat(self) -> int:
        """Get the current beat number (0-indexed)."""
        return self._engine.state.current_beat
    
    def get_current_measure(self) -> int:
        """Get the current measure number."""
        return self._engine.state.current_measure
    
    # ========== Callbacks ==========
    
    def add_beat_callback(self, callback: Callable[[int, SoundType], None]):
        """
        Register a callback to be called on each beat.
        
        Args:
            callback: Function(beat_number, sound_type)
        """
        self._engine.add_beat_callback(callback)
    
    def remove_beat_callback(self, callback: Callable[[int, SoundType], None]):
        """Unregister a beat callback."""
        self._engine.remove_beat_callback(callback)
    
    def add_state_callback(self, callback: Callable[[MetronomeState], None]):
        """
        Register a callback to be called on state changes.
        
        Args:
            callback: Function(state)
        """
        self._engine.add_state_callback(callback)
    
    def remove_state_callback(self, callback: Callable[[MetronomeState], None]):
        """Unregister a state callback."""
        self._engine.remove_state_callback(callback)
    
    # ========== Configuration Presets ==========
    
    def get_common_time_signatures(self) -> list:
        """Get list of common time signatures."""
        return list(BeatPattern.COMMON_SIGNATURES.keys())
    
    def get_tempo_markings(self) -> list:
        """Get list of available tempo markings."""
        return list(TempoConfig.TEMPO_MARKINGS.keys())
    
    # ========== Cleanup ==========
    
    def cleanup(self):
        """Clean up all resources."""
        self._engine.cleanup()
        self._audio_service.cleanup()
        self._initialized = False
        logger.info("Metronome controller cleaned up")
    
    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
