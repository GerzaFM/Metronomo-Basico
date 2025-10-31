"""
Tempo configuration model for managing BPM and timing.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TempoConfig:
    """
    Configuration for metronome tempo.
    
    Attributes:
        bpm: Beats per minute (30-300 typical range)
        name: Optional tempo marking name (e.g., "Allegro", "Andante")
    """
    
    bpm: int
    name: Optional[str] = None
    
    # BPM constraints
    MIN_BPM: int = 20
    MAX_BPM: int = 400
    DEFAULT_BPM: int = 120
    
    # Common tempo markings
    TEMPO_MARKINGS = {
        'Grave': (25, 45),
        'Largo': (40, 60),
        'Lento': (45, 60),
        'Adagio': (55, 65),
        'Andante': (73, 77),
        'Moderato': (86, 97),
        'Allegretto': (98, 109),
        'Allegro': (109, 132),
        'Vivace': (132, 140),
        'Presto': (168, 177),
        'Prestissimo': (178, 240),
    }
    
    def __post_init__(self):
        """Validate tempo configuration."""
        if not self.MIN_BPM <= self.bpm <= self.MAX_BPM:
            raise ValueError(
                f"BPM must be between {self.MIN_BPM} and {self.MAX_BPM}, "
                f"got {self.bpm}"
            )
    
    @property
    def interval_seconds(self) -> float:
        """
        Calculate the interval between beats in seconds.
        
        Returns:
            Time in seconds between beats
        """
        return 60.0 / self.bpm
    
    @property
    def interval_ms(self) -> float:
        """
        Calculate the interval between beats in milliseconds.
        
        Returns:
            Time in milliseconds between beats
        """
        return self.interval_seconds * 1000
    
    def get_tempo_marking(self) -> Optional[str]:
        """
        Get the Italian tempo marking that corresponds to this BPM.
        
        Returns:
            Tempo marking name if one matches, None otherwise
        """
        for marking, (min_bpm, max_bpm) in self.TEMPO_MARKINGS.items():
            if min_bpm <= self.bpm <= max_bpm:
                return marking
        return None
    
    def adjust_bpm(self, delta: int) -> 'TempoConfig':
        """
        Create a new TempoConfig with adjusted BPM.
        
        Args:
            delta: Amount to change BPM (can be negative)
            
        Returns:
            New TempoConfig with adjusted BPM
        """
        new_bpm = max(self.MIN_BPM, min(self.MAX_BPM, self.bpm + delta))
        return TempoConfig(bpm=new_bpm, name=self.name)
    
    @classmethod
    def from_tempo_marking(cls, marking: str) -> 'TempoConfig':
        """
        Create TempoConfig from an Italian tempo marking.
        
        Args:
            marking: Tempo marking name (e.g., "Allegro")
            
        Returns:
            TempoConfig with BPM in the middle of the range
            
        Raises:
            ValueError: If marking is not recognized
        """
        if marking not in cls.TEMPO_MARKINGS:
            raise ValueError(f"Unknown tempo marking: {marking}")
        
        min_bpm, max_bpm = cls.TEMPO_MARKINGS[marking]
        avg_bpm = (min_bpm + max_bpm) // 2
        return cls(bpm=avg_bpm, name=marking)
    
    def __str__(self) -> str:
        if self.name:
            return f"{self.name} ({self.bpm} BPM)"
        marking = self.get_tempo_marking()
        if marking:
            return f"{self.bpm} BPM ({marking})"
        return f"{self.bpm} BPM"
