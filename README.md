# Estructura
![image](https://github.com/user-attachments/assets/80bc9482-24f0-4653-80c5-f11723ebcc03)

# GUI
Este programa utiliza Qt como medidador con el usuario.

Para actualizar el GUI se debe utilizar el comando:

`pyside6-uic .\ui_files\mainwindow.ui -o .\views\view_main_window.py`

# Modelos

El programa contempla cuatro tipos de modelos

* Cv (Computer Vision)
* Filter
* Com
* Screen

// nota: Actualmente el modelo Screen esta fijo para verse en Qt

Se pueden añadir modelos y automaticamente se importaran en el programa, para ello tener en cuenta la estructura de la carpeta models

- models
  - Cam
    En esta carpeta se encuentran los modelos de camaras (deben incluirse en el __ init __.py)
  - Cv
    En esta carpeta se incluiran los modelos de computer vision(deben incluirse en el __ init __.py)
  - Com
    En esta carpeta se encuentran los modelos que utilizara el modelo Cv para comunicarse con algun periferico (deben incluirse en el __ init __.py)
  - Filter
    En esta carpeta se encuentran todos los filtros (deben incluirse en el __ init __.py)
  - decorators
    Aqui se encuentran los decoradores que se utillizaran por ejemplo como @add_param el cual despliega automaticamente el menu para modificar parametros en el programa
  - types

# Decoradores

## Añadir parametros al menú
Se pueden modificar los parametros en tiempo real a traves del decorador @add_param 

![image](https://github.com/user-attachments/assets/eda23751-04d2-45d6-9098-1c9f67eada4a)
![image](https://github.com/user-attachments/assets/6d63d5f2-773d-4882-83ba-abd3efd9c2f4)

![image](https://github.com/user-attachments/assets/357c7317-fde2-4e5d-8931-0a82a3cfada4)
![image](https://github.com/user-attachments/assets/3c0a807f-96ec-4b8c-bcec-44a464685066)

Este proyecto utiliza Qt (PySide6) bajo licencia LGPL v3 para la interfaz gráfica de usuario.
Para más información sobre la licencia, ver: https://doc.qt.io/qtforpython/licenses.html
