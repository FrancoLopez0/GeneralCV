# Patrones de Diseño y Estructura del Proyecto

## Patrones de Diseño Utilizados

El proyecto GeneralCV utiliza una combinación de patrones de diseño modernos que le permiten ser dinámico, escalable y muy flexible:

### 1. Patrón Strategy y Provider
El sistema hace un uso intensivo del patrón **Strategy**, gestionado a través de **Providers** (proveedores). En `controllers/`, encontramos clases como `CvProvider`, `CamProvider`, etc., que extienden de `BaseProvider`. 
Estos *Providers* actúan como un contexto que mantiene una referencia a una *Estrategia* concreta (el modelo seleccionado). En tiempo de ejecución, el usuario puede seleccionar un filtro diferente o un modelo de CV diferente; el sistema reemplaza el modelo instanciado en el *Provider* sin alterar la lógica de alto nivel. 
- *Ejemplo*: `cvProvider.setCv(cvModel)` permite intercambiar algoritmos sin afectar el flujo del programa.

### 2. Metaprogramación y Reflexión (Reflection) para UI Dinámica
Uno de los patrones más interesantes de este proyecto es la generación de interfaces gráficas guiada por código (Reflection). 
- **Decorador `@add_param`**: Ubicado en `models/decorators/add_param.py`, marca los métodos de los modelos con un atributo especial (`__is_param__ = True`).
- **Inspección en `BaseProvider`**: Mediante el módulo `inspect` de Python, `BaseProvider.getMethods()` escanea el modelo instanciado buscando métodos marcados y analiza las firmas de sus funciones y sus anotaciones de tipo (int, float, str, tipos custom).
- **Generación en `MyCustomTab`**: Se genera automáticamente la UI (botones, inputs, sliders) mapeando los tipos de datos requeridos por las funciones a los correspondientes Widgets de PySide6, y creando un *callback* (closure) para pasar los parámetros ingresados. Esto evita programar UIs específicas para cada modelo de CV.

### 3. Patrón Pipeline
En el archivo `main.py` (método `update_frame`), el sistema aplica un patrón de tubería (*Pipeline*) clásico. El dato (el frame de video) atraviesa una secuencia de transformaciones y procesos en un orden estricto:
`Camara -> Filtro de Entrada -> Modelo CV -> Envío de Datos (Com) -> Filtro de Salida -> Pantalla`.
Este enfoque asegura que los componentes están débilmente acoplados, ya que cada uno solo espera recibir un dato, modificarlo y retornar el resultado a la cadena.

---

## Estructura de Directorios

La organización del código fuente promueve la separación de responsabilidades:

- `/assets` y `/images`: Recursos estáticos utilizados por la aplicación, tales como logos o iconos.
- `/controllers`: Contiene los *Providers* (`BaseProvider`, `CamProvider`, `CvProvider`, etc.). Funcionan como intermediarios entre el ciclo principal del programa y la lógica específica de los modelos.
- `/docs`: Documentación técnica del proyecto (donde residen estos archivos).
- `/models`: El núcleo de la lógica de negocio y procesamiento.
  - `/models/interfaces`: Define los contratos (`iCv.py`, `iCam.py`, `iFilter.py`) que los diferentes modelos deben implementar para ser compatibles con los *Providers*.
  - `/models/decorators`: Aloja herramientas de metaprogramación como `add_param.py` para exponer funciones a la UI.
  - `/models/types`: Tipos de datos personalizados que dictan cómo la UI debe representar variables específicas (por ejemplo, `ComboInputType` o `SliderInputType`).
  - Subdirectorios específicos (`Cam`, `Com`, `Cv`, `Filter`, `Screen`): Agrupan las implementaciones concretas para cada parte del pipeline. Por ejemplo, en `/models/Cv` estarán los scripts de los algoritmos de IA/Computer Vision.
- `/views` y `/ui_files`: Archivos relacionados con la estructura visual de la interfaz. Pueden contener código autogenerado por herramientas como Qt Designer (`view_main_window.py`).
- `/widgets`: Elementos gráficos personalizados de PySide6, destacando `MyCustomTab.py`, que es el encargado de parsear el diccionario de métodos y construir dinámicamente los controles de parámetros en la pantalla.
- `main.py`: Punto de entrada del programa. Enlaza todas las piezas: UI, Providers, y el Timer que acciona el *Pipeline* iterativo.
