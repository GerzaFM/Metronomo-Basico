# 🚀 Guía de Inicio Rápido

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Sistema de audio funcionando

## Instalación Paso a Paso

### 1️⃣ Preparar el Entorno

Abrir PowerShell en el directorio del proyecto:

```powershell
cd "c:\Users\sismt\OneDrive\Documentos\Desarrollo\Python\Metronomo"
```

### 2️⃣ Crear Entorno Virtual

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1
```

**Nota**: Si hay error de permisos, ejecutar:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3️⃣ Instalar Dependencias

```powershell
pip install -r requirements.txt
```

Esto instalará:
- `pygame` (reproducción de audio)
- `numpy` (generación de sonidos)

### 4️⃣ Ejecutar la Aplicación

```powershell
python main.py
```

## Verificación de Instalación

Para verificar que todo funciona correctamente:

```powershell
# Ejecutar tests
python -m pytest tests/ -v

# O con unittest
python -m unittest discover tests/
```

## Uso Rápido

### Interfaz Gráfica

```powershell
python main.py
```

Controles:
- **BPM Slider**: Ajustar tempo
- **Time Signature**: Seleccionar compás
- **Play/Pause**: Iniciar/pausar metrónomo
- **Stop**: Detener y resetear
- **Tap Tempo**: Calcular BPM tocando
- **Volume**: Ajustar volumen

### Uso Programático

Crear un archivo `test_metronome.py`:

```python
from src.controllers import MetronomeController
import time

# Crear controlador
with MetronomeController() as controller:
    # Configurar
    controller.set_bpm(120)
    controller.set_time_signature("4/4")
    
    # Iniciar
    controller.start()
    
    # Dejar correr 10 segundos
    time.sleep(10)
    
    # Se detiene automáticamente al salir del contexto

print("✅ Metrónomo funcionando correctamente!")
```

Ejecutar:
```powershell
python test_metronome.py
```

### Ejecutar Ejemplos

```powershell
python examples\basic_usage.py
```

## Solución de Problemas Comunes

### ❌ Error: "pygame not found"

```powershell
pip install pygame --upgrade
```

### ❌ Error: "numpy not found"

```powershell
pip install numpy --upgrade
```

### ❌ No se escucha sonido

1. Verificar que el volumen del sistema esté activado
2. Verificar que no esté en modo "Mute" en la aplicación
3. Los sonidos se generan automáticamente en `assets/sounds/`

### ❌ Error de permisos al crear archivos

El programa generará automáticamente:
- Sonidos en `assets/sounds/`
- Logs en `logs/`

Si hay error, verificar permisos de escritura.

### ❌ Error: "Import ... could not be resolved"

Verificar que el entorno virtual esté activado:
```powershell
.\venv\Scripts\Activate.ps1
```

## Estructura de Archivos Generados

Después de la primera ejecución, se crearán:

```
Metronomo/
├── assets/
│   └── sounds/
│       ├── accent.wav         # ✅ Generado
│       ├── normal.wav          # ✅ Generado
│       └── subdivision.wav     # ✅ Generado
│
└── logs/
    └── metronome.log          # ✅ Generado
```

## Configuración Avanzada

Editar `config/config.yaml`:

```yaml
metronome:
  default_bpm: 120
  default_time_signature: "4/4"

audio:
  sample_rate: 44100
  default_volume: 1.0

logging:
  level: INFO  # DEBUG para más detalles
```

## Desinstalación

```powershell
# Desactivar entorno virtual
deactivate

# Eliminar entorno virtual
Remove-Item -Recurse -Force venv

# Opcional: eliminar archivos generados
Remove-Item -Recurse -Force logs
Remove-Item -Recurse -Force assets\sounds
```

## Comandos Útiles

```powershell
# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Ver paquetes instalados
pip list

# Ejecutar con logging detallado
$env:PYTHONPATH="src"; python main.py

# Ejecutar tests específicos
python -m unittest tests.test_models

# Generar documentación de cobertura
python -m pytest --cov=src --cov-report=html tests/
```

## Desarrollo

Para desarrollar nueva funcionalidad:

1. Activar entorno virtual
2. Hacer cambios en `src/`
3. Agregar tests en `tests/`
4. Ejecutar tests: `python -m pytest tests/`
5. Verificar estilo: `flake8 src/` (si está instalado)

## Recursos Adicionales

- 📚 Ver `README.md` para descripción general
- 🏗️ Ver `docs/ARCHITECTURE.md` para detalles técnicos
- 📖 Ver `docs/USAGE.md` para ejemplos de uso
- 📁 Ver `docs/PROJECT_STRUCTURE.md` para estructura

## Soporte

Si encuentras problemas:

1. Verificar logs en `logs/metronome.log`
2. Ejecutar con modo DEBUG (editar `config/config.yaml`)
3. Revisar documentación en `docs/`
4. Abrir un issue en GitHub

## Siguiente Paso

¡Ya está todo listo! Ejecuta:

```powershell
python main.py
```

Y disfruta del Professional Metronome! 🎵
