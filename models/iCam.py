from abc import ABC, abstractmethod

class iCam(ABC):
    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def getFrame(self):
        pass