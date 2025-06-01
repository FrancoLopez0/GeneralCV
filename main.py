# This Python file uses the following encoding: utf-8
# pyside6-uic .\ui_files\mainwindow.ui -o view_main_window.py
# pyside6-uic .\ui_files\main.ui > view_main_window.py
# pyside6-uic .\ui_files\mainwindow.ui -o .\views\view_main_window.py
# pyside6-designer .\ui_files\mainwindow.ui      
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDoubleSpinBox, QSpinBox, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from views.view_main_window import Ui_MainWindow
from models import Cam, OpenCvScreen, BypassFilter, ConsoleCom, HandsCv, QtScreen, HandTrackingCv, CannyFilter
from controllers import CamProvider, ScreenProvider, CvProvider, FilterProvider, ComProvider
import cv2

class MyCustomTab(QWidget):
    def __init__(self, methods, name):
        super().__init__()
        
        h = 25

        layout = QHBoxLayout()

        layout.addWidget(QLabel(name), alignment=Qt.AlignCenter)

        for method in methods:
            params = [param for param in methods[method]['parametros']]
            inputs = {}
            func_layout = QVBoxLayout()
            for param, param_type in methods[method]['parametros'].items():
                param_layout = QHBoxLayout()

                label = QLabel(param)

                label.setFixedHeight(h)

                param_layout.addWidget(label, alignment=Qt.AlignCenter)

                if(param_type == str):
                    var_widget=QLineEdit(param)
                if(param_type == float):
                    var_widget = QDoubleSpinBox(maximum=1000)
                if(param_type == int):
                    var_widget = QSpinBox(maximum=1000)
                inputs[param] = var_widget

                param_layout.addWidget(var_widget, alignment=Qt.AlignCenter)

                func_layout.addLayout(param_layout)
            
            layout.addLayout(func_layout)

            btn = QPushButton(method)

            btn.setFixedHeight(h)

            fun = self.make_callback(methods[method]['funcion'], inputs)

            btn.clicked.connect(fun)

            layout.addWidget(btn, alignment=Qt.AlignCenter)   
        
        layout.addStretch()         

        self.setLayout(layout)

    
    def make_callback(self, func, inputs):
        def callback():
            args = {}
            for k, widget in inputs.items():
                if isinstance(widget, QLineEdit):
                    args[k] = widget.text()
                else:
                    args[k] = widget.value()
            func(**args)
        return callback

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GeneralCV")

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.ui.parameters.removeTab(0)
        self.ui.parameters.removeTab(1)
        self.ui.parameters.removeTab(2)

        self.camWidget = QWidget()
        self.cvWidget = QWidget()
        self.iFilterWidget = QWidget()
        self.oFilterWidget = QWidget()
        self.comWidget = QWidget()

        self.ui.parameters.addTab(self.camWidget, 'CAM')
        self.ui.parameters.addTab(self.iFilterWidget, 'IFilter')
        self.ui.parameters.addTab(self.cvWidget, 'CV')
        self.ui.parameters.addTab(self.oFilterWidget, 'OFilter')
        self.ui.parameters.addTab(self.comWidget, 'COM')

        self.ui.parameters.removeTab(0)


        self.ui.cbSelectModel.addItems(['None','Hand', 'Hand Tracking'])
        self.ui.cbSelectModel.currentTextChanged.connect(self.select_cv_model)

        self.ui.cbSelectOuputFilter.addItems(['None', 'Border'])
        self.ui.cbSelectOuputFilter.currentTextChanged.connect(self.select_output_filter_model)

        self.ui.cbSelectInputFilter.addItems(['None', 'Border'])
        self.ui.cbSelectInputFilter.currentTextChanged.connect(self.select_input_filter_model)

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

    def select_input_filter_model(self, value):
        if(value == 'None'):
            self.inputFilterProvider.setFilter(BypassFilter())
        if(value=='Border'):
            self.inputFilterProvider.setFilter(CannyFilter())
        
        methods = self.outputFilterProvider.getMethods()
        self.update_tab(1, value, methods, 'OFilter')
        
        print(value)

    def select_output_filter_model(self, value):

        if(value == 'None'):
            self.outputFilterProvider.setFilter(BypassFilter())
        if(value=='Border'):
            self.outputFilterProvider.setFilter(CannyFilter())
        
        methods = self.outputFilterProvider.getMethods()
        self.update_tab(3, value, methods, 'OFilter')

        print(value)

    def select_cv_model(self, value):
        
        self.cvProvider.close()

        if(value=='Hand'):
            self.cvProvider.setCv(HandsCv())
        
        if(value=='Hand Tracking'):
            self.cvProvider.setCv(HandTrackingCv())

        print(f'Modelo seleccionado: {value}')

        methods = self.cvProvider.getMethods()

        self.update_tab(2, value, methods, 'CV')


    def update_tab(self, index, name, methods, tab_name):
        tab = MyCustomTab(methods, name)
        self.ui.parameters.removeTab(index)
        self.ui.parameters.insertTab(index,tab, tab_name)

    def show_on_qt(self, frame):
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # Mostrar la imagen en el QLabel
        self.ui.cam.setPixmap(QPixmap.fromImage(q_image))

    def update_frame(self):
        
        frame = self.camProvider.getFrame()                         # Tomo un frame
        
        frameToCvProcess = self.inputFilterProvider.process(frame)  # Aplico un filtro a mi frame para luego procesarlo
        
        frame,cvResponse = self.cvProvider.process(frameToCvProcess)# Proceso el frame
        
        self.comProvider.process(frame)                             # Comunico la respuesta a un periferico externo
        
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
    
