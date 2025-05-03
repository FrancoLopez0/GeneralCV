from .interfaces import iFilter

class BypassFilter():
    def __init__(self):
        super().__init__()

    def process(self, frame):
        return frame
        
    