from abc import abstractmethod
from iBase import iBase

class iFilter(iBase):

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def byPass(self):
        pass