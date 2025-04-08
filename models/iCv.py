from abc import ABC, abstractmethod

class iCam(ABC):
    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def getData(self):
        pass