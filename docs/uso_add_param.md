# Guía de Uso del Decorador `@add_param`

El decorador `@add_param` es una herramienta poderosa en este proyecto que permite generar automáticamente la interfaz de usuario (UI) a partir del código de las clases. 

## 1. La "Magia" detrás de `@add_param`

La magia de `@add_param` reside en el uso de **reflexión y metaprogramación** en Python. Cuando decoras un método con `@add_param`, el sistema inspecciona automáticamente:
1. El nombre del método y sus parámetros.
2. Las **anotaciones de tipo** (type hints) de cada parámetro.

Al analizar las firmas de los métodos en tiempo de ejecución, el sistema sabe exactamente qué tipo de dato se espera. Basado en esto, genera automáticamente el componente gráfico apropiado (un widget de PySide6) en el panel de control del usuario, vinculando la entrada del usuario directamente al método subyacente. Todo esto sucede sin necesidad de escribir código UI adicional para cada parámetro.

## 2. Tipos de Datos Soportados

El decorador soporta múltiples tipos de datos, generando diferentes widgets dependiendo del tipo especificado en la firma del método.

### Tipos Básicos

Los tipos estándar de Python se mapean a componentes comunes de la interfaz gráfica:

```python
from utils.param_decorator import add_param

class MiFiltro:
    # Genera un campo de texto (QLineEdit)
    @add_param
    def set_nombre(self, nombre: str):
        self.nombre = nombre

    # Genera un control numérico de enteros (QSpinBox)
    @add_param
    def set_cantidad(self, cantidad: int):
        self.cantidad = cantidad

    # Genera un control numérico decimal (QDoubleSpinBox)
    @add_param
    def set_umbral(self, umbral: float):
        self.umbral = umbral

    # Genera una casilla de verificación (QCheckBox)
    @add_param
    def set_activado(self, activado: bool):
        self.activado = activado
```

### Tipos Personalizados

Para controles más avanzados o específicos, el proyecto define tipos especiales:

```python
from utils.custom_types import SliderInputType, ComboInputType

class MiProcesador:
    # Genera un deslizador (QSlider) con rango definido
    @add_param
    def set_brillo(self, brillo: SliderInputType(min=0, max=100, default=50)):
        self.brillo = brillo.value

    # Genera un menú desplegable (QComboBox) con opciones fijas
    @add_param
    def set_color(self, color: ComboInputType(options=["Rojo", "Verde", "Azul"], default="Verde")):
        self.color = color.value
```

## 3. Ejemplo Práctico: Modificando la clase `Esp32_cam`

Supongamos que queremos añadir la capacidad de cambiar la URL del servidor de la cámara ESP32 en tiempo de ejecución desde la interfaz gráfica.

Solo necesitamos añadir un método `set_url` a la clase `Esp32_cam`, agregarle las anotaciones de tipo adecuadas (en este caso, `str`) y decorarlo con `@add_param`.

```python
from utils.param_decorator import add_param

class Esp32_cam:
    def __init__(self):
        self.url = "http://192.168.1.100/cam-hi.jpg"
        # Inicialización de la cámara...
    
    # Este método generará automáticamente un campo de texto en la UI.
    # Cuando el usuario escriba una nueva URL,
    # el sistema llamará a este método automáticamente con la nueva cadena.
    @add_param
    def set_url(self, nueva_url: str):
        """Actualiza la URL de la cámara desde la UI."""
        print(f"Actualizando URL de la cámara a: {nueva_url}")
        self.url = nueva_url
        # Aquí se añadiría la lógica para reconectar la cámara a la nueva URL
```

Con solo estas líneas de código, la interfaz mostrará automáticamente una entrada de texto interactiva que controla directamente la instancia de `Esp32_cam`. No es necesario modificar ningún archivo relacionado a las vistas (V) o controladores (C) de la interfaz gráfica.
