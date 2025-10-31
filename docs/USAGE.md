# Guía de Uso - Professional Metronome

## Inicio Rápido

### 1. Instalación

```bash
# Clonar repositorio
git clone https://github.com/yourusername/professional-metronome.git
cd professional-metronome

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación

```bash
python main.py
```

## Ejemplos de Uso

### Ejemplo 1: Uso Básico con GUI

```python
from src.controllers import MetronomeController
from src.views import MetronomeWindow

# Crear e inicializar controlador
controller = MetronomeController()
controller.initialize()

# Crear ventana
window = MetronomeWindow(controller)

# Ejecutar aplicación
window.run()
```

### Ejemplo 2: Uso Programático sin GUI

```python
from src.controllers import MetronomeController
import time

# Usar context manager para auto-cleanup
with MetronomeController() as controller:
    # Configurar
    controller.set_bpm(120)
    controller.set_time_signature("4/4")
    
    # Iniciar
    controller.start()
    
    # Dejar correr por 10 segundos
    time.sleep(10)
    
    # Detener
    controller.stop()
# Se limpia automáticamente aquí
```

### Ejemplo 3: Con Callbacks Personalizados

```python
from src.controllers import MetronomeController
from src.services.audio_service import SoundType

def on_beat(beat_number, sound_type):
    """Callback llamado en cada beat."""
    accent_mark = "!" if sound_type == SoundType.ACCENT else ""
    print(f"Beat {beat_number + 1}{accent_mark}")

def on_state_change(state):
    """Callback llamado cuando cambia el estado."""
    print(f"Estado: {state.status.value}")
    if state.is_playing:
        print(f"Compás {state.current_measure + 1}, Beat {state.current_beat + 1}")

# Crear controlador
controller = MetronomeController()
controller.initialize()

# Registrar callbacks
controller.add_beat_callback(on_beat)
controller.add_state_callback(on_state_change)

# Iniciar
controller.set_bpm(100)
controller.start()

# ... dejar correr ...
```

### Ejemplo 4: Cambiar Configuración en Tiempo Real

```python
from src.controllers import MetronomeController
import time

with MetronomeController() as controller:
    controller.start()
    
    # Empezar lento
    controller.set_bpm(60)
    controller.set_time_signature("4/4")
    time.sleep(5)
    
    # Acelerar
    controller.set_bpm(120)
    time.sleep(5)
    
    # Cambiar compás
    controller.set_time_signature("3/4")
    time.sleep(5)
    
    controller.stop()
```

### Ejemplo 5: Tap Tempo

```python
from src.controllers import MetronomeController
import time

controller = MetronomeController()
controller.initialize()

# Simular tapping
print("Tap tempo example...")
for i in range(4):
    controller.tap_tempo()
    time.sleep(0.5)  # Simular 120 BPM (0.5s entre beats)
    
print(f"BPM calculado: {controller.get_bpm()}")

controller.cleanup()
```

### Ejemplo 6: Usar Marcas de Tempo Italianas

```python
from src.controllers import MetronomeController

with MetronomeController() as controller:
    # Obtener marcas disponibles
    markings = controller.get_tempo_markings()
    print("Marcas disponibles:", markings)
    
    # Usar una marca
    controller.set_tempo_marking("Allegro")
    print(f"Tempo: {controller.get_tempo_info()}")
    
    controller.start()
    # ...
```

### Ejemplo 7: Control de Volumen

```python
from src.controllers import MetronomeController

with MetronomeController() as controller:
    # Volumen bajo
    controller.set_volume(0.3)
    controller.start()
    
    # ... después de un tiempo ...
    
    # Silenciar temporalmente
    controller.toggle_mute()
    
    # ... hacer algo ...
    
    # Reactivar
    controller.toggle_mute()
    
    # Volumen máximo
    controller.set_volume(1.0)
```

### Ejemplo 8: Subdivisiones

```python
from src.controllers import MetronomeController

with MetronomeController() as controller:
    controller.set_bpm(60)
    controller.set_time_signature("4/4")
    
    # Sin subdivisiones (solo quarter notes)
    controller.set_subdivisions(1)
    controller.start()
    # Escucharás: CLICK click click click (4 beats)
    
    # ... después ...
    
    # Con subdivisiones (eighth notes)
    controller.set_subdivisions(2)
    # Escucharás: CLICK tick click tick click tick click tick (8 beats)
```

### Ejemplo 9: Acentos Personalizados

```python
from src.controllers import MetronomeController

with MetronomeController() as controller:
    controller.set_time_signature("4/4")
    
    # Acentuar beats 1 y 3 (patrón rock común)
    controller.set_custom_accents([True, False, True, False])
    
    controller.start()
    # Escucharás: CLICK click CLICK click
```

### Ejemplo 10: Proveedor de Audio Personalizado

```python
from src.controllers import MetronomeController
from src.services.audio_service import IAudioProvider
from pathlib import Path

