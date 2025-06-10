from ..interfaces import iFilter
from ..decorators import add_param
from models.types import ComboInputType
import cv2

from settings import settings

class GaussianFilter(iFilter):
    def __init__(self):
        super().__init__()
        self.kernel = (settings.GAUSSIAN_FILTER_W_KERNEL_DEFAULT,settings.GAUSSIAN_FILTER_H_KERNEL_DEFAULT)
        pass
    
    def getParameters(self):
        return super().getParameters()
    
    def showInfo(self):
        return super().showInfo()

    @add_param
    def setKernel(self, w_kernel:int=settings.GAUSSIAN_FILTER_W_KERNEL_DEFAULT, h_kernel:int=settings.GAUSSIAN_FILTER_H_KERNEL_DEFAULT):
        self.kernel = (w_kernel, h_kernel)
        return

    def process(self, frame):
        frame = cv2.GaussianBlur(frame, self.kernel, 0)
        return frame
    