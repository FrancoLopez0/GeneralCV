from abc import abstractmethod
from .iBase import iBase

class iScreen(iBase):

    @abstractmethod
    def showInfo(self):
        pass
    
    @abstractmethod
    def getParameters(self):
        pass

    @abstractmethod
    def destroyAllWindows(self):
        pass

    @abstractmethod
    def showImage(self):
        pass

    @abstractmethod
    def updateTabs(self, methods, tab):
        pass