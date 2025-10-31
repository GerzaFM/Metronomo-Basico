# 🎵 Professional Metronome

Una aplicación de metrónomo profesional con arquitectura limpia, diseñada para uso comercial.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Características

- ✨ **Interfaz gráfica moderna** con Tkinter
- 🎯 **Control preciso de tempo** (20-400 BPM)
- 🎼 **Múltiples compases** (4/4, 3/4, 6/8, etc.)
- 🔊 **Control de volumen y silencio**
- 👆 **Tap Tempo** para calcular BPM
- 📊 **Indicador visual de beats**
- 🎨 **Marcas de tempo italianas** (Allegro, Andante, etc.)
- 🔧 **Subdivisiones** configurables
- 🎵 **Acentos personalizables**

## 🏗️ Arquitectura

Este proyecto sigue principios de **arquitectura limpia** y patrones de diseño profesionales:

### Estructura del Proyecto

```
Metronomo/
├── src/
│   ├── models/              # Capa de dominio (entidades)
│   │   ├── beat_pattern.py  # Patrones de compás
│   │   ├── tempo_config.py  # Configuración de tempo
│   │   └── metronome_state.py # Estado del metrónomo
│   ├── services/            # Capa de servicios (lógica de negocio)
│   │   ├── audio_service.py # Servicio de audio (Strategy Pattern)
│   │   └── metronome_engine.py # Motor del metrónomo
│   ├── controllers/         # Controladores (MVC)
│   │   └── metronome_controller.py # Controlador principal (Facade)
│   ├── views/               # Capa de presentación
│   │   ├── widgets.py       # Widgets personalizados
│   │   └── metronome_window.py # Ventana principal
│   └── utils/               # Utilidades
├── tests/                   # Pruebas unitarias
├── assets/                  # Recursos (sonidos)
├── config/                  # Archivos de configuración
└── docs/                    # Documentación

```

### Patrones de Diseño Implementados

1. **MVC (Model-View-Controller)**: Separación clara de responsabilidades
2. **Strategy Pattern**: Abstracción del proveedor de audio (`IAudioProvider`)
3. **Facade Pattern**: `MetronomeController` simplifica la interacción con el sistema
4. **Observer Pattern**: Sistema de callbacks para eventos
5. **Dependency Injection**: Los componentes reciben sus dependencias
6. **Data Classes**: Uso de `@dataclass` para modelos inmutables

### Principios SOLID

- ✅ **Single Responsibility**: Cada clase tiene una única responsabilidad
- ✅ **Open/Closed**: Extensible sin modificar código existente
- ✅ **Liskov Substitution**: Proveedores de audio intercambiables
- ✅ **Interface Segregation**: Interfaces específicas y pequeñas
- ✅ **Dependency Inversion**: Dependencias en abstracciones, no implementaciones

## 🚀 Instalación

### Requisitos

- Python 3.8 o superior
- pip

### Pasos

1. **Clonar el repositorio**:
```bash
git clone https://github.com/yourusername/professional-metronome.git
cd professional-metronome
```

2. **Crear entorno virtual** (recomendado):
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

## 💻 Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Uso programático

```python
from src.controllers import MetronomeController
from src.views import MetronomeWindow

# Crear controlador
controller = MetronomeController()
controller.initialize()

# Configurar
controller.set_bpm(120)
controller.set_time_signature("4/4")

# Iniciar
controller.start()

# O usar la GUI
window = MetronomeWindow(controller)
window.run()
```

### Uso como Context Manager

```python
from src.controllers import MetronomeController

with MetronomeController() as controller:
    controller.set_bpm(140)
    controller.start()
    # ... hacer algo ...
# Se limpia automáticamente al salir del contexto
```

## 🧪 Testing

Ejecutar todas las pruebas:

```bash
python -m pytest tests/
```

Ejecutar con cobertura:

```bash
python -m pytest --cov=src tests/
```

Ejecutar pruebas específicas:

```bash
python -m unittest tests.test_models
python -m unittest tests.test_controller
```

## 📚 Documentación de API

### MetronomeController

Controlador principal que coordina toda la funcionalidad.

```python
controller = MetronomeController()

# Inicialización
controller.initialize()

# Control de reproducción
controller.start()
controller.stop()
controller.pause()
controller.toggle_playback()

# Control de tempo
controller.set_bpm(120)
controller.increase_bpm(10)
controller.decrease_bpm(5)
controller.tap_tempo()

# Compás
controller.set_time_signature("3/4")
controller.set_subdivisions(2)

# Audio
controller.set_volume(0.8)
controller.toggle_mute()

# Estado
state = controller.get_state()
is_playing = controller.is_playing()
```

### BeatPattern

Gestiona patrones de compás y acentuación.

```python
from src.models import BeatPattern, TimeSignature

# Crear patrón
sig = TimeSignature(4, 4)
pattern = BeatPattern(sig, subdivisions=1)

# Acentos personalizados
pattern.set_custom_accents([True, False, True, False])

# Obtener información
beat_type = pattern.get_beat_type(0)  # ACCENT, NORMAL, SUBDIVISION
```

### TempoConfig

Configuración de tempo y BPM.

```python
from src.models import TempoConfig

# Crear configuración
config = TempoConfig(bpm=120)

# Obtener intervalos
seconds = config.interval_seconds
ms = config.interval_ms

# Marcas de tempo
marking = config.get_tempo_marking()  # "Allegro"
config = TempoConfig.from_tempo_marking("Andante")
```

## 🎨 Personalización

### Crear un proveedor de audio personalizado

```python
from src.services import IAudioProvider
from pathlib import Path

class MyAudioProvider(IAudioProvider):
    def initialize(self) -> bool:
        # Tu implementación
        return True
    
    def load_sound(self, sound_path: Path):
        # Cargar sonido
        return sound_object
    
    def play_sound(self, sound) -> bool:
        # Reproducir
        return True
    
    def set_volume(self, volume: float):
        # Ajustar volumen
        pass
    
    def cleanup(self):
        # Limpiar recursos
        pass

# Usar tu proveedor
controller = MetronomeController(audio_provider=MyAudioProvider())
```

### Agregar sonidos personalizados

Coloca archivos WAV en `assets/sounds/`:
- `accent.wav` - Sonido del beat acentuado
- `normal.wav` - Sonido del beat normal
- `subdivision.wav` - Sonido de subdivisiones

## 🔧 Configuración

Editar `config/config.yaml`:

```yaml
metronome:
  default_bpm: 120
  default_time_signature: "4/4"
  min_bpm: 20
  max_bpm: 400

audio:
  sample_rate: 44100
  buffer_size: 512
  default_volume: 1.0
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código

- Seguir PEP 8
- Docstrings en formato Google
- Type hints en todas las funciones
- Cobertura de tests > 80%

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores

- Tu Nombre - *Trabajo inicial*

## 🙏 Agradecimientos

- Pygame por el motor de audio
- NumPy para generación de sonidos
- La comunidad de Python

## 📞 Soporte

Para soporte, email your.email@example.com o abre un issue en GitHub.

## 🗺️ Roadmap

- [ ] Presets de tempo guardables
- [ ] Soporte para múltiples idiomas
- [ ] Modo oscuro
- [ ] Exportar sesiones
- [ ] Aplicación móvil
- [ ] Sincronización MIDI

## 📊 Estado del Proyecto

- ✅ Core funcional
- ✅ Interfaz gráfica
- ✅ Pruebas unitarias
- ✅ Documentación
- 🚧 Optimizaciones de rendimiento
- 🚧 Más presets de tempo

---

Hecho con ❤️ y ☕ por [Tu Nombre]
