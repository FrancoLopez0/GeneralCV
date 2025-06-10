from ..interfaces import iFilter
from ..decorators import add_param
from models.types import ComboInputType
import cv2

class GaussianFilter(iFilter):
    def __init__(self):
        super().__init__()
        self.kernel = (5,5)
        pass
    
    def getParameters(self):
        return super().getParameters()
    
    def showInfo(self):
        return super().showInfo()

    @add_param
    def setKernel(self, w_kernel:int=5, h_kernel:int=5):
        self.kernel = (w_kernel, h_kernel)
        return

    def process(self, frame):
        frame = cv2.GaussianBlur(frame, self.kernel, 0)
        return frame
    