from .interfaces import iCv
import mediapipe as mp
from dataclasses import dataclass

@dataclass
class Hand:
    index: int
    fingers_state: list
    fingers_coords: dict

class HandsCv(iCv):
    def __init__(self):
        super().__init__()

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

        self.fingers_tip_index = [
                              self.mp_hands.HandLandmark.THUMB_TIP,
                              self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
                              self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                              self.mp_hands.HandLandmark.RING_FINGER_TIP,
                              self.mp_hands.HandLandmark.PINKY_TIP
                              ]
        
        self.fingers_base_index = [2, 5, 9, 13, 17]

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7)
        
        self.main_hand = Hand(0, [0,0,0,0,0], {})
    
    def showInfo(self):
        return super().showInfo()

    def getParameters(self):
        return super().getParameters()

    def process(self, frame):
        results = self.hands.process(frame)
        if results.multi_hand_landmarks is not None:

            # Obtengo la primer mano
            hand = results.multi_hand_landmarks[0]
            
            # Guardo todas las coordenadas de los dedos de la mano principal
            self.main_hand.fingers_coords = {
                'thumb':[hand.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x,hand.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y],
                'index':[hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x,hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y],
                'middle':[hand.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,hand.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y],
                'ring':[hand.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].x,hand.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].y],
                'pinky':[hand.landmark[self.mp_hands.HandLandmark.PINKY_TIP].x,hand.landmark[self.mp_hands.HandLandmark.PINKY_TIP].y],
                }

            # Recorro todas las manos
            for hand_landmarks in results.multi_hand_landmarks: 
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0,0,255), thickness=1, circle_radius=1),
                    self.mp_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1))   
            
            if(hand.landmark[0].y>hand.landmark[self.fingers_tip_index[1]].y):
                self.main_hand.fingers_state = [hand.landmark[finger_tip].y<hand.landmark[finger_base].y for finger_tip, finger_base in zip(self.fingers_tip_index, self.fingers_base_index)]
            else:
                self.main_hand.fingers_state = [None for finger in self.main_hand.fingers_state]
        return frame, self.main_hand
    
    def close(self):
        self.hands.close()
        return super().close()
    
    def getData(self):
        return super().getData()