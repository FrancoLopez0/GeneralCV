from abc import ABC, abstractmethod

class iFilter(ABC):
    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def byPass(self):
        pass