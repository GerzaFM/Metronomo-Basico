"""
Custom widgets for the metronome application.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class BeatIndicator(tk.Canvas):
    """
    Visual beat indicator that pulses on each beat.
    """
    
    def __init__(self, parent, beats_per_measure: int = 4, **kwargs):
        """
        Initialize beat indicator.
        
        Args:
            parent: Parent widget
            beats_per_measure: Number of beats to display
            **kwargs: Additional canvas arguments
        """
        super().__init__(parent, **kwargs)
        self._beats_per_measure = beats_per_measure
        self._current_beat = -1
        self._circles = []
        self._create_beat_circles()
    
    def _create_beat_circles(self):
        """Create visual circles for each beat."""
        self.delete("all")
        self._circles.clear()
        
        width = self.winfo_reqwidth() or 400
        height = self.winfo_reqheight() or 60
        
        # Calculate circle size and spacing
        circle_radius = min(20, width // (self._beats_per_measure * 3))
        spacing = (width - circle_radius * 2) / (self._beats_per_measure + 1)
        
        for i in range(self._beats_per_measure):
            x = spacing * (i + 1) + circle_radius
            y = height // 2
            
            circle = self.create_oval(
                x - circle_radius,
                y - circle_radius,
                x + circle_radius,
                y + circle_radius,
                fill='#d0d0d0',
                outline='#808080',
                width=2,
                tags=f"beat_{i}"
            )
            self._circles.append(circle)
    
    def set_beats_per_measure(self, beats: int):
        """Update the number of beats displayed."""
        self._beats_per_measure = beats
        self._current_beat = -1
        self._create_beat_circles()
    
    def highlight_beat(self, beat_number: int, is_accent: bool = False):
        """
        Highlight a specific beat.
        
        Args:
            beat_number: Beat to highlight (0-indexed)
            is_accent: Whether this is an accented beat
        """
        # Reset previous beat
        if 0 <= self._current_beat < len(self._circles):
            self.itemconfig(self._circles[self._current_beat], fill='#d0d0d0')
        
        # Highlight current beat
        if 0 <= beat_number < len(self._circles):
            color = '#ff4444' if is_accent else '#44ff44'
            self.itemconfig(self._circles[beat_number], fill=color)
            self._current_beat = beat_number
    
    def reset(self):
        """Reset all beats to default state."""
        for circle in self._circles:
            self.itemconfig(circle, fill='#d0d0d0')
        self._current_beat = -1


class BPMSlider(ttk.Frame):
    """
    Custom BPM slider with label and value display.
    """
    
    def __init__(
        self,
        parent,
        initial_bpm: int = 120,
        min_bpm: int = 20,
        max_bpm: int = 400,
        callback: Optional[Callable[[int], None]] = None,
        **kwargs
    ):
        """
        Initialize BPM slider.
        
        Args:
            parent: Parent widget
            initial_bpm: Initial BPM value
            min_bpm: Minimum BPM
            max_bpm: Maximum BPM
            callback: Function to call when value changes
            **kwargs: Additional frame arguments
        """
        super().__init__(parent, **kwargs)
        
        self._min_bpm = min_bpm
        self._max_bpm = max_bpm
        self._callback = callback
        self._bpm_var = tk.IntVar(value=initial_bpm)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create slider widgets."""
        # BPM Label
        label_frame = ttk.Frame(self)
        label_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(label_frame, text="Tempo (BPM):", font=('Arial', 10)).pack(side=tk.LEFT)
        self._value_label = ttk.Label(
            label_frame,
            textvariable=self._bpm_var,
            font=('Arial', 14, 'bold'),
            foreground='#2c3e50'
        )
        self._value_label.pack(side=tk.RIGHT)
        
        # Slider
        self._slider = ttk.Scale(
            self,
            from_=self._min_bpm,
            to=self._max_bpm,
            orient=tk.HORIZONTAL,
            variable=self._bpm_var,
            command=self._on_value_change
        )
        self._slider.pack(fill=tk.X, pady=(0, 5))
        
        # Fine control buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="-10",
            width=5,
            command=lambda: self.adjust_bpm(-10)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            button_frame,
            text="-1",
            width=5,
            command=lambda: self.adjust_bpm(-1)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            button_frame,
            text="+1",
            width=5,
            command=lambda: self.adjust_bpm(1)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            button_frame,
            text="+10",
            width=5,
            command=lambda: self.adjust_bpm(10)
        ).pack(side=tk.LEFT, padx=2)
    
    def _on_value_change(self, value):
        """Handle slider value change."""
        bpm = int(float(value))
        self._bpm_var.set(bpm)
        if self._callback:
            self._callback(bpm)
    
    def adjust_bpm(self, delta: int):
        """Adjust BPM by a delta value."""
        new_bpm = max(self._min_bpm, min(self._max_bpm, self._bpm_var.get() + delta))
        self._bpm_var.set(new_bpm)
        if self._callback:
            self._callback(new_bpm)
    
    def get_bpm(self) -> int:
        """Get current BPM value."""
        return self._bpm_var.get()
    
    def set_bpm(self, bpm: int):
        """Set BPM value."""
        bpm = max(self._min_bpm, min(self._max_bpm, bpm))
        self._bpm_var.set(bpm)


