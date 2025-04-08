from abc import ABC, abstractmethod

class iCom(ABC):
    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def recieve(self):
        pass