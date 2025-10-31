"""
Audio service with provider abstraction for sound playback.

This module implements the Strategy pattern for audio playback,
allowing different audio backends to be used interchangeably.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class SoundType(Enum):
    """Types of metronome sounds."""
    ACCENT = "accent"
    NORMAL = "normal"
    SUBDIVISION = "subdivision"


class IAudioProvider(ABC):
    """
    Abstract interface for audio playback providers.
    
    This interface allows different audio backends (pygame, simpleaudio, etc.)
    to be used interchangeably following the Strategy pattern.
    """
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the audio provider.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def load_sound(self, sound_path: Path) -> Optional[any]:
        """
        Load a sound file.
        
        Args:
            sound_path: Path to the sound file
            
        Returns:
            Sound object that can be played, or None if loading failed
        """
        pass
    
    @abstractmethod
    def play_sound(self, sound: any) -> bool:
        """
        Play a loaded sound.
        
        Args:
            sound: Sound object returned from load_sound
            
        Returns:
            True if playback started successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def set_volume(self, volume: float):
        """
        Set the playback volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        pass
    
    @abstractmethod
    def cleanup(self):
        """Clean up resources used by the audio provider."""
        pass


class PygameAudioProvider(IAudioProvider):
    """Audio provider implementation using pygame mixer."""
    
    def __init__(self):
        """Initialize pygame audio provider."""
        self._initialized = False
        self._volume = 1.0
        self._loaded_sounds = []  # Keep track of loaded sounds
    
    def initialize(self) -> bool:
        """Initialize pygame mixer."""
        try:
            import pygame
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self._initialized = True
            logger.info("Pygame audio provider initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize pygame audio: {e}")
            return False
    
    def load_sound(self, sound_path: Path) -> Optional[any]:
        """Load a sound using pygame."""
        if not self._initialized:
            logger.error("Audio provider not initialized")
            return None
        
        try:
            import pygame
            sound = pygame.mixer.Sound(str(sound_path))
            sound.set_volume(self._volume)
            self._loaded_sounds.append(sound)  # Track this sound
            logger.debug(f"Loaded sound: {sound_path}")
            return sound
        except Exception as e:
            logger.error(f"Failed to load sound {sound_path}: {e}")
            return None
    
    def play_sound(self, sound: any) -> bool:
        """Play a pygame sound."""
        if sound is None:
            return False
        
        try:
            sound.play()
            return True
        except Exception as e:
            logger.error(f"Failed to play sound: {e}")
            return False
    
    def set_volume(self, volume: float):
        """Set volume for pygame."""
        self._volume = max(0.0, min(1.0, volume))
        # Update volume for all loaded sounds
        for sound in self._loaded_sounds:
            try:
                sound.set_volume(self._volume)
            except:
                pass
        # Removed logger.debug to avoid console spam
    
    def cleanup(self):
        """Clean up pygame resources."""
        if self._initialized:
            try:
                import pygame
                self._loaded_sounds.clear()
                pygame.mixer.quit()
                logger.info("Pygame audio provider cleaned up")
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")


class AudioService:
    """
    Service for managing audio playback in the metronome.
    
    This service acts as a facade for the audio provider and manages
    loading and playing of different sound types.
    """
    
    def __init__(self, provider: IAudioProvider, sounds_dir: Optional[Path] = None):
        """
        Initialize the audio service.
        
        Args:
            provider: Audio provider implementation
            sounds_dir: Directory containing sound files
        """
        self._provider = provider
        self._sounds_dir = sounds_dir or Path(__file__).parent.parent.parent / "assets" / "sounds"
        self._sounds: Dict[SoundType, any] = {}
        self._volume = 1.0
        self._muted = False
    
    def initialize(self) -> bool:
        """
        Initialize the audio service and load sounds.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        if not self._provider.initialize():
            return False
        
        # Load default sounds (will be generated if not present)
        self._load_default_sounds()
        return True
    
    def _load_default_sounds(self):
        """Load or generate default metronome sounds."""
        sound_files = {
            SoundType.ACCENT: self._sounds_dir / "accent.wav",
            SoundType.NORMAL: self._sounds_dir / "normal.wav",
            SoundType.SUBDIVISION: self._sounds_dir / "subdivision.wav",
        }
        
        for sound_type, sound_path in sound_files.items():
            if sound_path.exists():
                sound = self._provider.load_sound(sound_path)
                if sound:
                    self._sounds[sound_type] = sound
                    logger.info(f"Loaded {sound_type.value} sound")
            else:
                logger.warning(f"Sound file not found: {sound_path}")
                # Generate a default beep sound
                self._generate_default_sound(sound_type, sound_path)
    
    def _generate_default_sound(self, sound_type: SoundType, output_path: Path):
        """
        Generate a default beep sound if sound file is missing.
        
        Args:
            sound_type: Type of sound to generate
            output_path: Where to save the generated sound
        """
        try:
            import numpy as np
            import wave
            
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Generate different frequencies for different sound types
            frequencies = {
                SoundType.ACCENT: 1200,      # Higher pitch for accent
                SoundType.NORMAL: 800,       # Medium pitch for normal
                SoundType.SUBDIVISION: 600,  # Lower pitch for subdivision
            }
            
            frequency = frequencies[sound_type]
            duration = 0.05  # 50ms
            sample_rate = 44100
            
            # Generate sine wave
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave_data = np.sin(2 * np.pi * frequency * t)
            
            # Apply envelope to avoid clicks
            envelope = np.exp(-t * 20)
            wave_data *= envelope
            
            # Convert to 16-bit PCM
            wave_data = (wave_data * 32767).astype(np.int16)
            
            # Save as WAV file
            with wave.open(str(output_path), 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(wave_data.tobytes())
            
            logger.info(f"Generated default {sound_type.value} sound")
            
            # Load the generated sound
            sound = self._provider.load_sound(output_path)
            if sound:
                self._sounds[sound_type] = sound
                
        except ImportError:
            logger.warning("NumPy not available, cannot generate default sounds")
        except Exception as e:
            logger.error(f"Failed to generate default sound: {e}")
    
    def play_sound(self, sound_type: SoundType) -> bool:
        """
        Play a metronome sound.
        
        Args:
            sound_type: Type of sound to play
            
        Returns:
            True if sound was played successfully, False otherwise
        """
        if self._muted:
            return False
        
        sound = self._sounds.get(sound_type)
        if sound is None:
            logger.warning(f"Sound {sound_type.value} not loaded")
            return False
        
        return self._provider.play_sound(sound)
    
    def set_volume(self, volume: float):
        """
        Set the playback volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self._volume = max(0.0, min(1.0, volume))
        self._provider.set_volume(self._volume)
        # Removed logger.info to avoid console spam
    
    def get_volume(self) -> float:
        """Get the current volume level."""
        return self._volume
    
    def mute(self):
        """Mute audio playback."""
        self._muted = True
        logger.info("Audio muted")
    
    def unmute(self):
        """Unmute audio playback."""
        self._muted = False
        logger.info("Audio unmuted")
    
    def is_muted(self) -> bool:
        """Check if audio is muted."""
        return self._muted
    
    def toggle_mute(self):
        """Toggle mute state."""
        if self._muted:
            self.unmute()
        else:
            self.mute()
    
    def cleanup(self):
        """Clean up audio resources."""
        self._provider.cleanup()
        self._sounds.clear()
        logger.info("Audio service cleaned up")
