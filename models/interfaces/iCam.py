from abc import abstractmethod
from interfaces.iBase import iBase

class iCam(iBase):

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def getFrame(self):
        pass