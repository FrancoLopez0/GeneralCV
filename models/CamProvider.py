from interfaces.iCam import iCam

class CamProvider():
    def __init__(self):
        
        self.cam = None

        pass

    def setCam(self, camObj:iCam):

        self.cam = camObj

        pass


    def loop(self):

        frame = self.cam.getFrame()

        pass