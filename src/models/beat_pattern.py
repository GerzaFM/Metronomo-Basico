"""
Beat pattern model for managing time signatures and beat structures.
"""

from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum


class BeatType(Enum):
    """Enumeration of beat types."""
    ACCENT = "accent"      # First beat (strong)
    NORMAL = "normal"      # Regular beat
    SUBDIVISION = "subdivision"  # Sub-beat (eighth notes, etc.)


@dataclass(frozen=True)
class TimeSignature:
    """
    Represents a musical time signature.
    
    Attributes:
        beats_per_measure: Number of beats in a measure (numerator)
        beat_unit: Note value that gets one beat (denominator)
    """
    beats_per_measure: int
    beat_unit: int
    
    def __post_init__(self):
        """Validate time signature values."""
        if self.beats_per_measure < 1:
            raise ValueError("beats_per_measure must be at least 1")
        if self.beat_unit not in [1, 2, 4, 8, 16]:
            raise ValueError("beat_unit must be 1, 2, 4, 8, or 16")
    
    def __str__(self) -> str:
        return f"{self.beats_per_measure}/{self.beat_unit}"
    
    @classmethod
    def from_string(cls, signature: str) -> 'TimeSignature':
        """
        Create TimeSignature from string representation.
        
        Args:
            signature: String in format "4/4", "3/4", etc.
            
        Returns:
            TimeSignature instance
            
        Raises:
            ValueError: If signature format is invalid
        """
        try:
            beats, unit = signature.split('/')
            return cls(int(beats), int(unit))
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Invalid time signature format: {signature}") from e


class BeatPattern:
    """
    Manages the pattern of beats within a measure.
    
    This class determines which beats are accented and handles
    subdivision of beats.
    """
    
    # Common time signatures
    COMMON_SIGNATURES = {
        '4/4': TimeSignature(4, 4),
        '3/4': TimeSignature(3, 4),
        '6/8': TimeSignature(6, 8),
        '2/4': TimeSignature(2, 4),
        '5/4': TimeSignature(5, 4),
        '7/8': TimeSignature(7, 8),
        '12/8': TimeSignature(12, 8),
    }
    
    def __init__(self, time_signature: TimeSignature, subdivisions: int = 1):
        """
        Initialize beat pattern.
        
        Args:
            time_signature: The time signature for this pattern
            subdivisions: Number of subdivisions per beat (1 = quarter notes only,
                         2 = eighth notes, 4 = sixteenth notes)
        """
        self._time_signature = time_signature
        self._subdivisions = subdivisions
        self._accent_pattern = self._generate_default_accents()
    
    @property
    def time_signature(self) -> TimeSignature:
        """Get the time signature."""
        return self._time_signature
    
    @property
    def subdivisions(self) -> int:
        """Get the number of subdivisions per beat."""
        return self._subdivisions
    
    @subdivisions.setter
    def subdivisions(self, value: int):
        """Set the number of subdivisions per beat."""
        if value < 1 or value > 4:
            raise ValueError("Subdivisions must be between 1 and 4")
        self._subdivisions = value
    
    @property
    def total_clicks_per_measure(self) -> int:
        """Calculate total number of clicks in one measure."""
        return self._time_signature.beats_per_measure * self._subdivisions
    
    def _generate_default_accents(self) -> List[bool]:
        """
        Generate default accent pattern based on time signature.
        
        Returns:
            List of booleans indicating which beats are accented
        """
        beats = self._time_signature.beats_per_measure
        
        # First beat is always accented
        pattern = [True] + [False] * (beats - 1)
        
        # Special patterns for compound time signatures
        if self._time_signature.beat_unit == 8 and beats % 3 == 0:
            # Compound meter (6/8, 9/8, 12/8) - accent every 3rd beat
            pattern = [i % 3 == 0 for i in range(beats)]
        
        return pattern
    
    def get_beat_type(self, click_number: int) -> BeatType:
        """
        Determine the type of a specific click in the measure.
        
        Args:
            click_number: The click number (0-indexed)
            
        Returns:
            BeatType indicating if this is an accent, normal beat, or subdivision
        """
        if click_number < 0 or click_number >= self.total_clicks_per_measure:
            raise ValueError(f"Click number {click_number} out of range")
        
        # If it's a subdivision (not on the main beat)
        if click_number % self._subdivisions != 0:
            return BeatType.SUBDIVISION
        
        # Get the beat number (0-indexed)
        beat_number = click_number // self._subdivisions
        
        # Check if this beat is accented
        if self._accent_pattern[beat_number]:
            return BeatType.ACCENT
        
        return BeatType.NORMAL
    
    def set_custom_accents(self, accent_pattern: List[bool]):
        """
        Set a custom accent pattern.
        
        Args:
            accent_pattern: List of booleans for each beat in the measure
            
        Raises:
            ValueError: If pattern length doesn't match beats per measure
        """
        if len(accent_pattern) != self._time_signature.beats_per_measure:
            raise ValueError(
                f"Accent pattern length must match beats per measure "
                f"({self._time_signature.beats_per_measure})"
            )
        self._accent_pattern = accent_pattern.copy()
    
    def get_accent_pattern(self) -> List[bool]:
        """Get the current accent pattern."""
        return self._accent_pattern.copy()
    
    def __repr__(self) -> str:
        return (f"BeatPattern(time_signature={self._time_signature}, "
                f"subdivisions={self._subdivisions})")
