"""
Metronome state model for tracking runtime state.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


class MetronomeStatus(Enum):
    """Enumeration of metronome states."""
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


@dataclass
class MetronomeState:
    """
    Represents the current state of the metronome.
    
    This class tracks runtime information including playback status,
    current position, and statistics.
    """
    
    status: MetronomeStatus = MetronomeStatus.STOPPED
    current_beat: int = 0
    current_measure: int = 0
    total_beats_played: int = 0
    session_start_time: Optional[datetime] = None
    last_beat_time: Optional[datetime] = None
    
    def start(self):
        """Start the metronome session."""
        self.status = MetronomeStatus.PLAYING
        if self.session_start_time is None:
            self.session_start_time = datetime.now()
        self.last_beat_time = datetime.now()
    
    def stop(self):
        """Stop the metronome and reset position."""
        self.status = MetronomeStatus.STOPPED
        self.current_beat = 0
        self.current_measure = 0
        self.session_start_time = None
        self.last_beat_time = None
    
    def pause(self):
        """Pause the metronome without resetting position."""
        if self.status == MetronomeStatus.PLAYING:
            self.status = MetronomeStatus.PAUSED
    
    def resume(self):
        """Resume from paused state."""
        if self.status == MetronomeStatus.PAUSED:
            self.status = MetronomeStatus.PLAYING
            self.last_beat_time = datetime.now()
    
    def advance_beat(self, beats_per_measure: int):
        """
        Advance to the next beat.
        
        Args:
            beats_per_measure: Number of beats in a measure
        """
        self.current_beat = (self.current_beat + 1) % beats_per_measure
        if self.current_beat == 0:
            self.current_measure += 1
        self.total_beats_played += 1
        self.last_beat_time = datetime.now()
    
    def reset_position(self):
        """Reset beat and measure counters without stopping."""
        self.current_beat = 0
        self.current_measure = 0
    
    @property
    def is_playing(self) -> bool:
        """Check if metronome is currently playing."""
        return self.status == MetronomeStatus.PLAYING
    
    @property
    def is_stopped(self) -> bool:
        """Check if metronome is stopped."""
        return self.status == MetronomeStatus.STOPPED
    
    @property
    def is_paused(self) -> bool:
        """Check if metronome is paused."""
        return self.status == MetronomeStatus.PAUSED
    
    @property
    def session_duration(self) -> Optional[float]:
        """
        Get the duration of the current session in seconds.
        
        Returns:
            Duration in seconds, or None if no session is active
        """
        if self.session_start_time is None:
            return None
        return (datetime.now() - self.session_start_time).total_seconds()
    
    def __repr__(self) -> str:
        return (f"MetronomeState(status={self.status.value}, "
                f"beat={self.current_beat}, measure={self.current_measure})")
