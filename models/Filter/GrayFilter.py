from ..interfaces import iFilter
from ..decorators import add_param
import cv2

class GrayFilter(iFilter):
    def __init__(self):
        super().__init__()
        self.kernel = (5,5)
        pass
    
    def getParameters(self):
        return super().getParameters()
    
    def showInfo(self):
        return super().showInfo()

    def process(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    