from abc import abstractmethod
from iBase import iBase

class iCom(iBase):

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def recieve(self):
        pass