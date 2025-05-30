from .interfaces import iScreen
from PySide6.QtGui import QImage, QPixmap
        
class QtScreen(iScreen):
    def __init__(self, label):
          super().__init__()
          self.label = label
    
    def showImage(self, frame):
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # Mostrar la imagen en el QLabel
        self.label.setPixmap(QPixmap.fromImage(q_image))
        return
    
    def showInfo(self):
         return super().showInfo()

    def getParameters(self):
         return super().getParameters()
    
    def destroyAllWindows(self):
         return super().destroyAllWindows()
    