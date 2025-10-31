# Estructura del Proyecto - Professional Metronome

```
Metronomo/
│
├── 📄 README.md                    # Documentación principal
├── 📄 LICENSE                      # Licencia MIT
├── 📄 .gitignore                   # Configuración Git
├── 📄 requirements.txt             # Dependencias Python
├── 📄 setup.py                     # Script de instalación
├── 🚀 main.py                      # Punto de entrada principal
│
├── 📁 src/                         # Código fuente
│   ├── 📄 __init__.py
│   │
│   ├── 📁 models/                  # 🎯 DOMAIN LAYER
│   │   ├── 📄 __init__.py
│   │   ├── 📄 beat_pattern.py      # Patrones de compás y acentuación
│   │   ├── 📄 tempo_config.py      # Configuración de tempo y BPM
│   │   └── 📄 metronome_state.py   # Estado del metrónomo
│   │
│   ├── 📁 services/                # ⚙️ SERVICE LAYER
│   │   ├── 📄 __init__.py
│   │   ├── 📄 audio_service.py     # Servicio de audio (Strategy Pattern)
│   │   └── 📄 metronome_engine.py  # Motor de timing y coordinación
│   │
│   ├── 📁 controllers/             # 🎮 CONTROLLER LAYER
│   │   ├── 📄 __init__.py
│   │   └── 📄 metronome_controller.py  # Controlador principal (Facade)
│   │
│   ├── 📁 views/                   # 🖼️ PRESENTATION LAYER
│   │   ├── 📄 __init__.py
│   │   ├── 📄 widgets.py           # Widgets personalizados
│   │   └── 📄 metronome_window.py  # Ventana principal
│   │
│   └── 📁 utils/                   # 🛠️ UTILITIES
│       └── 📄 __init__.py          # Logging, helpers
│
├── 📁 tests/                       # 🧪 TESTS
│   ├── 📄 __init__.py
│   ├── 📄 test_models.py           # Tests de modelos
│   ├── 📄 test_audio_service.py    # Tests de audio
│   └── 📄 test_controller.py       # Tests de controlador
│
├── 📁 assets/                      # 🎨 ASSETS
│   └── 📁 sounds/                  # Archivos de audio
│       ├── accent.wav              # (generado automáticamente)
│       ├── normal.wav              # (generado automáticamente)
│       └── subdivision.wav         # (generado automáticamente)
│
├── 📁 config/                      # ⚙️ CONFIGURATION
│   └── 📄 config.yaml              # Archivo de configuración
│
├── 📁 docs/                        # 📚 DOCUMENTATION
│   ├── 📄 ARCHITECTURE.md          # Documentación de arquitectura
│   └── 📄 USAGE.md                 # Guía de uso
│
└── 📁 examples/                    # 💡 EXAMPLES
    └── 📄 basic_usage.py           # Ejemplos de uso programático
```

## Descripción de Componentes

### 🎯 Domain Layer (Modelos)
**Responsabilidad**: Lógica de negocio pura, sin dependencias externas
- `BeatPattern`: Gestiona patrones de compás, acentuación
- `TempoConfig`: Maneja configuración de tempo y BPM
- `MetronomeState`: Representa el estado en tiempo de ejecución

### ⚙️ Service Layer (Servicios)
**Responsabilidad**: Operaciones de negocio y coordinación
- `AudioService`: Abstracción de reproducción de audio (Strategy Pattern)
- `MetronomeEngine`: Motor de timing preciso, callbacks, threading

### 🎮 Controller Layer (Controladores)
**Responsabilidad**: Orquestación entre capas
- `MetronomeController`: API simplificada (Facade Pattern)

### 🖼️ Presentation Layer (Vistas)
**Responsabilidad**: Interfaz de usuario
- `MetronomeWindow`: Ventana principal de la aplicación
- `widgets.py`: Componentes UI personalizados
  - BeatIndicator
  - BPMSlider
  - TimeSignatureSelector
  - PlaybackControls
  - VolumeControl

### 🧪 Tests
**Cobertura completa de**:
- Modelos de dominio
- Servicios de audio
- Controladores
- Casos de uso

### 📚 Documentación
- **README.md**: Vista general, instalación, uso básico
- **ARCHITECTURE.md**: Diseño detallado, patrones, decisiones
- **USAGE.md**: Guía completa con ejemplos

## Características Técnicas

### Patrones de Diseño
- ✅ MVC (Model-View-Controller)
- ✅ Strategy (IAudioProvider)
- ✅ Facade (MetronomeController)
- ✅ Observer (Callbacks)
- ✅ Dependency Injection

### Principios SOLID
- ✅ Single Responsibility
- ✅ Open/Closed
- ✅ Liskov Substitution
- ✅ Interface Segregation
- ✅ Dependency Inversion

### Calidad de Código
- ✅ Type hints completos
- ✅ Docstrings (Google style)
- ✅ PEP 8 compliant
- ✅ Logging comprehensivo
- ✅ Error handling robusto
- ✅ Thread-safe operations
- ✅ Context managers
- ✅ Unit tests

### Características Avanzadas
- ⚡ Timing preciso con compensación de drift
- 🧵 Threading apropiado para no bloquear UI
- 🔒 Thread-safety con locks
- 🎵 Generación automática de sonidos
- 📊 Estadísticas de sesión
- 🎯 Callbacks para extensibilidad

## Tamaño del Proyecto

```
Archivos Python:     ~20 archivos
Líneas de código:    ~2,500+ líneas
Tests:               ~600+ líneas
Documentación:       ~1,500+ líneas
```

## Dependencias

```
pygame      >= 2.5.0  (Audio backend)
numpy       >= 1.24.0 (Generación de sonidos)
```

## Licencia

MIT License - Ver LICENSE para detalles
