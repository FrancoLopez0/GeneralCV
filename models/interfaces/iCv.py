from abc import abstractmethod
from iBase import iBase

class iCam(iBase):

    @abstractmethod
    def showInfo(self):
        pass
    
    @abstractmethod
    def getParameters(self):
        pass

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def getData(self):
        pass