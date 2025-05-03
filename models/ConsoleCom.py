from .interfaces import iCom

class ConsoleCom():
    def __init__(self, text=''):
        super().__init__()
        self.text = text

    def process(self, cvResponse):
        if cvResponse:
            print(cvResponse)
        else:
            return
        