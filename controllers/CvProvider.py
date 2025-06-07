from models.interfaces import iCv
from controllers import BaseProvider

class CvProvider(BaseProvider.BaseProvider):
    def __init__(self):
        super().__init__()

    def setCv(self, cv:iCv):
        self.model = cv

    """
    Retorna la informacion obtenida
    """
    def process(self, frame):
        if self.model != None and self.isActive:
            return self.model.process(frame)
        else:
            return frame, False
    
    def close(self):
        if(self.model!=None):
            self.model.close()
            self.model = None
            return
        return