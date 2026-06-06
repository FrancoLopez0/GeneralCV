# Guía de Onboarding para Nuevos Contribuyentes

¡Bienvenido al proyecto **GeneralCV**! Este documento te guiará para que puedas comenzar a contribuir rápidamente al proyecto.

## Estructura del Proyecto

El proyecto está diseñado bajo una arquitectura fuertemente desacoplada usando el patrón **Provider/Strategy**. El núcleo reside en:
- `main.py`: Punto de entrada de la aplicación PySide6.
- `controllers/`: Proveedores que envuelven los modelos.
- `models/`: Donde debes colocar tus implementaciones (visión, filtros, comunicaciones).
- `widgets/`: Componentes dinámicos de UI (PySide6).
- `views/`: Vistas de UI generadas desde archivos `.ui` de QtDesigner.

## Cómo Añadir un Nuevo Modelo de Computer Vision (CV)

Para crear un nuevo módulo (por ejemplo, detección de rostros):

1. **Crea el archivo:** Añade un archivo `.py` dentro de `models/Cv/` (ej. `FaceDetectionCv.py`).
2. **Hereda de la interfaz:** Tu clase debe heredar de `iCv` (ubicada en `models.interfaces`).
3. **Implementa el método `process`:** Este es el método central que recibe el frame.

```python
from ..interfaces import iCv
import cv2

class FaceDetectionCv(iCv):
    def __init__(self):
        super().__init__()
        # Inicializa tus variables, cascadas, o modelos neuronales aquí
        
    def process(self, frame):
        # 1. Procesa el frame
        # 2. Dibuja sobre el frame
        # 3. Retorna la tupla: (frame_modificado, metadata_de_respuesta)
        return frame, {"faces_detected": 1}

    def close(self):
        # Libera recursos si es necesario
        pass
```

El modelo aparecerá automáticamente en el menú desplegable de la interfaz porque `main.py` escanea la carpeta `models/Cv/` al iniciar.

## Interfaz de Usuario Dinámica y el Decorador `@add_param`

Una de las características más potentes de GeneralCV es la **generación dinámica de UI**. Si quieres que tu modelo exponga un método para cambiar un parámetro (por ejemplo, ajustar la sensibilidad) o ejecutar una acción en tiempo real, puedes usar el decorador `@add_param`.

### ¿Cómo funciona?

1. Importa el decorador y los tipos (opcionalmente).
2. Decora un método dentro de tu clase.
3. Utiliza "Type Hints" (anotaciones de tipo) o valores por defecto para que el sistema sepa qué Widget (control de Qt) dibujar.

### Ejemplo Práctico

```python
from ..interfaces import iCv
from ..decorators import add_param
from ..types import ComboInputType, SliderInputType

class MyAwesomeCv(iCv):
    def __init__(self):
        super().__init__()
        self.threshold = 0.5
        self.mode = "fast"
        
    def process(self, frame):
        # Usa self.threshold y self.mode para modificar tu algoritmo
        return frame, True

    # 1. Botón simple (sin parámetros)
    @add_param
    def resetConfig(self):
        self.threshold = 0.5
        
    # 2. SpinBox decimal y SpinBox de enteros usando tipado y defaults
    @add_param
    def setThreshold(self, threshold: float = 0.5, max_objects: int = 5):
        self.threshold = threshold
        
    # 3. Text Input (String)
    @add_param
    def setName(self, name: str = "default_name"):
        pass

    # 4. Uso de Tipos Especiales (Slider y ComboBox)
    # Nota: El tipo determina el widget visual. El valor por defecto provee las opciones iniciales en el combo.
    @add_param
    def setAdvanced(self, sensibility: SliderInputType = 50, mode: ComboInputType = ["fast", "accurate"]):
        pass
```

Al seleccionar este modelo en la aplicación, la pestaña **CV** se poblará automáticamente con:
- Un botón **"resetConfig"**.
- Un input decimal **"threshold"** y uno entero **"max_objects"** asociados a un botón **"setThreshold"**.
- Un campo de texto **"name"** con un botón.
- Un slider horizontal y un menú desplegable (ComboBox) para ajustar configuraciones avanzadas.

¡No necesitas tocar código de PySide6 para hacer que tu algoritmo sea controlable gráficamente!

¡Feliz código y gracias por contribuir a GeneralCV!
