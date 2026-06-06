# Plan de Ataque: Módulo Com para Control de ESP32 vía HTTP

Este documento detalla los requerimientos y pasos para implementar un nuevo módulo `Com` en GeneralCV que tome los datos de seguimiento de manos (`HandsCv`), convierta las posiciones a ángulos de paneo (pan) e inclinación (tilt), y los envíe vía peticiones HTTP a un ESP32.

## 1. Requerimientos de la Interfaz
- **Clase Base:** El nuevo módulo debe heredar de la interfaz/clase base `iCom` para integrarse correctamente con la arquitectura del sistema.
- **Implementación de Métodos:** Debes implementar obligatoriamente los métodos requeridos por la interfaz, en particular el método `send(data)`.

## 2. Extracción de Datos
- **Recepción de la Estructura:** El método `send(data)` recibirá la estructura de datos que retorna `HandsCv`.
- **Lectura de Coordenadas:** Es necesario acceder a las coordenadas (X, Y) de los puntos de referencia de la mano (landmarks) extraídos por `HandsCv`, como la punta del dedo índice o el centro de la palma, para utilizarlos como guía para el movimiento de los servos.

## 3. Mapeo Matemático (Coordenadas a Ángulos)
- **Mapeo Lineal:** Para controlar los servomotores, debes mapear el rango de resolución de pantalla al rango de grados del servo.
- **Función de Mapeo:** Implementa una función similar a `map()` de Arduino. Si la pantalla o imagen es de `640x480`, y los servos operan entre `0` y `180` grados:
  - Para X (Pan): Mapear el rango `[0, 640]` a `[0, 180]`.
  - Para Y (Tilt): Mapear el rango `[0, 480]` a `[0, 180]`.

## 4. Optimización de Red y Concurrencia (¡CRÍTICO!)
- **Peligro de Bloqueo de la UI:** **NUNCA** realices una petición HTTP bloqueante (como `requests.get(...)` o `requests.post(...)`) directamente dentro del método `send()`. Las llamadas de red son lentas y hacer esto congelará el `QTimer` principal de PySide6, trabando toda la interfaz gráfica del usuario y arruinando los FPS del video.
- **Solución Asíncrona:** Debes lanzar las peticiones HTTP en segundo plano. Para esto, utiliza un hilo en segundo plano (`threading.Thread`) o un sistema de cola (`queue.Queue`) con un hilo trabajador. El método `send()` debe limitarse a depositar las coordenadas o ángulos en la cola y retornar inmediatamente, dejando que el hilo en segundo plano realice las peticiones de red al ESP32.

## 5. Integración con la Interfaz de Usuario (UI)
- **Configuración Dinámica:** Utiliza el decorador `@add_param` provisto por GeneralCV para permitir que los parámetros del módulo se puedan editar desde la GUI.
- **Parámetro de IP:** Registra la IP o la URL del ESP32 utilizando `@add_param` (ej. `@add_param(name="ESP32 URL", default="http://192.168.1.100")`). De esta manera, el usuario podrá modificar dinámicamente el destino de los comandos HTTP sin tener que modificar el código fuente.
