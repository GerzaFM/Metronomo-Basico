"""
Metronome engine - core timing and coordination service.

This module implements the main business logic for the metronome,
coordinating timing, beat patterns, and audio playback.
"""

import threading
import time
import logging
from typing import Optional, Callable, List
from datetime import datetime

from ..models import BeatPattern, TempoConfig, MetronomeState
from .audio_service import AudioService, SoundType

logger = logging.getLogger(__name__)


class MetronomeEngine:
    """
    Core metronome engine responsible for timing and coordination.
    
    This class manages the metronome's timing loop, coordinates
    beat patterns with audio playback, and provides callbacks
    for UI updates.
    """
    
    def __init__(
        self,
        audio_service: AudioService,
        tempo_config: Optional[TempoConfig] = None,
        beat_pattern: Optional[BeatPattern] = None
    ):
        """
        Initialize the metronome engine.
        
        Args:
            audio_service: Service for audio playback
            tempo_config: Initial tempo configuration
            beat_pattern: Initial beat pattern
        """
        self._audio_service = audio_service
        self._tempo_config = tempo_config or TempoConfig(bpm=TempoConfig.DEFAULT_BPM)
        self._beat_pattern = beat_pattern or BeatPattern(
            BeatPattern.COMMON_SIGNATURES['4/4']
        )
        self._state = MetronomeState()
        
        # Threading for metronome loop
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._lock = threading.RLock()
        
        # Callbacks for UI updates
        self._beat_callbacks: List[Callable[[int, SoundType], None]] = []
        self._state_callbacks: List[Callable[[MetronomeState], None]] = []
        
        # Performance tracking
        self._timing_error_threshold = 0.005  # 5ms
        self._last_timing_error = 0.0
    
    # ========== Property Accessors ==========
    
    @property
    def tempo_config(self) -> TempoConfig:
        """Get current tempo configuration."""
        with self._lock:
            return self._tempo_config
    
    @tempo_config.setter
    def tempo_config(self, config: TempoConfig):
        """Set tempo configuration."""
        with self._lock:
            self._tempo_config = config
            logger.info(f"Tempo changed to {config}")
    
    @property
    def beat_pattern(self) -> BeatPattern:
        """Get current beat pattern."""
        with self._lock:
            return self._beat_pattern
    
    @beat_pattern.setter
    def beat_pattern(self, pattern: BeatPattern):
        """Set beat pattern."""
        with self._lock:
            self._beat_pattern = pattern
            self._state.reset_position()
            logger.info(f"Beat pattern changed to {pattern}")
    
    @property
    def state(self) -> MetronomeState:
        """Get current metronome state."""
        with self._lock:
            return self._state
    
    # ========== Callback Management ==========
    
    def add_beat_callback(self, callback: Callable[[int, SoundType], None]):
        """
        Add a callback to be called on each beat.
        
        Args:
            callback: Function that takes beat_number and sound_type
        """
        with self._lock:
            if callback not in self._beat_callbacks:
                self._beat_callbacks.append(callback)
    
    def remove_beat_callback(self, callback: Callable[[int, SoundType], None]):
        """Remove a beat callback."""
        with self._lock:
            if callback in self._beat_callbacks:
                self._beat_callbacks.remove(callback)
    
    def add_state_callback(self, callback: Callable[[MetronomeState], None]):
        """
        Add a callback to be called on state changes.
        
        Args:
            callback: Function that takes MetronomeState
        """
        with self._lock:
            if callback not in self._state_callbacks:
                self._state_callbacks.append(callback)
    
    def remove_state_callback(self, callback: Callable[[MetronomeState], None]):
        """Remove a state callback."""
        with self._lock:
            if callback in self._state_callbacks:
                self._state_callbacks.remove(callback)
    
    # ========== Metronome Control ==========
    
    def start(self):
        """Start the metronome."""
        with self._lock:
            if self._state.is_playing:
                logger.warning("Metronome already playing")
                return
            
            if self._state.is_paused:
                self._state.resume()
                logger.info("Metronome resumed")
            else:
                self._state.start()
                logger.info("Metronome started")
            
            # Start timing thread
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._timing_loop, daemon=True)
            self._thread.start()
            
            self._notify_state_change()
    
    def stop(self):
        """Stop the metronome."""
        with self._lock:
            if self._state.is_stopped:
                logger.warning("Metronome already stopped")
                return
            
            # Signal thread to stop
            self._stop_event.set()
            
            # Wait for thread to finish
            if self._thread and self._thread.is_alive():
                self._lock.release()  # Release lock while waiting
                self._thread.join(timeout=1.0)
                self._lock.acquire()
            
            self._state.stop()
            logger.info("Metronome stopped")
            self._notify_state_change()
    
    def pause(self):
        """Pause the metronome."""
        with self._lock:
            if not self._state.is_playing:
                logger.warning("Cannot pause - metronome not playing")
                return
            
            self._stop_event.set()
            
            if self._thread and self._thread.is_alive():
                self._lock.release()
                self._thread.join(timeout=1.0)
                self._lock.acquire()
            
            self._state.pause()
            logger.info("Metronome paused")
            self._notify_state_change()
    
    def tap_tempo(self, tap_time: Optional[datetime] = None) -> Optional[int]:
        """
        Calculate BPM from tap tempo input.
        
        This method should be called multiple times (at least 2) to calculate tempo.
        
        Args:
            tap_time: Time of tap (defaults to now)
            
        Returns:
            Calculated BPM if enough taps, None otherwise
        """
        # This is a simplified implementation
        # A production version would maintain a buffer of recent taps
        tap_time = tap_time or datetime.now()
        
        with self._lock:
            if self._state.last_beat_time is None:
                self._state.last_beat_time = tap_time
                return None
            
            # Calculate interval between taps
            interval = (tap_time - self._state.last_beat_time).total_seconds()
            self._state.last_beat_time = tap_time
            
            if interval > 0:
                bpm = int(60.0 / interval)
                if TempoConfig.MIN_BPM <= bpm <= TempoConfig.MAX_BPM:
                    self._tempo_config = TempoConfig(bpm=bpm)
                    logger.info(f"Tap tempo calculated: {bpm} BPM")
                    return bpm
        
        return None
    
    # ========== Internal Timing Loop ==========
    
    def _timing_loop(self):
        """
        Main timing loop running in separate thread.
        
        This uses a compensating timer to maintain accurate timing
        even with processing delays.
        """
        next_beat_time = time.perf_counter()
        
        while not self._stop_event.is_set():
            current_time = time.perf_counter()
            
            # Calculate when next beat should occur
            interval = self._tempo_config.interval_seconds
            next_beat_time += interval
            
            # If we're behind schedule, resync
            if next_beat_time < current_time:
                self._last_timing_error = current_time - next_beat_time
                if self._last_timing_error > self._timing_error_threshold:
                    logger.warning(
                        f"Timing drift detected: {self._last_timing_error*1000:.2f}ms"
                    )
                next_beat_time = current_time + interval
            
            # Process the beat
            self._process_beat()
            
            # Sleep until next beat (with high precision)
            sleep_time = next_beat_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    def _process_beat(self):
        """Process a single beat - play sound and update state."""
        with self._lock:
            # Get current beat information
            beat_num = self._state.current_beat
            click_in_measure = beat_num * self._beat_pattern.subdivisions
            
            # Determine sound type
            beat_type = self._beat_pattern.get_beat_type(click_in_measure)
            sound_type = self._map_beat_to_sound(beat_type)
            
            # Play sound
            self._audio_service.play_sound(sound_type)
            
            # Update state
            self._state.advance_beat(self._beat_pattern.time_signature.beats_per_measure)
            
            # Notify callbacks
            self._notify_beat(beat_num, sound_type)
    
    def _map_beat_to_sound(self, beat_type) -> SoundType:
        """Map BeatType to SoundType for audio playback."""
        from ..models.beat_pattern import BeatType
        
        mapping = {
            BeatType.ACCENT: SoundType.ACCENT,
            BeatType.NORMAL: SoundType.NORMAL,
            BeatType.SUBDIVISION: SoundType.SUBDIVISION,
        }
        return mapping.get(beat_type, SoundType.NORMAL)
    
    def _notify_beat(self, beat_number: int, sound_type: SoundType):
        """Notify all beat callbacks."""
        for callback in self._beat_callbacks[:]:  # Copy to avoid modification during iteration
            try:
                callback(beat_number, sound_type)
            except Exception as e:
                logger.error(f"Error in beat callback: {e}")
    
    def _notify_state_change(self):
        """Notify all state callbacks."""
        for callback in self._state_callbacks[:]:
            try:
                callback(self._state)
            except Exception as e:
                logger.error(f"Error in state callback: {e}")
    
    # ========== Cleanup ==========
    
    def cleanup(self):
        """Clean up resources."""
        self.stop()
        self._beat_callbacks.clear()
        self._state_callbacks.clear()
        logger.info("Metronome engine cleaned up")
