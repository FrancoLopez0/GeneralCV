from ..interfaces import iScreen
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QDoubleSpinBox, QSpinBox, QLineEdit, QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton
        
class QtScreen(iScreen):
     def __init__(self, label):
          super().__init__()
          self.label = label
    
     def showImage(self, frame):
        
          if len(frame.shape) == 3:
               # Imagen en color (BGR)
               h, w, ch = frame.shape
               bytes_per_line = ch * w
               q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
          else:
              # Imagen en escala de grises
              h, w = frame.shape
              bytes_per_line = w
              q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
          
          self.label.setPixmap(QPixmap.fromImage(q_image))

          return

     def updateTabs(self, methods:dict, tabs:QTabWidget):
          # print('====================================================================')
          # for method in methods:

          #      params = [param for param in methods[method]['parametros']]

          #      for param, param_type in methods[method]['parametros'].items():
          #           if(param_type == str):
          #                print('Es una variable del tipo string')
          #           if(param_type == float):
          #                print('Es del tipo float')
          #           if(param_type == int):
          #                print('Es del tipo entero')
          #           # if (isinstance(param_type, str)):
          #           #      print(f'{param} es del tipo string')

          #      # print(f'{method}({params})')
          #      # for param, param_type in methods[method].items():
          #      #      print(f'{param}({param_type})')
          #      # for nombre_param, tipo in method["parametros"].items():
          #      #      if tipo == float:
          #      #           widget = QDoubleSpinBox()
          #      #      elif tipo == int:
          #      #           widget = QSpinBox()
          #      #      else:
          #      #           widget = QLineEdit()
          #      #      entradas[nombre_param] = widget
          #      #      layout_tab.addWidget(widget)

          #      # boton = QPushButton(method["nombre"])
          #      # layout_tab.addWidget(boton)

          #      # def make_callback(func=method["funcion"], inputs=entradas):
          #      #      def callback():
          #      #           args = {}
          #      #           for k, widget in inputs.items():
          #      #                if isinstance(widget, QLineEdit):
          #      #                     args[k] = widget.text()
          #      #                else:
          #      #                     args[k] = widget.value()
          #      #           func(**args)
          #      #      return callback

          #      # boton.clicked.connect(make_callback())
          #      # tabs.addTab(layout_tab)
          # print('====================================================================')
          
          return
    
     def showInfo(self):
         return super().showInfo()

     def getParameters(self):
         return super().getParameters()
    
     def destroyAllWindows(self):
         return super().destroyAllWindows()
    