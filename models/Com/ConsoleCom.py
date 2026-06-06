from ..interfaces import iCom

class ConsoleCom(iCom):
    def __init__(self, text=''):
        super().__init__()
        self.text = text

    def process(self, cvResponse):
        try:
            if cvResponse:
                print(cvResponse)
                pass
            else:
                return
        except:
            return
    
    def scan(self):
        return super().scan()
        
    def showInfo(self):
        pass
    
    def getParameters(self):
        pass

    def recieve(self):
        pass

    def send(self):
        pass
        