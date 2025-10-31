#!/usr/bin/env python
"""
Ejemplo simple de uso del metrónomo.

Este script demuestra el uso básico programático del metrónomo.
"""

import time
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.controllers import MetronomeController
from src.services.audio_service import SoundType


def example_basic():
    """Ejemplo básico de uso."""
    print("=== Ejemplo Básico ===\n")
    
    with MetronomeController() as controller:
        print("Configurando metrónomo...")
        controller.set_bpm(120)
        controller.set_time_signature("4/4")
        
        print(f"Tempo: {controller.get_tempo_info()}")
        print(f"Compás: {controller.get_time_signature()}")
        print("\nIniciando metrónomo por 5 segundos...")
        
        controller.start()
        time.sleep(5)
        
        print("\nDeteniéndose...")
        controller.stop()
        print("Finalizado.\n")


def example_with_callbacks():
    """Ejemplo con callbacks."""
    print("=== Ejemplo con Callbacks ===\n")
    
    beat_count = 0
    
    def on_beat(beat_number, sound_type):
        nonlocal beat_count
        beat_count += 1
        accent = "!" if sound_type == SoundType.ACCENT else ""
        print(f"Beat {beat_number + 1}{accent}", end=" ")
        if (beat_number + 1) % 4 == 0:
            print()  # Nueva línea cada compás
    
    def on_state_change(state):
        if state.is_playing:
            print(f"▶ Reproduciendo - Compás {state.current_measure + 1}")
        elif state.is_stopped:
            print("⬛ Detenido")
    
    with MetronomeController() as controller:
        controller.add_beat_callback(on_beat)
        controller.add_state_callback(on_state_change)
        
        controller.set_bpm(100)
        controller.set_time_signature("4/4")
        
        print("Iniciando...")
        controller.start()
        
        time.sleep(6)
        
        controller.stop()
        print(f"\nTotal de beats: {beat_count}\n")


def example_tempo_changes():
    """Ejemplo cambiando el tempo dinámicamente."""
    print("=== Ejemplo con Cambios de Tempo ===\n")
    
    with MetronomeController() as controller:
        tempos = [60, 80, 100, 120, 140]
        
        for bpm in tempos:
            controller.set_bpm(bpm)
            print(f"♩ = {bpm} BPM ({controller.get_tempo_info()})")
            controller.start()
            time.sleep(3)
            controller.stop()
            time.sleep(0.5)
        
        print("\nFinalizado.\n")


def example_different_time_signatures():
    """Ejemplo con diferentes compases."""
    print("=== Ejemplo con Diferentes Compases ===\n")
    
    signatures = ["4/4", "3/4", "6/8", "5/4"]
    
    with MetronomeController() as controller:
        controller.set_bpm(100)
        
        for sig in signatures:
            controller.set_time_signature(sig)
            print(f"Compás: {sig}")
            controller.start()
            time.sleep(4)
            controller.stop()
            time.sleep(0.5)
        
        print("\nFinalizado.\n")


def main():
    """Función principal."""
    print("╔═══════════════════════════════════════════════╗")
    print("║   Professional Metronome - Ejemplos de Uso   ║")
    print("╚═══════════════════════════════════════════════╝\n")
    
    try:
        # Ejecutar ejemplos
        example_basic()
        time.sleep(1)
        
        example_with_callbacks()
        time.sleep(1)
        
        example_tempo_changes()
        time.sleep(1)
        
        example_different_time_signatures()
        
        print("✅ Todos los ejemplos completados exitosamente!")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
