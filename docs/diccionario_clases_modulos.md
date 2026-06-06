# Diccionario de Clases y Módulos

Esta referencia detalla la estructura principal de paquetes, módulos y clases de **GeneralCV**.

## Módulos de Controladores (`controllers/`)

Los controladores actúan como envoltorios (Wrappers) o Contextos bajo el patrón Strategy. Ellos manejan una interfaz estandarizada y exponen los métodos dinámicos de los modelos subyacentes.

- **`BaseProvider`**: Clase base de la que heredan los demás proveedores. Contiene la lógica de reflexión (`getMethods()`) para analizar la instancia actual, buscando métodos decorados con `@add_param` para exponerlos en la UI.
- **`CamProvider`**: Administra la instancia de la cámara (`iCam`).
- **`CvProvider`**: Administra el modelo de visión artificial (`iCv`).
- **`FilterProvider`**: Administra los modelos de filtros de imagen (`iFilter`). Se instancia dos veces en la aplicación (Filtro de Entrada y Filtro de Salida).
- **`ComProvider`**: Administra la comunicación de datos hacia periféricos u otros sistemas (`iCom`).
- **`ScreenProvider`**: Gestiona el componente donde se muestran las imágenes (`iScreen`).

## Módulos de Modelos (`models/`)

Esta carpeta contiene la implementación real de las estrategias. Están agrupadas por su rol en el flujo del sistema.

### Interfaces (`models/interfaces/`)
Contiene las clases abstractas o interfaces (como `iCv`, `iCam`, `iFilter`, `iCom`) que dictan los métodos obligatorios (ej. `process`, `close`, `getData`) que cualquier modelo nuevo debe implementar.

### Modelos de Visión (`models/Cv/`)
- **`HandsCv`**, **`HandTrackingCv`**, **`FingersTrackingCv`**: Implementaciones concretas basadas en MediaPipe para la detección, seguimiento de manos y clasificación de estados de los dedos.

### Modelos de Filtros, Cámaras y Com
Cada subcarpeta (`Cam/`, `Filter/`, `Com/`, `Screen/`) alberga implementaciones concretas. Por ejemplo, en filtros podría existir un `BypassFilter` (que no hace nada) o un filtro de escala de grises.

## Decoradores y Tipos Especiales

### `models/decorators/add_param.py`
Proporciona el decorador `@add_param`.
- **Propósito**: Marca los métodos internos de un modelo (`func.__is_param__ = True`) para que el `BaseProvider` los detecte vía reflexión.
- **Uso**: Permite que, dinámicamente, se genere un botón o un control en la interfaz de usuario en tiempo de ejecución.

### `models/types/`
Contiene definiciones de tipos customizados para la UI.
- **`ComboInputType`**, **`SliderInputType`**: Clases vacías usadas para realizar un "Type Hinting" (anotación de tipos) en los métodos decorados con `@add_param`. Le informan al creador de pestañas qué tipo de widget visual generar (`QComboBox`, `QSlider`, etc.).

## Interfaz Gráfica (`widgets/` y `views/`)

### `widgets/MyCustomTab.py`
Clase clave en la generación dinámica de UI. 
- Analiza la firma (`inspect.signature`) de los métodos extraídos por los controladores.
- Dependiendo de los tipos de argumentos (`int`, `float`, `str`, `ComboInputType`), crea al vuelo widgets como `QSpinBox`, `QDoubleSpinBox`, `QLineEdit` o `QComboBox`.
- Empaqueta todo en una pestaña (`QWidget`) inyectada en el `QTabWidget` de los parámetros de la interfaz principal.

### `main.py`
El núcleo orquestador. Importa todos los componentes, inicializa las ventanas, descubre modelos leyendo los archivos del disco (`os.listdir`) y une los proveedores al temporizador del frame.