class MyCustomAudioProvider(IAudioProvider):
    """Proveedor de audio personalizado."""
    
    def initialize(self) -> bool:
        print("Inicializando mi proveedor de audio")
        return True
    
    def load_sound(self, sound_path: Path):
        print(f"Cargando: {sound_path}")
        return {"path": sound_path}  # Tu objeto de sonido
    
    def play_sound(self, sound) -> bool:
        print(f"Reproduciendo: {sound}")
        return True
    
    def set_volume(self, volume: float):
        print(f"Volumen: {volume}")
    
    def cleanup(self):
        print("Limpiando proveedor de audio")

# Usar proveedor personalizado
provider = MyCustomAudioProvider()
controller = MetronomeController(audio_provider=provider)
controller.initialize()
controller.start()
```

### Ejemplo 11: Monitorear Estadísticas

```python
from src.controllers import MetronomeController
import time

with MetronomeController() as controller:
    controller.set_bpm(120)
    controller.start()
    
    time.sleep(5)
    
    # Obtener estado
    state = controller.get_state()
    print(f"Beats tocados: {state.total_beats_played}")
    print(f"Compás actual: {state.current_measure}")
    print(f"Beat actual: {state.current_beat}")
    
    if state.session_duration:
        print(f"Duración de sesión: {state.session_duration:.2f}s")
```

### Ejemplo 12: Widget Personalizado en la GUI

```python
import tkinter as tk
from tkinter import ttk
from src.controllers import MetronomeController
from src.views import MetronomeWindow

class CustomMetronomeWindow(MetronomeWindow):
    """Ventana extendida con funcionalidad personalizada."""
    
    def _create_widgets(self):
        # Llamar al método padre para crear widgets normales
        super()._create_widgets()
        
        # Agregar widgets personalizados
        custom_frame = ttk.Frame(self._root)
        custom_frame.pack(pady=10)
        
        ttk.Label(custom_frame, text="Mi Widget Personalizado").pack()
        ttk.Button(
            custom_frame,
            text="Mi Acción",
            command=self._my_custom_action
        ).pack()
    
    def _my_custom_action(self):
        """Acción personalizada."""
        print("¡Acción personalizada ejecutada!")
        # Acceder al controlador
        current_bpm = self._controller.get_bpm()
        print(f"BPM actual: {current_bpm}")

# Usar ventana personalizada
controller = MetronomeController()
controller.initialize()
window = CustomMetronomeWindow(controller)
window.run()
```

## Casos de Uso Comunes

### Práctica Musical

```python
# Configuración para práctica de piano
controller.set_bpm(60)  # Comenzar lento
controller.set_time_signature("4/4")
controller.start()

# Gradualmente aumentar velocidad cada 2 minutos
# hasta alcanzar el tempo deseado
```

### Estudio de Compases Complejos

```python
# Practicar 7/8
controller.set_time_signature("7/8")
controller.set_custom_accents([True, False, False, True, False, False, False])
```

### Entrenamiento de Ritmo

```python
# Usar subdivisiones para mejorar timing
controller.set_subdivisions(4)  # Semicorcheas
controller.set_bpm(60)
```

## Solución de Problemas

### No se escucha sonido

```python
# Verificar volumen
print(f"Volumen: {controller.get_volume()}")
print(f"Silenciado: {controller.is_muted()}")

# Ajustar
controller.set_volume(1.0)
if controller.is_muted():
    controller.toggle_mute()
```

### Timing impreciso

```python
# El motor de metronomo tiene compensación automática
# pero se puede monitorear:

import logging
logging.basicConfig(level=logging.DEBUG)
# Verás warnings si hay drift > 5ms
```

### Error al inicializar

```python
controller = MetronomeController()
if not controller.initialize():
    print("Error en inicialización")
    # Verificar que pygame esté instalado
    # Verificar permisos de audio del sistema
```

## Mejores Prácticas

1. **Siempre usar context manager cuando sea posible**:
   ```python
   with MetronomeController() as controller:
       # tu código
   # cleanup automático
   ```

2. **Detener antes de cambiar configuración crítica**:
   ```python
   controller.stop()
   controller.set_time_signature("5/4")
   controller.start()
   ```

3. **Usar callbacks para sincronización**:
   ```python
   def on_beat(beat, sound):
       # Sincronizar con tu lógica
       pass
   controller.add_beat_callback(on_beat)
   ```

4. **Manejar excepciones**:
   ```python
   try:
       controller.set_bpm(bpm)
   except ValueError as e:
       print(f"BPM inválido: {e}")
   ```

## Recursos Adicionales

- Ver `docs/ARCHITECTURE.md` para detalles de arquitectura
- Ver `tests/` para más ejemplos de uso
- Ver docstrings en el código para documentación de API
