from .HandsCv import HandsCv
from ..decorators import add_param
from settings import settings
import numpy as np
import cv2

class FingersTrackingCv(HandsCv):
    def __init__(self):
        super().__init__()

        self.is_front_number = settings.IS_FRONT_NUMBER
        self.full_extend_finger_number = settings.FULL_EXTEND_FINGER_NUMBER_DEFAULT
        self.full_closed_finger_number =settings.FULL_CLOSED_FINGER_NUMBER_DEFAULT
        self.finger_distance = None
        self.finger_distance_raw = None

        pass
    
    @add_param
    def setFullExtend(self):
        if self.finger_distance_raw != None:
            self.full_extend_finger_number = self.finger_distance_raw[1]

    def setFullClosed(self):
        if self.finger_distance_raw != None:
            self.full_closed_finger_number = self.finger_distance_raw[1]


    def process(self, frame):
        frame,response = super().process(frame)

        self.frame_h, self.frame_w, _= frame.shape
        
        if self.results.multi_hand_landmarks is not None:
            hand = self.results.multi_hand_landmarks[-1]

            try:
                if(hand.landmark[0].y-hand.landmark[1].y>self.is_front_number):
                    self.finger_distance_raw = [(hand.landmark[0].y-hand.landmark[tip].y)/(hand.landmark[0].y-hand.landmark[base].y) for tip, base in zip(self.fingers_tip_index, self.fingers_base_index)]
                    self.finger_distance = np.clip(self.finger_distance_raw, self.full_closed_finger_number, self.full_extend_finger_number)
                    self.main_hand.fingers_state = (self.finger_distance - self.full_closed_finger_number) / (self.full_extend_finger_number - self.full_closed_finger_number)
                    
                    c = 0
                    for finger_state in self.main_hand.fingers_state[1:]:
                        cv2.line(frame, (40 + c, self.frame_h - 20), (40 + c, int(self.frame_h - 100 * finger_state)), (5,200,10), 10)
                        c += 20
                    
                    return frame, self.main_hand
                return frame, False
            except:
                pass
        return frame, response
    