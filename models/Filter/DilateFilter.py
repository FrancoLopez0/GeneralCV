from ..interfaces import iFilter
from ..decorators import add_param
from models.types import ComboInputType, SliderInputType
import cv2

class DilateFilter(iFilter):
    def __init__(self):
        super().__init__()
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        pass
    
    def getParameters(self):
        return super().getParameters()
    
    def showInfo(self):
        return super().showInfo()

    @add_param
    def setKernel(self, k_type: ComboInputType = ["MORPH_RECT", "MORPH_CROSS", "MORPH_ELLIPSE"], w_kernel:SliderInputType=5, h_kernel:SliderInputType=5):
        self.kernel = cv2.getStructuringElement(getattr(cv2, k_type), (w_kernel, h_kernel))
        return

    def process(self, frame):
        frame = cv2.dilate(frame, self.kernel)
        return frame
    