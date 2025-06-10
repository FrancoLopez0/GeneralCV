from models.types import ComboInputType
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDoubleSpinBox, QSpinBox, QHBoxLayout, QComboBox
from PySide6.QtCore import QTimer, Qt
import inspect

class MyCustomTab(QWidget):
    def __init__(self, methods, name, **kwargs):
        super().__init__()

        h = 25
        layout = QHBoxLayout()
        layout.addWidget(QLabel(name), alignment=Qt.AlignCenter)

        for method_name, method_data in methods.items():
            funcion = method_data['funcion']
            parametros = method_data['parametros']

            sig = inspect.signature(funcion)
            default_values = {
                k: v.default
                for k, v in sig.parameters.items()
                if v.default is not inspect.Parameter.empty
            }

            inputs = {}
            func_layout = QVBoxLayout()
            
            for param, param_type in parametros.items():
                param_layout = QHBoxLayout()
                label = QLabel(param)
                label.setFixedHeight(h)
                param_layout.addWidget(label, alignment=Qt.AlignCenter)

                var_widget = None

                if param_type == str:
                    var_widget = QLineEdit()
                    if param in default_values:
                        var_widget.setText(str(default_values[param]))
                elif param_type == float:
                    var_widget = QDoubleSpinBox()
                    var_widget.setMaximum(1000)
                    if param in default_values:
                        var_widget.setValue(float(default_values[param]))
                elif param_type == int:
                    var_widget = QSpinBox()
                    var_widget.setMaximum(1000)

                    if param in default_values:
                        var_widget.setValue(int(default_values[param]))
                elif param_type == ComboInputType:
                    var_widget = QComboBox()
                    try:
                        var_widget.addItems(default_values[param])
                    except:
                        var_widget.addItems(kwargs.get(param))

                else:
                    var_widget = QLabel("Tipo no soportado")

                inputs[param] = var_widget
                param_layout.addWidget(var_widget, alignment=Qt.AlignCenter)
                func_layout.addLayout(param_layout)

            layout.addLayout(func_layout)

            btn = QPushButton(method_name)
            btn.setFixedHeight(h)

            fun = self.make_callback(funcion, inputs)
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
                    print(type(widget))
            func(**args)
        return callback