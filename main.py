from pygrabber.dshow_graph import FilterGraph
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPlainTextEdit
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap, QIcon
from views.view_main_window import Ui_MainWindow
import importlib
from models import *
from controllers import CamProvider, ScreenProvider, CvProvider, FilterProvider, ComProvider
from widgets import MyCustomTab
import cv2_enumerate_cameras 
import cv2
import os

models_cam = [f.replace(".py", "") for f in os.listdir("./models/Cam") if os.path.isfile(os.path.join("./models/Cam", f))][:-1]
models_com = [f.replace(".py", "") for f in os.listdir("./models/Com") if os.path.isfile(os.path.join("./models/Com", f))][:-1]
models_cv = [f.replace(".py", "") for f in os.listdir("./models/Cv") if os.path.isfile(os.path.join("./models/Cv", f))][:-1]
models_filter = [f.replace(".py", "") for f in os.listdir("./models/Filter") if os.path.isfile(os.path.join("./models/Filter", f))][:-1]

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GeneralCV")
        image = QImage()
        image.load("./assets/lab.jpg")
        icon = QIcon()
        icon.addPixmap(QPixmap.fromImage(image))
        self.setWindowIcon(icon)

        print("=====================MODELOS IMORTADOS===========================")
        print(models_cam) 
        print(models_cv )
        print(models_com)
        print(models_filter)
        print("=================================================================")

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

        self.console = QLabel("Hola")

        self.ui.parameters.addTab(self.console, 'Console')

        self.ui.cbSelectModel.addItems(['None']+models_cv)
        self.ui.cbSelectModel.currentTextChanged.connect(self.select_cv_model)

        self.ui.cbSelectOuputFilter.addItems(['None']+models_filter)
        self.ui.cbSelectOuputFilter.currentTextChanged.connect(self.select_output_filter_model)

        self.ui.cbSelectInputFilter.addItems(['None']+models_filter)
        self.ui.cbSelectInputFilter.currentTextChanged.connect(self.select_input_filter_model)

        self.ui.cbSelectCam.currentTextChanged.connect(self.select_cam)

        self.ui.cbSelectCom.addItems(['None']+models_com)
        self.ui.cbSelectCom.currentTextChanged.connect(self.select_com)

        self.ui.btnScan.clicked.connect(self.list_cameras)

        self.list_cameras()

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
        screen = QtScreen(self.ui.cam)                # Instancio el tipo de ventana donde voy a mostrar la salida

        #=======================SELECCION DE MODELOS========================================================

        self.camProvider.setCam(cam)                  # Seteo la camara que voy a usar
        self.cvProvider.setCv(cvModel)                # Seteo el modelo de vision por computadora a usar
        self.ui.enableCv.clicked.connect(self.enable_cv)
        self.inputFilterProvider.setFilter(inputFilter)    
        self.outputFilterProvider.setFilter(outputFilter)
        self.screenProvider.setScreen(screen)         # Seteo la pantalla en donde voy a mostrar los frames
        self.comProvider.setCom(comModel)             # Seteo el dispositivo de comunicacion que voy a usar

        # Timer para actualizar el frame cada 30 ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def enable_cv(self):
        self.cvProvider.toggleActive()
        self.ui.enableCv.setText('Disable' if self.cvProvider.isActive else 'Enable')

    '''
        Lista las camaras
    '''
    def list_cameras(self):  
        cameras = cv2_enumerate_cameras.enumerate_cameras()
        list_cameras = []

        print("=====================CAMARAS============================")
        graph = FilterGraph()
        camaras = graph.get_input_devices()
        for i, cam in enumerate(camaras):
            list_cameras.append(f"{i}: {cam}")
            print(f"{i}: {cam}")
        print("========================================================")


        self.ui.cbSelectCam.clear()
        self.ui.cbSelectCam.addItems(list_cameras)

    '''
        Importa un modelo que se encuentre en la carpeta models
    '''
    def import_model(self, class_name, provider):
        module = importlib.import_module(f"models")
        model = getattr(module, class_name)
        provider.setModel(model())
        return 

    def select_input_filter_model(self, value):

        if(value == 'None'):
            self.inputFilterProvider.setFilter(BypassFilter())
        else:
            self.import_model(value, self.inputFilterProvider)
        
        methods = self.inputFilterProvider.getMethods()
        self.update_tab(1, value, methods, 'iFilter')
        

    def select_com(self, value):

        self.comProvider.close()

        if(value == 'None'):
            methods = {}
        else:
            self.import_model(value, self.comProvider)
        
            methods = self.comProvider.getMethods()

        ports = self.comProvider.scan()
        self.update_tab(4, value, methods, 'COM', port=ports)

    def select_cam(self):
        index = self.ui.cbSelectCam.currentIndex()
        self.camProvider.realease()
        self.camProvider.setCam(Cam(index))
        methods = self.camProvider.getMethods()
        self.update_tab(0, '', methods, 'CAM')

    '''
        Selecciona el filtro a la salida
    '''
    def select_output_filter_model(self, value):

        if(value == 'None'):
            self.outputFilterProvider.setFilter(BypassFilter())
        else:
            self.import_model(value, self.outputFilterProvider)
        
        methods = self.outputFilterProvider.getMethods()
        self.update_tab(3, value, methods, 'oFilter')

    '''
        Selecciona el modelo de computer vision
    '''
    def select_cv_model(self, value):
        
        self.cvProvider.close()

        if(value == 'None'):
            methods = {}
        else:
            self.import_model(value, self.cvProvider)
        
            methods = self.comProvider.getMethods()

        self.update_tab(2, value, methods, 'CV')

    '''
        Actualiza la tab donde se encuentran los parametros
    '''
    def update_tab(self, index, name, methods, tab_name, **kwargs):
        tab = MyCustomTab(methods, name, **kwargs)
        self.ui.parameters.removeTab(index)
        self.ui.parameters.insertTab(index,tab, tab_name)
        self.ui.parameters.setCurrentIndex(index)

    '''
        Muestra el frame en Qt
    '''
    def show_on_qt(self, frame):
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # Mostrar la imagen en el QLabel
        self.ui.cam.setPixmap(QPixmap.fromImage(q_image))

    def print_gui_console(self, res):
        if res:
            try:
                if isinstance(res, object):
                    r = ""
                    for key, value in vars(res).items():
                        r += f'{key}: {value} \n'
                    self.console.setText(r)
            except:
                self.console.setText(str(res))

    '''
        Actualiza el frame
    '''
    def update_frame(self):
        
        frame = self.camProvider.getFrame()                         # Tomo un frame
        
        frameToCvProcess = self.inputFilterProvider.process(frame)  # Aplico un filtro a mi frame para luego procesarlo
        
        frame,cvResponse = self.cvProvider.process(frameToCvProcess)# Proceso el frame

        self.print_gui_console(cvResponse)
        
        self.comProvider.process(cvResponse)                        # Comunico la respuesta a un periferico externo
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = self.outputFilterProvider.process(frame)            # Aplico un filtro a mi frame para luego mostrarlo en pantalla

        self.screenProvider.showFrame(frame)
    
    '''
        Libera los recursos
    '''
    def close(self):
        self.cvProvider.close()  
        self.cam.realese()                            # Libero el recurso de camara
        self.comProvider.close()
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
    
