# Arquitectura General de GeneralCV

El proyecto **GeneralCV** presenta una arquitectura modular y extensible diseñada para facilitar la integración, visualización y procesamiento de flujos de video mediante visión por computadora (Computer Vision). 

La arquitectura general se puede dividir en tres subsistemas principales que interactúan de forma fluida:

## 1. Subsistema de Interfaz de Usuario (PySide6 UI)
La interfaz de usuario está construida con el framework **PySide6**. Está diseñada para ser dinámica, permitiendo a los usuarios intercambiar componentes en tiempo de ejecución (como cámaras, modelos de CV, filtros y módulos de comunicación).
- **Ventana Principal (`main.py`)**: Coordina la inicialización de la interfaz, el ciclo de vida de los componentes y la actualización periódica (usando `QTimer`) de los cuadros (frames) procesados.
- **Generación Dinámica de UI**: Gracias al uso de introspección (reflection), las pestañas de parámetros de la UI (`MyCustomTab`) se construyen automáticamente en base a las funciones de los modelos que se han seleccionado, interpretando sus anotaciones de tipo para generar controles (Sliders, ComboBoxes, SpinBoxes, etc.).

## 2. Subsistema del Núcleo de Visión por Computadora (Computer Vision Core)
Este subsistema aloja la lógica pura de procesamiento de imágenes e inferencia de modelos. Está altamente desacoplado del resto de la aplicación, lo que significa que agregar un nuevo modelo de CV o un nuevo filtro de imagen es tan simple como crear un nuevo archivo en el directorio correspondiente (`models/Cv` o `models/Filter`) que implemente la interfaz base. 
Los modelos son envueltos (wrapped) por los *Providers* correspondientes, los cuales administran la configuración, el estado y proporcionan una interfaz estándar para que el sistema central se comunique con ellos.

## 3. Pipeline de Procesamiento de Frames
El flujo de datos del sistema sigue un modelo de *Pipeline* bien definido que se ejecuta de forma iterativa y continua (habitualmente cada 30 ms):

1. **Adquisición (`CamProvider`)**: Se obtiene un cuadro (frame) crudo del dispositivo de captura seleccionado.
2. **Pre-procesamiento (`InputFilterProvider`)**: Se aplica un filtro opcional al cuadro de entrada para adecuarlo antes del análisis (por ejemplo, corrección de color, recortes, o bypass).
3. **Inferencia (`CvProvider`)**: El cuadro pre-procesado se envía al modelo de CV. El modelo retorna el cuadro con anotaciones visuales y una respuesta/metadatos sobre lo que detectó.
4. **Comunicación (`ComProvider`)**: Los resultados o metadatos extraídos por el modelo de CV (por ejemplo, coordenadas, clases detectadas, etc.) se envían a periféricos, consolas, o se comunican por puertos serie/red.
5. **Post-procesamiento (`OutputFilterProvider`)**: Se aplica un filtro final a la imagen (a menudo para adaptarla al espacio de color requerido por la interfaz o añadir efectos adicionales).
6. **Visualización (`ScreenProvider`)**: El cuadro resultante se muestra al usuario a través del componente Qt de la interfaz gráfica.

## Enfoque Modular y Diseño del Sistema
El diseño del sistema busca que **las piezas de software sean independientes e intercambiables en caliente (hot-swappable)**. Para lograr esto, `main.py` lee dinámicamente el contenido de los directorios de los modelos y permite al usuario seleccionarlos en la UI. Mediante `importlib`, el sistema instancia las clases solicitadas y las inyecta en los proveedores (*Providers*), modificando el comportamiento del Pipeline en tiempo real sin necesidad de reiniciar la aplicación.
