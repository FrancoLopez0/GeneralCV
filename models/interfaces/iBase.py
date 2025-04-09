from abc import ABC, abstractmethod

class iBase(ABC):
    @abstractmethod
    def showInfo(self):
        pass

    @abstractmethod
    def getParameters(self):
        pass