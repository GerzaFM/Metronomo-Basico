# Arquitectura del Professional Metronome

## Visión General

Este documento describe la arquitectura del sistema Professional Metronome, sus componentes principales, patrones de diseño y decisiones arquitectónicas.

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │    Window    │  │   Widgets    │  │  GUI Events  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   Controller Layer                       │
│            ┌─────────────────────────┐                   │
│            │  MetronomeController    │ (Facade)          │
│            └─────────────────────────┘                   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    Service Layer                         │
│  ┌──────────────┐            ┌──────────────┐           │
│  │   Engine     │◄───────────┤AudioService  │           │
│  │              │            │              │           │
│  └──────────────┘            └──────┬───────┘           │
│                                     │                   │
│                                     ▼                   │
│                          ┌──────────────────┐           │
│                          │ IAudioProvider   │ (Strategy)│
│                          └──────────────────┘           │
│                                   △                     │
│                     ┌─────────────┴─────────────┐       │
│                     │                           │       │
│            ┌────────┴──────┐         ┌─────────┴────┐  │
│            │PygameProvider │         │CustomProvider│  │
│            └───────────────┘         └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                     Domain Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ BeatPattern  │  │ TempoConfig  │  │    State     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Capas de la Arquitectura

### 1. Domain Layer (Capa de Dominio)

**Responsabilidad**: Entidades de negocio y reglas de dominio.

**Componentes**:
- `BeatPattern`: Gestiona patrones de compás, acentuación y subdivisiones
- `TempoConfig`: Configuración de tempo, BPM, marcas italianas
- `MetronomeState`: Estado del metrónomo en tiempo de ejecución
- `TimeSignature`: Representación de compases musicales

**Características**:
- Sin dependencias externas
- Inmutabilidad donde es apropiado (usando `@dataclass(frozen=True)`)
- Validación de datos en `__post_init__`
- Type hints completos

### 2. Service Layer (Capa de Servicios)

**Responsabilidad**: Lógica de negocio y coordinación.

**Componentes**:

#### AudioService
- **Patrón**: Strategy Pattern
- **Responsabilidad**: Gestión de reproducción de audio
- **Características**:
  - Abstracción mediante `IAudioProvider`
  - Generación automática de sonidos si no existen
  - Control de volumen y mute
  - Carga de múltiples tipos de sonidos

#### MetronomeEngine
- **Responsabilidad**: Motor de timing y coordinación
- **Características**:
  - Loop de timing preciso en thread separado
  - Compensación de drift temporal
  - Sistema de callbacks (Observer Pattern)
  - Thread-safe con `threading.RLock`
  - Detección de errores de timing

### 3. Controller Layer (Capa de Control)

**Componentes**:

#### MetronomeController
- **Patrón**: Facade Pattern
- **Responsabilidad**: API simplificada para la aplicación
- **Características**:
  - Coordina entre servicios y modelos
  - Valida inputs
  - Gestión de callbacks
  - Context manager support (`__enter__`/`__exit__`)

### 4. Presentation Layer (Capa de Presentación)

**Componentes**:

#### Widgets Personalizados
- `BeatIndicator`: Indicador visual de beats
- `BPMSlider`: Control de tempo con fine-tuning
- `TimeSignatureSelector`: Selector de compás
- `PlaybackControls`: Controles de reproducción
- `VolumeControl`: Control de volumen

#### MetronomeWindow
- **Responsabilidad**: Ventana principal y coordinación de UI
- **Características**:
  - Binding de eventos
  - Actualización thread-safe de UI
  - Gestión del ciclo de vida

## Patrones de Diseño

### 1. Strategy Pattern (IAudioProvider)

**Problema**: Necesidad de soportar diferentes backends de audio.

**Solución**: Interface `IAudioProvider` con implementaciones intercambiables.

```python
class IAudioProvider(ABC):
    @abstractmethod
    def initialize(self) -> bool: ...
    @abstractmethod
    def play_sound(self, sound) -> bool: ...
```

**Beneficios**:
- Fácil agregar nuevos proveedores
- Testing simplificado con mocks
- Desacoplamiento de implementación

### 2. Facade Pattern (MetronomeController)

**Problema**: Sistema complejo con múltiples subsistemas.

**Solución**: Controller que proporciona una API unificada.

```python
class MetronomeController:
    def start(self): ...
    def set_bpm(self, bpm): ...
    def set_time_signature(self, sig): ...
```

**Beneficios**:
- API simple para clientes
- Oculta complejidad interna
- Punto único de entrada

### 3. Observer Pattern (Callbacks)

**Problema**: UI necesita reaccionar a eventos del motor.

**Solución**: Sistema de callbacks registrables.

