from ..interfaces import iFilter
from ..decorators import add_param
from models.types import ComboInputType
import cv2
import numpy as np

from settings import settings

class BackgroundSubstractionFilter(iFilter):
    def __init__(self):
        super().__init__()
        self.subs = cv2.bgsegm.createBackgroundSubtractorMOG()
        self.subs_original = True
        self.kernel = (settings.GAUSSIAN_FILTER_W_KERNEL_DEFAULT,settings.GAUSSIAN_FILTER_H_KERNEL_DEFAULT)
        self.morph = cv2.MORPH_OPEN
        self.prev_centroid = (0,0)
        self.line_color = (0,255,0)
        self.centroids = []
        self.return_original = True
        self.show_centroids = False
        pass
    
    def getParameters(self):
        return super().getParameters()
    
    @add_param
    def returnOriginal(self):
        self.return_original = not self.return_original
    
    @add_param
    def setMorph(self, morph: ComboInputType = ['MORPH_ERODE','MORPH_DILATE','MORPH_OPEN','MORPH_CLOSE','MORPH_GRADIENT','MORPH_TOPHAT','MORPH_BLACKHAT']):
        self.morph = getattr(cv2, morph)

    @add_param
    def setKernel(self, w_kernel:int=settings.GAUSSIAN_FILTER_W_KERNEL_DEFAULT, h_kernel:int=settings.GAUSSIAN_FILTER_H_KERNEL_DEFAULT):
        self.kernel = (w_kernel, h_kernel)
        return
    
    @add_param
    def subsOriginal(self):
        self.subs_original = not self.subs_original
    
    @add_param
    def showCentroids(self):
        self.show_centroids = not self.show_centroids
    
    def showInfo(self):
        return super().showInfo()

    def process(self, frame):
        original = frame
        frame = self.subs.apply(frame)
        frame = cv2.morphologyEx(frame, self.morph, self.kernel)

        if self.subs_original:
            fgmask_color = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

            if self.show_centroids:
                contornos, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for cnt in contornos:
                    area = cv2.contourArea(cnt)
                    if area > 500:  # filtrar ruido
                        M = cv2.moments(cnt)
                        if M["m00"] > 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            cv2.circle(original, (cx, cy), 10, (255, 100, 0), -1)
                            cv2.line(original, (cx,cy), self.prev_centroid, self.line_color, 2)

                            self.prev_centroid = (cx,cy)

            frame = cv2.bitwise_and(original, fgmask_color)

        cv2.putText(original, f'Movimiento: {np.sum(frame==255)}',(50,50),0,1,(255,255,0),2)
        
        if self.return_original:
            return original
        return frame
    