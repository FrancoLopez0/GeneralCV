# This Python file uses the following encoding: utf-8
# pyside6-uic .\ui_files\mainwindow.ui -o view_main_window.py
# pyside6-uic .\ui_files\main.ui > view_main_window.py
# pyside6-designer .\ui_files\mainwindow.ui      
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QVBoxLayout, QLabel, QDialog
from views.view_main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GeneralCV")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
