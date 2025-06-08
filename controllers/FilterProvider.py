from models.interfaces import iFilter
from controllers import BaseProvider

class FilterProvider(BaseProvider.BaseProvider):
    def __init__(self):
        super().__init__()

    def setFilter(self, filter):
        self.model = filter

    def process(self, frame):
        if self.model != None and self.isActive:
            return self.model.process(frame)
        else:
            return frame