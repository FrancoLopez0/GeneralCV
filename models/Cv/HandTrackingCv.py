from .HandsCv import HandsCv
import cv2
from ..decorators import add_param
from ..types import SliderInputType
from settings import settings
import numpy as np

class HandTrackingCv(HandsCv):
    def __init__(self):
        super().__init__()

        self.reference = [0,0]
        self.line_color = (0,255,0)

        self.rectange_w = settings.SQR_HAND_TRACKING_W

        self.frame_h = 0
        self.frame_w = 0

        pass
    
    @add_param
    def setRectangeWidth(self, w:SliderInputType= settings.SQR_HAND_TRACKING_W):
        self.rectange_w = int((w/100) * self.frame_h/2)

    def process(self, frame):
        frame,response = super().process(frame)

        self.frame_h, self.frame_w, _= frame.shape

        try:
            if(self.main_hand.fingers_state == [True, True, False, False, False]):
                
                h, w, ch = frame.shape

                reference = (w//2, h//2)

                x_norm, y_norm = self.main_hand.fingers_coords['index']
                index_tip = (int(x_norm * w), int(y_norm * h))

                # ES MEJOR MANDAR LA POSICION ABSOLUTA Y QUE LA CALSE TRACKING TENGA LA REFERENCIA ?
                self.main_hand.center = {
                    'x': index_tip[0]-reference[0],
                    'y': index_tip[1]-reference[1]
                }

                rectange_w_bot_point = (reference[0]+self.rectange_w, reference[1]-self.rectange_w)
                rectange_w_top_point = (reference[0]-self.rectange_w, reference[1]+self.rectange_w)

                in_rectangle = (index_tip[0] > rectange_w_top_point[0]) and (index_tip[0] < rectange_w_bot_point[0]) and (index_tip[1] < rectange_w_top_point[1]) and (index_tip[1] > rectange_w_bot_point[1])

                if(in_rectangle):
                    return frame, False

                cv2.circle(frame, reference, 4, (0,255,0), 2)
                cv2.line(frame, reference, index_tip, self.line_color, 2)
                cv2.rectangle(frame, rectange_w_bot_point, rectange_w_top_point, self.line_color, 2)
                
                cv2.putText(frame,f'[{index_tip[0]-reference[0]},{index_tip[1]-reference[1]}]',index_tip,0,1,(0,255,0),2)

                return frame, self.main_hand
        except:
            pass
        return frame, response
        # return frame, self.main_hand.fingers_coords

    @add_param
    def set_line_color(self, r:int = 0, g:int = 255, b:int = 0):
        self.line_color = (b,g,r)
    