from models.interfaces import iCv

class CvProvider():
    def __init__(self):
        self.cv:iCv = None
    
    def setCv(self, cv:iCv):
        self.cv = cv

    """
    Retorna la informacion obtenida
    """
    def process(self, frame):
        if self.cv != None:
            return self.cv.process()
        else:
            return False