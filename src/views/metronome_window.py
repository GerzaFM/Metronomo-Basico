"""
Main window for the metronome application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Optional

from ..controllers import MetronomeController
from ..services.audio_service import SoundType
from ..models.beat_pattern import BeatType
from .widgets import (
    BeatIndicator,
    BPMSlider,
    TimeSignatureSelector,
    PlaybackControls,
    VolumeControl
)

logger = logging.getLogger(__name__)


class MetronomeWindow:
    """
    Main window for the metronome application.
    
    This class manages the GUI and coordinates with the controller
    to provide metronome functionality.
    """
    
    def __init__(self, controller: MetronomeController):
        """
        Initialize the metronome window.
        
        Args:
            controller: Metronome controller instance
        """
        self._controller = controller
        self._root = tk.Tk()
        self._root.title("Professional Metronome")
        self._root.geometry("600x500")
        self._root.resizable(True, True)
        
        # Configure style
        self._setup_style()
        
        # Create UI
        self._create_widgets()
        
        # Register callbacks
        self._register_callbacks()
        
        # Handle window close
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _setup_style(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#ecf0f1')
        style.configure('TLabel', background='#ecf0f1', foreground='#2c3e50')
        style.configure('TButton', padding=6)
        style.configure('TLabelframe', background='#ecf0f1', foreground='#2c3e50')
        style.configure('TLabelframe.Label', background='#ecf0f1', foreground='#2c3e50', font=('Arial', 10, 'bold'))
        
        self._root.configure(bg='#ecf0f1')
    
    def _create_widgets(self):
        """Create all UI widgets."""
        # Main container
        main_frame = ttk.Frame(self._root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="🎵 Professional Metronome",
            font=('Arial', 20, 'bold'),
            foreground='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # Beat indicator
        self._beat_indicator = BeatIndicator(
            main_frame,
            beats_per_measure=4,
            width=400,
            height=60,
            bg='#ecf0f1',
            highlightthickness=0
        )
        self._beat_indicator.pack(pady=10)
        
        # Tempo controls frame
        tempo_frame = ttk.LabelFrame(main_frame, text="Tempo Control", padding="10")
        tempo_frame.pack(fill=tk.X, pady=10)
        
        self._bpm_slider = BPMSlider(
            tempo_frame,
            initial_bpm=self._controller.get_bpm(),
            callback=self._on_bpm_change
        )
        self._bpm_slider.pack(fill=tk.X, pady=5)
        
        # Tempo marking display
        self._tempo_info_var = tk.StringVar(value=self._controller.get_tempo_info())
        tempo_info_label = ttk.Label(
            tempo_frame,
            textvariable=self._tempo_info_var,
            font=('Arial', 11, 'italic'),
            foreground='#7f8c8d'
        )
        tempo_info_label.pack(pady=5)
        
        # Time signature controls
        signature_frame = ttk.LabelFrame(main_frame, text="Time Signature", padding="10")
        signature_frame.pack(fill=tk.X, pady=10)
        
        self._time_signature_selector = TimeSignatureSelector(
            signature_frame,
            initial_signature=self._controller.get_time_signature(),
            callback=self._on_time_signature_change
        )
        self._time_signature_selector.pack()
        
        # Playback controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(pady=15)
        
        self._playback_controls = PlaybackControls(
            controls_frame,
            on_play=self._on_play_pause,
            on_stop=self._on_stop,
            on_tap=self._on_tap_tempo
        )
        self._playback_controls.pack()
        
        # Volume control
        volume_frame = ttk.LabelFrame(main_frame, text="Volume", padding="10")
        volume_frame.pack(fill=tk.X, pady=10)
        
        self._volume_control = VolumeControl(
            volume_frame,
            initial_volume=self._controller.get_volume(),
            on_volume_change=self._on_volume_change,
            on_mute_toggle=self._on_mute_toggle
        )
        self._volume_control.pack()
        
        # Status bar
        self._status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self._status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=('Arial', 9)
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
    
    def _register_callbacks(self):
        """Register callbacks with the controller."""
        self._controller.add_beat_callback(self._on_beat)
        self._controller.add_state_callback(self._on_state_change)
    
    # ========== Event Handlers ==========
    
    def _on_bpm_change(self, bpm: int):
        """Handle BPM slider change."""
        try:
            self._controller.set_bpm(bpm)
            self._tempo_info_var.set(self._controller.get_tempo_info())
            logger.debug(f"BPM changed to {bpm}")
        except Exception as e:
            logger.error(f"Error setting BPM: {e}")
            messagebox.showerror("Error", f"Failed to set BPM: {e}")
    
    def _on_time_signature_change(self, signature: str):
        """Handle time signature change."""
        try:
            self._controller.set_time_signature(signature)
            # Update beat indicator
            beats = int(signature.split('/')[0])
            self._beat_indicator.set_beats_per_measure(beats)
            self._beat_indicator.reset()
            logger.info(f"Time signature changed to {signature}")
        except Exception as e:
            logger.error(f"Error setting time signature: {e}")
            messagebox.showerror("Error", f"Failed to set time signature: {e}")
    
    def _on_play_pause(self):
        """Handle play/pause button click."""
        try:
            self._controller.toggle_playback()
        except Exception as e:
            logger.error(f"Error toggling playback: {e}")
            messagebox.showerror("Error", f"Failed to toggle playback: {e}")
    
    def _on_stop(self):
        """Handle stop button click."""
        try:
            self._controller.stop()
            self._beat_indicator.reset()
        except Exception as e:
            logger.error(f"Error stopping: {e}")
            messagebox.showerror("Error", f"Failed to stop: {e}")
    
    def _on_tap_tempo(self):
        """Handle tap tempo button click."""
        try:
            self._controller.tap_tempo()
            # Update UI with new BPM
            new_bpm = self._controller.get_bpm()
            self._bpm_slider.set_bpm(new_bpm)
            self._tempo_info_var.set(self._controller.get_tempo_info())
        except Exception as e:
            logger.error(f"Error in tap tempo: {e}")
    
    def _on_volume_change(self, volume: float):
        """Handle volume slider change."""
        try:
            self._controller.set_volume(volume)
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
    
    def _on_mute_toggle(self):
        """Handle mute button click."""
        try:
            self._controller.toggle_mute()
            self._volume_control.set_muted(self._controller.is_muted())
        except Exception as e:
            logger.error(f"Error toggling mute: {e}")
    
    # ========== Controller Callbacks ==========
    
    def _on_beat(self, beat_number: int, sound_type: SoundType):
        """
        Callback for each beat.
        
        Args:
            beat_number: Current beat number
            sound_type: Type of sound played
        """
        # Update beat indicator (must be called from UI thread)
        is_accent = sound_type == SoundType.ACCENT
        self._root.after(0, lambda: self._beat_indicator.highlight_beat(beat_number, is_accent))
    
    def _on_state_change(self, state):
        """
        Callback for state changes.
        
        Args:
            state: New metronome state
        """
        # Update UI based on state
        def update_ui():
            self._playback_controls.set_playing(state.is_playing)
            
            if state.is_playing:
                self._status_var.set(f"Playing - Measure: {state.current_measure + 1}, Beat: {state.current_beat + 1}")
            elif state.is_paused:
                self._status_var.set("Paused")
            else:
                self._status_var.set("Ready")
        
        self._root.after(0, update_ui)
    
    def _on_close(self):
        """Handle window close event."""
        try:
            self._controller.stop()
            self._controller.cleanup()
            self._root.destroy()
            logger.info("Application closed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            self._root.destroy()
    
    # ========== Public Methods ==========
    
    def run(self):
        """Start the application main loop."""
        logger.info("Starting metronome application")
        self._root.mainloop()
    
    def get_root(self) -> tk.Tk:
        """Get the root window."""
        return self._root
