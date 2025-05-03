# This Python file uses the following encoding: utf-8
# pyside6-uic .\ui_files\mainwindow.ui -o view_main_window.py
# pyside6-uic .\ui_files\main.ui > view_main_window.py
# pyside6-designer .\ui_files\mainwindow.ui      
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QVBoxLayout, QLabel, QDialog
from views.view_main_window import Ui_MainWindow
from models import Cam, OpenCvScreen, BypassFilter, ConsoleCom
from controllers import CamProvider, ScreenProvider, CvProvider, FilterProvider, ComProvider
import cv2

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GeneralCV")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":

    #=======================CONTROLLERS=================================================================

    camProvider = CamProvider()              # Inicializo el proevedor que controlara la camara
    screenProvider = ScreenProvider()        # Inicializo el proevedor que controlara la pantalla
    cvProvider = CvProvider()                # Inicializo el proevedor que controlara el modelo de cv
    inputFilterProvider = FilterProvider()   # Inicializo el proevedor que controlara el filtro que se le aplicaran al frame para luego aplicar cv
    outputFilterProvider = FilterProvider()  # Inicializo el proevedor que controlara el filtro que se le aplicara al frame para mostrar en pantalla
    comProvider = ComProvider()

    #=======================MODELOS=====================================================================

    cam = Cam()                              # Instancio el tipo de camara que voy a usar
    screen = OpenCvScreen()                  # Instancio el tipo de ventana donde voy a mostrar la salida
    cvModel = None                           # Instancio el modelo de CV
    inputFilter = BypassFilter()             # Instancio el filtro que tendra la entrada
    outputFilter = BypassFilter()            # Instancio el filtro que tendra la salida [lo que se mostrara en el screen]
    comModel = ConsoleCom()

    #=======================SELECCION DE MODELOS========================================================

    camProvider.setCam(cam)                  # Seteo la camara que voy a usar
    cvProvider.setCv(cvModel)                # Seteo el modelo de vision por computadora a usar
    inputFilterProvider.setFilter(inputFilter)    
    outputFilterProvider.setFilter(outputFilter)
    screenProvider.setScreen(screen)         # Seteo la pantalla en donde voy a mostrar los frames
    comProvider.setCom(comModel)             # Seteo el dispositivo de comunicacion que voy a usar

    #=======================Chequeo de informacion========================================================

    # camProvider.cam.showInfo()                
    # screenProvider.screen.showInfo()          
    # cvProvider.cv.showInfo()                 

    #=======================VIEW==========================================================================

    while True:
        frame = camProvider.getFrame()                         # Tomo un frame

        frameToCvProcess = inputFilterProvider.process(frame)  # Aplico un filtro a mi frame para luego procesarlo
        cvResponse = cvProvider.process(frameToCvProcess)      # Proceso el frame

        comProvider.process(cvResponse)                        # Comunico la respuesta a un periferico externo
        
        frame = outputFilterProvider.process(frame)            # Aplico un filtro a mi frame para luego mostrarlo en pantalla
        screenProvider.showFrame(frame)                        # Lo muestro en mi pantalla

        if cv2.waitKey(1) & 0xFF == ord('q'):                  # Si presiono 'q' el programa finaliza
            break

    #=======================Liberacion de recursos======================================================
    
    cam.realese()                            # Libero el recurso de camara
    screenProvider.destroyAllWindows()       # Elimino todas las pantallas del proevedor

    # app = QApplication(sys.argv)
    # widget = MainWindow()
    # widget.show()
    # sys.exit(app.exec())

    
