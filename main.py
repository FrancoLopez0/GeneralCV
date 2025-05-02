# This Python file uses the following encoding: utf-8
# pyside6-uic .\ui_files\mainwindow.ui -o view_main_window.py
# pyside6-uic .\ui_files\main.ui > view_main_window.py
# pyside6-designer .\ui_files\mainwindow.ui      
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QVBoxLayout, QLabel, QDialog
from views.view_main_window import Ui_MainWindow
from models import Cam, OpenCvScreen
from controllers import CamProvider, ScreenProvider
import cv2

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GeneralCV")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    camProvider = CamProvider()              # Inicializo el proevedor de camara
    screenProvider = ScreenProvider()        # Inicializo el proevedor de pantalla
    cam = Cam()                              # Inicializo el tipo de camara que voy a usar

    camProvider.setCam(Cam())                # Seteo la camara que voy a usar
    screenProvider.setScreen(OpenCvScreen()) # Seteo la pantalla en donde voy a mostrar los frames

    while True:
        frame = camProvider.getFrame()       # Tomo un frame
        screenProvider.showFrame(frame)      # Lo muestro en mi pantalla
        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):# Si presiono 'q' el programa finaliza
            break
    
    cam.realese()                            # Libero el recurso de camara
    screenProvider.destroyAllWindows()       # Elimino todas las pantallas del proevedor

    # app = QApplication(sys.argv)
    # widget = MainWindow()
    # widget.show()
    # sys.exit(app.exec())

    
