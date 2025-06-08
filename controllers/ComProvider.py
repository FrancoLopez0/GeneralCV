from models.interfaces import iCom
from controllers import BaseProvider

class ComProvider(BaseProvider.BaseProvider):
    def __init__(self):
        super().__init__()
        self.model:iCom = None

    def setCom(self, com):
        self.model = com

    def scan(self):
        return self.model.scan()
    
    def close(self):
        try:
            return self.model.close()
        except:
            return
    
    def process(self, cvResponse):
        if self.model != None and self.isActive:
            self.model.process(cvResponse)
        else:
            return False
        
