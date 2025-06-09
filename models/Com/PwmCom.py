from . import SerialCom 

class PwmCom(SerialCom):
    def __init__(self):
        super().__init__()
        
        self.pwm = 0
    
    def process(self, cvResponse):
        try:
            print(round(cvResponse[0] * 255))
            self.setPwm(round(cvResponse[0] * 255))
        except:
            pass
        return 

    def setPwm(self, pwm):
        self.pwm = pwm
        self.send(pwm.to_bytes())