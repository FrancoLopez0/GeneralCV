from models.interfaces import iCom

class ComProvider():
    def __init__(self):
        self.com:iCom = None

    def setCom(self, com):
        self.com = com
    
    def process(self, cvResponse):
        if self.com != None:
            self.com.process(cvResponse)
        else:
            return False
        
