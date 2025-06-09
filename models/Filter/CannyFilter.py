from ..interfaces import iFilter
import cv2
from ..decorators import add_param

class CannyFilter(iFilter):
    def __init__(self):
        super().__init__()

        self.th0 = 100
        self.th1 = 200

        self.invert = False
    
    def getParameters(self):
        return super().getParameters()
    
    def showInfo(self):
        return super().showInfo()
    
    @add_param
    def invertColors(self):
        self.invert = not self.invert

    @add_param
    def setThresholds(self, th0:int = 100, th1:int = 100):
        max = 255
        if(th0>0 and th0<max):
            self.th0 = th0
        if(th1>0 and th1<max):
            self.th1 = th1

    def process(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = cv2.Canny(gray, self.th0, self.th1)

        if self.invert:
            return cv2.bitwise_not(frame)

        return frame
    