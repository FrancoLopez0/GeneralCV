# Guía para Implementar un Módulo de Cámara de Red (Network Cam)

Esta guía detalla los requisitos y la arquitectura necesarios para implementar un nuevo módulo de cámara (modelo `Cam`) en GeneralCV que se conecte a un servidor y obtenga los frames de video mediante peticiones HTTP.

## 1. Importaciones Requeridas
Para que el módulo funcione correctamente, asegúrate de incluir las siguientes importaciones en tu archivo:

```python
import cv2
import numpy as np
import requests

# Importaciones específicas de GeneralCV (ajusta las rutas según la estructura de tu proyecto)
from core.interfaces.icam import iCam
from core.decorators import add_param
```

## 2. Estructura de la Clase e Interfaz
Tu nueva clase de cámara debe heredar de la interfaz `iCam`. Esto asegura que el sistema reconozca tu módulo y pueda interactuar con él de manera estandarizada.

Debes implementar obligatoriamente los siguientes métodos:

- `__init__(self, **kwargs)`: Constructor de la clase. Aquí debes inicializar las variables, obtener los parámetros de configuración y, de ser necesario, realizar una comprobación inicial de conexión con el servidor.
- `get_frame(self)`: Este es el núcleo de la cámara. Debe realizar la petición HTTP al servidor, obtener los bytes de la imagen y retornar el frame procesado (ver sección 4). Si la petición falla, debe manejar la excepción y devolver un frame vacío o indicar el error.
- `release(self)`: Método para liberar recursos. En el caso de peticiones HTTP simples (REST) puede no ser estrictamente necesario cerrar una conexión como en un socket o una cámara USB, pero debes asegurarte de limpiar cualquier estado interno o sesión si usas `requests.Session()`.

Ejemplo de estructura básica:
```python
class NetworkCam(iCam):
    def __init__(self, **kwargs):
        super().__init__()
        # Inicialización y validación de la URL
        self.server_url = kwargs.get('server_url', 'http://127.0.0.1:5000/video_feed')
        # Opcional: testear conexión inicial aquí
        
    def get_frame(self):
        # Lógica de petición y conversión de frame
        pass
        
    def release(self):
        # Limpieza de recursos
        pass
```

## 3. Integración con el Proveedor (Provider)
Para que el usuario pueda configurar la URL del servidor dinámicamente desde la interfaz de usuario de PySide6, debes utilizar el decorador `@add_param` (o el sistema de parámetros correspondiente del proyecto) sobre tu clase.

Esto expondrá el parámetro en la UI (a través del `CamProvider`), permitiendo su modificación en tiempo de ejecución sin cambiar el código fuente.

Ejemplo:
```python
@add_param(name="server_url", type=str, default="http://192.168.1.100:8080/shot.jpg", description="URL del servidor para obtener el frame")
class NetworkCam(iCam):
    # La implementación de la clase...
```

## 4. Conversión de Datos (Petición HTTP a OpenCV)
Dentro del método `get_frame()`, recibirás una respuesta cruda (bytes) del servidor. Para convertir esto en un arreglo de numpy compatible con OpenCV, debes seguir estos pasos:

1. Realizar la petición GET.
2. Extraer los bytes del contenido (`response.content`).
3. Convertir los bytes a un arreglo unidimensional de numpy de tipo `uint8`.
4. Decodificar este arreglo usando `cv2.imdecode` para obtener el frame final en formato BGR.

Ejemplo de implementación en `get_frame()`:
```python
def get_frame(self):
    try:
        # 1. Hacer la petición HTTP
        response = requests.get(self.server_url, timeout=2.0)
        response.raise_for_status() # Lanza excepción si el código HTTP indica error
        
        # 2. y 3. Convertir bytes a arreglo numpy (uint8)
        img_array = np.frombuffer(response.content, dtype=np.uint8)
        
        # 4. Decodificar la imagen a un formato OpenCV (BGR)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        return frame
    except Exception as e:
        # Opcional: Loguear el error
        print(f"Error al obtener frame de {self.server_url}: {e}")
        return None
```
