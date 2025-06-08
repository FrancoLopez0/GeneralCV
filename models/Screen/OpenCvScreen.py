from ..interfaces import iScreen
import cv2

class OpenCvScreen(iScreen):
    def __init__(self):
        super().__init__()

    def updateTabs(self, methods, tab):
        return super().updateTabs(methods, tab)

    def showInfo(self):
        return

    def getParameters(self):
        return
    
    def destroyAllWindows(self):
        cv2.destroyAllWindows()
    
    def showImage(self, frame):
        cv2.imshow('Camera', frame)
            