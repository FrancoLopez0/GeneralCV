# This Python file uses the following encoding: utf-8
# pyside6-uic .\ui_files\mainwindow.ui -o view_main_window.py
# pyside6-uic .\ui_files\main.ui > view_main_window.py
# pyside6-uic .\ui_files\mainwindow.ui -o .\views\view_main_window.py
# pyside6-designer .\ui_files\mainwindow.ui      
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QVBoxLayout, QLabel, QDialog
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from views.view_main_window import Ui_MainWindow
from models import Cam, OpenCvScreen, BypassFilter, ConsoleCom, HandsCv, QtScreen
from controllers import CamProvider, ScreenProvider, CvProvider, FilterProvider, ComProvider
import cv2

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GeneralCV")

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.ui.cbSelectModel.addItems(['None','Hand'])
        self.ui.cbSelectModel.currentTextChanged.connect(self.select_cv_model)

        #=======================CONTROLLERS=================================================================

        self.camProvider = CamProvider()              # Inicializo el proevedor que controlara la camara
        self.screenProvider = ScreenProvider()        # Inicializo el proevedor que controlara la pantalla
        self.cvProvider = CvProvider()                # Inicializo el proevedor que controlara el modelo de cv
        self.inputFilterProvider = FilterProvider()   # Inicializo el proevedor que controlara el filtro que se le aplicaran al frame para luego aplicar cv
        self.outputFilterProvider = FilterProvider()  # Inicializo el proevedor que controlara el filtro que se le aplicara al frame para mostrar en pantalla
        self.comProvider = ComProvider()              # Inicializo el proevedor que controlara la comunicacion con hardware/software externo

        #=======================MODELOS=====================================================================

        cam = Cam()                                   # Instancio el tipo de camara que voy a usar
        # self.screen = OpenCvScreen()                # Instancio el tipo de ventana donde voy a mostrar la salida
        cvModel = None                                # Instancio el modelo de CV
        inputFilter = BypassFilter()                  # Instancio el filtro que tendra la entrada
        outputFilter = BypassFilter()                 # Instancio el filtro que tendra la salida [lo que se mostrara en el screen]
        comModel = ConsoleCom()
        screen = QtScreen(self.ui.cam)                  # Instancio el tipo de ventana donde voy a mostrar la salida

        #=======================SELECCION DE MODELOS========================================================

        self.camProvider.setCam(cam)                  # Seteo la camara que voy a usar
        self.cvProvider.setCv(cvModel)                # Seteo el modelo de vision por computadora a usar
        self.inputFilterProvider.setFilter(inputFilter)    
        self.outputFilterProvider.setFilter(outputFilter)
        self.screenProvider.setScreen(screen)         # Seteo la pantalla en donde voy a mostrar los frames
        self.comProvider.setCom(comModel)             # Seteo el dispositivo de comunicacion que voy a usar

        # Timer para actualizar el frame cada 30 ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def select_cv_model(self, value):
        
        self.cvProvider.close()

        if(value=='Hand'):
            self.cvProvider.setCv(HandsCv())

        print(value)
    
    def show_on_qt(self, frame):
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # Mostrar la imagen en el QLabel
        self.ui.cam.setPixmap(QPixmap.fromImage(q_image))

    def update_frame(self):
        
        frame = self.camProvider.getFrame()                         # Tomo un frame
        
        frameToCvProcess = self.inputFilterProvider.process(frame)  # Aplico un filtro a mi frame para luego procesarlo
        
        frame,cvResponse = self.cvProvider.process(frameToCvProcess)      # Proceso el frame
        
        self.comProvider.process(frame)                        # Comunico la respuesta a un periferico externo
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = self.outputFilterProvider.process(frame)            # Aplico un filtro a mi frame para luego mostrarlo en pantalla

        self.screenProvider.showFrame(frame)
    
    def close(self):
        self.cvProvider.close()  
        self.cam.realese()                            # Libero el recurso de camara
        return super().close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

# if __name__ == "__main__":

#     #=======================CONTROLLERS=================================================================

#     camProvider = CamProvider()              # Inicializo el proevedor que controlara la camara
#     screenProvider = ScreenProvider()        # Inicializo el proevedor que controlara la pantalla
#     cvProvider = CvProvider()                # Inicializo el proevedor que controlara el modelo de cv
#     inputFilterProvider = FilterProvider()   # Inicializo el proevedor que controlara el filtro que se le aplicaran al frame para luego aplicar cv
#     outputFilterProvider = FilterProvider()  # Inicializo el proevedor que controlara el filtro que se le aplicara al frame para mostrar en pantalla
#     comProvider = ComProvider()              # Inicializo el proevedor que controlara la comunicacion con hardware/software externo

#     #=======================MODELOS=====================================================================

#     cam = Cam()                              # Instancio el tipo de camara que voy a usar
#     screen = OpenCvScreen()                  # Instancio el tipo de ventana donde voy a mostrar la salida
#     cvModel = HandsCv()                      # Instancio el modelo de CV
#     inputFilter = BypassFilter()             # Instancio el filtro que tendra la entrada
#     outputFilter = BypassFilter()            # Instancio el filtro que tendra la salida [lo que se mostrara en el screen]
#     comModel = ConsoleCom()

#     #=======================SELECCION DE MODELOS========================================================

#     camProvider.setCam(cam)                  # Seteo la camara que voy a usar
#     cvProvider.setCv(cvModel)                # Seteo el modelo de vision por computadora a usar
#     inputFilterProvider.setFilter(inputFilter)    
#     outputFilterProvider.setFilter(outputFilter)
#     screenProvider.setScreen(screen)         # Seteo la pantalla en donde voy a mostrar los frames
#     comProvider.setCom(comModel)             # Seteo el dispositivo de comunicacion que voy a usar

#     #=======================Chequeo de informacion========================================================

#     # camProvider.cam.showInfo()                
#     # screenProvider.screen.showInfo()          
#     # cvProvider.cv.showInfo()                 

#     #=======================VIEW==========================================================================

#     while True:
#         frame = camProvider.getFrame()                         # Tomo un frame

#         frameToCvProcess = inputFilterProvider.process(frame)  # Aplico un filtro a mi frame para luego procesarlo
#         cvResponse = cvProvider.process(frameToCvProcess)      # Proceso el frame

#         comProvider.process(cvResponse)                        # Comunico la respuesta a un periferico externo
        
#         frame = outputFilterProvider.process(frame)            # Aplico un filtro a mi frame para luego mostrarlo en pantalla
#         screenProvider.showFrame(cvResponse)                        # Lo muestro en mi pantalla

#         if cv2.waitKey(1) & 0xFF == ord('q'):                  # Si presiono 'q' el programa finaliza
#             break

#     #=======================Liberacion de recursos======================================================
    
#     cvProvider.close()                       # Libero los recursos tomados por el modelo de CV
#     cam.realese()                            # Libero el recurso de camara
#     screenProvider.destroyAllWindows()       # Elimino todas las pantallas del proevedor
    
