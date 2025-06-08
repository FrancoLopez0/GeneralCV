from ..interfaces import iFilter

class BypassFilter(iFilter):
    def __init__(self):
        super().__init__()

    def process(self, frame):
        return frame
    
    def showInfo(self):
        pass
    
    def getParameters(self):
        pass
        
    