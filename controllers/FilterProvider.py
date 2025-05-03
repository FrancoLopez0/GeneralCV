from models.interfaces import iFilter

class FilterProvider():
    def __init__(self):
        self.filter: iFilter = None

    def setFilter(self, filter):
        self.filter = filter
    
    def process(self, frame):
        if self.filter != None:
            return self.filter.process(frame)
        else:
            return frame