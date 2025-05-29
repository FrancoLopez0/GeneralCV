from abc import abstractmethod
from .iBase import iBase

class iCv(iBase):

    @abstractmethod
    def showInfo(self):
        pass
    
    @abstractmethod
    def getParameters(self):
        pass

    @abstractmethod
    def process(self, frame):
        pass

    @abstractmethod
    def getData(self):
        pass

    @abstractmethod
    def close(self):
        pass