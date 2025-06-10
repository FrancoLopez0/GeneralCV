from . import SerialCom

class TrackingRobot(SerialCom):
    def __init__(self):
        super().__init__()
        self.coords=[]
        self.ref = []

    def process(self, cvResponse):
        try:
            # print(cvResponse.center)
            print(cvResponse.center['x'].to_bytes(1, signed=True), cvResponse.center['y'].to_bytes(1, signed=True))
        except:
            pass
        # self.send(str(cvResponse.center))
        return super().process(cvResponse)