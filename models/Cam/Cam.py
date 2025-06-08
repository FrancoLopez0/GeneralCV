from ..interfaces import iCam
from ..decorators import add_param
import cv2

class Cam(iCam):
    def __init__(self, camNumber = 0):
        super().__init__()

        self.cap = cv2.VideoCapture(camNumber)

        self.flip = True
    
    def getFrame(self):

        ret, frame = self.cap.read()

        if not ret:
            print("Error: Can't recieve frame...")
            return TypeError
        else:
            frame = cv2.flip(frame, 1) if self.flip else frame
            return frame
    
    @add_param
    def flipFrame(self):
        self.flip = not self.flip
    
    def getParameters(self):
        return super().getParameters()
    
    def show(self):
        return super().show()
    
    def showInfo(self):
        return super().showInfo()

    def realese(self):
        self.cap.release()
        return True
        
if __name__ == "__main__":
    cam = Cam()
    while True:
        frame = cam.getFrame()
        
        cv2.imshow('Camera', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cam.realese()
    cv2.destroyAllWindows()
        
        