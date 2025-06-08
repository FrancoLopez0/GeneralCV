from models.types import ComboInputType
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDoubleSpinBox, QSpinBox, QHBoxLayout, QComboBox
from PySide6.QtCore import QTimer, Qt

class MyCustomTab(QWidget):
    def __init__(self, methods, name, **kwargs):
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
                if(param_type == ComboInputType):
                    var_widget = QComboBox()
                    var_widget.addItems(kwargs.get('combo_items'))
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
                if isinstance(widget, QComboBox):
                    args[k] = widget.currentText()
                else:
                    args[k] = widget.value()
            func(**args)
        return callback