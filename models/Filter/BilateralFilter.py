from ..interfaces import iFilter
from ..decorators import add_param
from models.types import ComboInputType
import cv2

class BilateralFilter(iFilter):
    def __init__(self):
        super().__init__()
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        self.d = 9
        self.sigmaColor = 75
        self.sigmaSpace = 75
        pass
    
    def getParameters(self):
        return super().getParameters()
    
    def showInfo(self):
        return super().showInfo()

    @add_param
    def setParams(self, d:int=9, color:int=75,space:int=75):
        self.d = d
        self.sigmaColor = color
        self.sigmaSpace = space
        return

    def process(self, frame):
        frame = cv2.bilateralFilter(frame,self.d,self.sigmaColor,self.sigmaSpace)
        return frame
    