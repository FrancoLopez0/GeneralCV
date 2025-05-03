from abc import ABC, abstractmethod

class iBase(ABC):

    """
        Muestra la informacion acerca del objeto
    
    Returns:
        str: Informacion del objeto.
    """
    @abstractmethod
    def showInfo(self):
        pass
        
    @abstractmethod
    def getParameters(self):
        pass