from ..interfaces import iCam
from ..decorators import add_param
from ..types import ComboInputType, SliderInputType
import cv2
import numpy as np

class Cam(iCam):
    def __init__(self, camNumber = 0):
        super().__init__()

        self.cap = cv2.VideoCapture(camNumber)

        self.flip = True

        self.res = []

        self.lut = np.array([np.clip(i , 0, 255) for i in range(256)], dtype=np.uint8)

        self.alpha_max = 10
        self.beta_max = 200
    
    @add_param
    def setLut(self, alpha:SliderInputType = 1, beta:SliderInputType = 0):

        if alpha == 0:
            alpha = 1
        alpha = (alpha / 100) * self.alpha_max
        
        beta = (beta / 100) * self.beta_max

        self.lut = np.array([np.clip(alpha * i + beta, 0, 255) for i in range(256)], dtype=np.uint8)
    
    @add_param
    def resetLut(self):
        self.lut = np.array([np.clip(i , 0, 255) for i in range(256)], dtype=np.uint8)

    def getFrame(self):

        ret, frame = self.cap.read()

        if not ret:
            print("Error: Can't recieve frame...")
            return TypeError
        else:
            frame = cv2.flip(frame, 1) if self.flip else frame
            frame = cv2.LUT(frame, self.lut)
            return frame
    
    @add_param
    def flipFrame(self):
        self.flip = not self.flip
    
    @add_param
    def setResolution(self, res: ComboInputType = ['260x460', '1280x720']):
        self.res = res
    
    def getParameters(self):
        return super().getParameters()
    
    def show(self):
        return super().show()
    
    def showInfo(self):
        return super().showInfo()

    def realese(self):
        self.cap.release()
        return True
        
if __name__ == "__main__":
    cam = Cam()
    while True:
        frame = cam.getFrame()
        
        cv2.imshow('Camera', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cam.realese()
    cv2.destroyAllWindows()
        
        