```python
engine.add_beat_callback(on_beat)
engine.add_state_callback(on_state_change)
```

**Beneficios**:
- Desacoplamiento de componentes
- Múltiples observadores
- Comunicación asíncrona

### 4. Dependency Injection

**Problema**: Componentes necesitan dependencias configurables.

**Solución**: Inyección mediante constructor.

```python
def __init__(self, audio_provider: IAudioProvider):
    self._provider = audio_provider
```

**Beneficios**:
- Testabilidad
- Flexibilidad
- Inversión de control

## Decisiones Arquitectónicas

### Threading Model

**Decisión**: Loop de timing en thread separado.

**Razones**:
- No bloquear UI thread
- Timing preciso con `time.perf_counter()`
- Compensación de drift

**Implementación**:
```python
def _timing_loop(self):
    next_beat_time = time.perf_counter()
    while not self._stop_event.is_set():
        # Compensating timer
        interval = self._tempo_config.interval_seconds
        next_beat_time += interval
        # ... process beat ...
        sleep_time = next_beat_time - time.perf_counter()
        if sleep_time > 0:
            time.sleep(sleep_time)
```

### Inmutabilidad Selectiva

**Decisión**: Usar `@dataclass(frozen=True)` para configuración.

**Razones**:
- Thread-safety
- Claridad de intención
- Prevención de bugs

**Ejemplo**:
```python
@dataclass(frozen=True)
class TimeSignature:
    beats_per_measure: int
    beat_unit: int
```

### Separación de Concerns

**Decisión**: Arquitectura en capas estricta.

**Reglas**:
- Domain no depende de nada
- Services dependen de Domain
- Controllers dependen de Services y Domain
- Views dependen de Controllers

### Error Handling

**Decisión**: Logging comprehensivo + validación temprana.

**Implementación**:
- Validación en `__post_init__`
- Excepciones descriptivas
- Logging en todos los niveles
- Try-catch en boundaries

## Flujo de Datos

### Inicio de Reproducción

```
1. User clicks "Play"
   │
   ▼
2. MetronomeWindow._on_play_pause()
   │
   ▼
3. MetronomeController.toggle_playback()
   │
   ▼
4. MetronomeEngine.start()
   │
   ▼
5. Thread starts → _timing_loop()
   │
   ▼
6. Loop: _process_beat()
   │
   ├─► AudioService.play_sound()
   │   └─► IAudioProvider.play_sound()
   │
   └─► Callbacks fired
       ├─► UI updates
       └─► State changes
```

### Cambio de BPM

```
1. User adjusts slider
   │
   ▼
2. BPMSlider._on_value_change()
   │
   ▼
3. MetronomeController.set_bpm()
   │
   ├─► Validates BPM
   ├─► Creates TempoConfig
   │
   ▼
4. MetronomeEngine.tempo_config = ...
   │
   ▼
5. Next beat uses new interval
```

## Extensibilidad

### Agregar nuevo Audio Provider

```python
class MyProvider(IAudioProvider):
    def initialize(self): ...
    def load_sound(self, path): ...
    def play_sound(self, sound): ...
    def set_volume(self, volume): ...
    def cleanup(self): ...

controller = MetronomeController(audio_provider=MyProvider())
```

### Agregar nuevo Widget

```python
class MyWidget(ttk.Frame):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        # ... implement ...

# En MetronomeWindow
self._my_widget = MyWidget(parent, callback=self._on_custom_event)
```

## Testing Strategy

### Unit Tests
- Cada capa testeada independientemente
- Mocks para dependencias externas
- Cobertura > 80%

### Integration Tests
- Controller con servicios reales
- Audio con mock provider

### UI Tests
- Event simulation
- State verification

## Performance Considerations

### Timing Precision
- Uso de `perf_counter()` para alta precisión
- Compensating timer para evitar drift
- Detección de timing errors

### Thread Safety
- `RLock` para estado compartido
- Callbacks ejecutados en UI thread (`root.after()`)
- Atomic operations donde sea posible

### Resource Management
- Cleanup explícito
- Context manager support
- Proper thread joining

## Logging

### Niveles
- **DEBUG**: Timing details, callbacks
- **INFO**: State changes, configuration
- **WARNING**: Timing drift, missing resources
- **ERROR**: Failures, exceptions

### Formato
```
2024-10-31 10:15:23 - src.services.metronome_engine - INFO - Metronome started
```

## Conclusión

Esta arquitectura proporciona:
- ✅ Separación clara de responsabilidades
- ✅ Fácil mantenimiento y extensión
- ✅ Testabilidad completa
- ✅ Rendimiento óptimo
- ✅ Código profesional y limpio