class TimeSignatureSelector(ttk.Frame):
    """
    Selector for time signatures.
    """
    
    COMMON_SIGNATURES = ['4/4', '3/4', '6/8', '2/4', '5/4', '7/8', '12/8']
    
    def __init__(
        self,
        parent,
        initial_signature: str = '4/4',
        callback: Optional[Callable[[str], None]] = None,
        **kwargs
    ):
        """
        Initialize time signature selector.
        
        Args:
            parent: Parent widget
            initial_signature: Initial time signature
            callback: Function to call when signature changes
            **kwargs: Additional frame arguments
        """
        super().__init__(parent, **kwargs)
        
        self._callback = callback
        self._signature_var = tk.StringVar(value=initial_signature)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create selector widgets."""
        ttk.Label(self, text="Time Signature:", font=('Arial', 10)).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        
        self._combobox = ttk.Combobox(
            self,
            textvariable=self._signature_var,
            values=self.COMMON_SIGNATURES,
            state='readonly',
            width=8,
            font=('Arial', 12)
        )
        self._combobox.pack(side=tk.LEFT)
        self._combobox.bind('<<ComboboxSelected>>', self._on_selection_change)
    
    def _on_selection_change(self, event):
        """Handle selection change."""
        if self._callback:
            self._callback(self._signature_var.get())
    
    def get_signature(self) -> str:
        """Get current time signature."""
        return self._signature_var.get()
    
    def set_signature(self, signature: str):
        """Set time signature."""
        if signature in self.COMMON_SIGNATURES:
            self._signature_var.set(signature)


class PlaybackControls(ttk.Frame):
    """
    Playback control buttons.
    """
    
    def __init__(
        self,
        parent,
        on_play: Optional[Callable] = None,
        on_stop: Optional[Callable] = None,
        on_tap: Optional[Callable] = None,
        **kwargs
    ):
        """
        Initialize playback controls.
        
        Args:
            parent: Parent widget
            on_play: Callback for play/pause button
            on_stop: Callback for stop button
            on_tap: Callback for tap tempo button
            **kwargs: Additional frame arguments
        """
        super().__init__(parent, **kwargs)
        
        self._on_play = on_play
        self._on_stop = on_stop
        self._on_tap = on_tap
        self._is_playing = False
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create control buttons."""
        # Play/Pause button
        self._play_button = ttk.Button(
            self,
            text="▶ Play",
            command=self._handle_play,
            width=12
        )
        self._play_button.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        ttk.Button(
            self,
            text="⬛ Stop",
            command=self._handle_stop,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        # Tap tempo button
        ttk.Button(
            self,
            text="👆 Tap Tempo",
            command=self._handle_tap,
            width=12
        ).pack(side=tk.LEFT, padx=5)
    
    def _handle_play(self):
        """Handle play/pause button click."""
        self._is_playing = not self._is_playing
        self._update_play_button()
        if self._on_play:
            self._on_play()
    
    def _handle_stop(self):
        """Handle stop button click."""
        self._is_playing = False
        self._update_play_button()
        if self._on_stop:
            self._on_stop()
    
    def _handle_tap(self):
        """Handle tap tempo button click."""
        if self._on_tap:
            self._on_tap()
    
    def _update_play_button(self):
        """Update play button text based on state."""
        if self._is_playing:
            self._play_button.config(text="⏸ Pause")
        else:
            self._play_button.config(text="▶ Play")
    
    def set_playing(self, is_playing: bool):
        """Set playing state."""
        self._is_playing = is_playing
        self._update_play_button()


class VolumeControl(ttk.Frame):
    """
    Volume control with mute button.
    """
    
    def __init__(
        self,
        parent,
        initial_volume: float = 1.0,
        on_volume_change: Optional[Callable[[float], None]] = None,
        on_mute_toggle: Optional[Callable] = None,
        **kwargs
    ):
        """
        Initialize volume control.
        
        Args:
            parent: Parent widget
            initial_volume: Initial volume (0.0-1.0)
            on_volume_change: Callback for volume changes
            on_mute_toggle: Callback for mute button
            **kwargs: Additional frame arguments
        """
        super().__init__(parent, **kwargs)
        
        self._on_volume_change = on_volume_change
        self._on_mute_toggle = on_mute_toggle
        self._volume_var = tk.DoubleVar(value=initial_volume * 100)  # Convert to 0-100 scale
        self._is_muted = False
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create volume control widgets."""
        ttk.Label(self, text="🔊", font=('Arial', 14)).pack(side=tk.LEFT, padx=5)
        
        self._volume_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self._volume_var,
            command=self._on_slider_change,
            length=150
        )
        self._volume_slider.pack(side=tk.LEFT, padx=5)
        
        self._mute_button = ttk.Button(
            self,
            text="🔇 Mute",
            command=self._handle_mute,
            width=10
        )
        self._mute_button.pack(side=tk.LEFT, padx=5)
    
    def _on_slider_change(self, value):
        """Handle volume slider change."""
        volume = float(value) / 100.0
        if self._on_volume_change:
            self._on_volume_change(volume)
    
    def _handle_mute(self):
        """Handle mute button click."""
        self._is_muted = not self._is_muted
        self._update_mute_button()
        if self._on_mute_toggle:
            self._on_mute_toggle()
    
    def _update_mute_button(self):
        """Update mute button text."""
        if self._is_muted:
            self._mute_button.config(text="🔊 Unmute")
        else:
            self._mute_button.config(text="🔇 Mute")
    
    def set_muted(self, is_muted: bool):
        """Set mute state."""
        self._is_muted = is_muted
        self._update_mute_button()
