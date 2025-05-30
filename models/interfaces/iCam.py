from abc import abstractmethod
from .iBase import iBase

class iCam(iBase):

    """
        Muestra informacion de la camara

    Returns:
        str
    """
    @abstractmethod
    def show(self, frame):
        pass

    """
        Obtiene un frame de la camara
    Returns:
        np.array: Arreglo de datos.
    """
    @abstractmethod
    def getFrame(self):
        pass