from models.interfaces import iCam
from controllers import BaseProvider
import numpy as np

class CamProvider(BaseProvider.BaseProvider):
    def __init__(self):
        super().__init__()
        self.model = None

        pass
    
    def setCam(self, camObj:iCam):

        self.model = camObj

        pass

    def getFrame(self):
        if self.model != None and self.isActive:
            return self.model.getFrame()
        else: 
            return ValueError

    def realease(self):
        if self.model != None:
            try:
                self.model.realese()
            except:
                pass


    # def loop(self):

    #     while True:

    #         frame = self.cam.getFrame()

    #         cv2.imshow('Camera', frame)

    #         # Exit the loop if 'q' is pressed
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
        
    #     self.cam.realese()
    #     cv2.destroyAllWindows()

    #     pass