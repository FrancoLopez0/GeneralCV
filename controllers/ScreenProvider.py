from models.interfaces import iScreen
import numpy as np
import cv2

class ScreenProvider():
    def __init__(self):
        
        self.screen:iScreen = None

        pass

    def setScreen(self, screen):
        self.screen = screen

    def destroyAllWindows(self):
        self.screen.destroyAllWindows()

    def showFrame(self, frame):
        if self.screen != None:
            self.screen.showImage(frame)
        return
    
    def updateTabs(self, methods, tab):
        if(methods != None):
            self.screen.updateTabs(methods, tab)