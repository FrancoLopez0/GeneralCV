from models.interfaces import iCam
import numpy as np
import cv2

class CamProvider():
    def __init__(self):
        
        self.cam = None

        pass
    
    def setCam(self, camObj:iCam):

        self.cam = camObj

        pass

    def getFrame(self):
        if self.cam != None:
            return self.cam.getFrame()
        else: 
            return ValueError

    def loop(self):

        while True:

            frame = self.cam.getFrame()

            cv2.imshow('Camera', frame)

            # Exit the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cam.realese()
        cv2.destroyAllWindows()

        pass