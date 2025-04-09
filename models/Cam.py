from interfaces.iCam import iCam
import numpy as np
import cv2

class Cam(iCam):
    def __init__(self):
        super().__init__()

        self.cap = cv2.VideoCapture(0)
    
    def getFrame(self):

        ret, frame = self.cap.read()

        if not ret:
            print("Error: Can't recieve frame...")
            return TypeError
        else:
            return frame
    
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
        
        