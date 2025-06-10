from .HandsCv import HandsCv
import cv2
from ..decorators import add_param

class HandTrackingCv(HandsCv):
    def __init__(self):
        super().__init__()

        self.reference = [0,0]
        self.line_color = (0,255,0)

        pass
    
    def process(self, frame):
        frame,response = super().process(frame)

        try:
            if(self.main_hand.fingers_state == [True, True, False, False, False]):
                
                h, w, ch = frame.shape

                reference = (w//2, h//2)

                x_norm, y_norm = self.main_hand.fingers_coords['index']
                index_tip = (int(x_norm * w), int(y_norm * h))

                cv2.circle(frame, reference, 4, (0,255,0), 2)
                cv2.line(frame, reference, index_tip, self.line_color, 2)
                
                

                cv2.putText(frame,f'[{index_tip[0]-reference[0]},{index_tip[1]-reference[1]}]',index_tip,0,1,(0,255,0),2)

                # ES MEJOR MANDAR LA POSICION ABSOLUTA Y QUE LA CALSE TRACKING TENGA LA REFERENCIA ?
                self.main_hand.center = {
                    'x': index_tip[0]-reference[0],
                    'y': index_tip[1]-reference[1]
                }

                return frame, self.main_hand
        except:
            pass
        return frame, response
        # return frame, self.main_hand.fingers_coords

    @add_param
    def set_line_color(self, r:int = 0, g:int = 255, b:int = 0):
        self.line_color = (b,g,r)
    