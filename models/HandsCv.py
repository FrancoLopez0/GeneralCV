from .interfaces import iCv
import mediapipe as mp

class HandsCv(iCv):
    def __init__(self):
        super().__init__()

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5)
    
    def showInfo(self):
        return super().showInfo()

    def getParameters(self):
        return super().getParameters()

    def process(self, frame):
        results = self.hands.process(frame)
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0,0,255), thickness=3, circle_radius=3),
                    self.mp_drawing.DrawingSpec(color=(0,255,0), thickness=3, circle_radius=3))
        return frame
    
    def close(self):
        self.hands.close()
        return super().close()
    
    def getData(self):
        return super().getData()