from ..interfaces import iCom
from ..decorators import add_param
import threading
import queue
import requests

class TrackingRobot(iCom):
    def __init__(self):
        super().__init__()
        self.coords = []
        self.ref = []
        self.ip_url = "http://192.168.1.100"
        
        self.send_queue = queue.Queue(maxsize=5)
        self.thread = threading.Thread(target=self._http_worker, daemon=True)
        self.thread.start()

    def _http_worker(self):
        while True:
            try:
                pan, tilt = self.send_queue.get()
                url = f"{self.ip_url}/relative?pan={pan}&tilt={tilt}"
                requests.get(url, timeout=1.0)
            except Exception as e:
                print(f"TrackingRobot HTTP error: {e}")

    def process(self, cvResponse):
        try:
            if cvResponse and hasattr(cvResponse, 'center'):
                x = cvResponse.center.get('x', 0)
                y = cvResponse.center.get('y', 0)
                print(f"Raw coordinates: X={x}, Y={y}")
                                    
                # Math mapping: 640x480 resolution to 0-180 servo angles
                # x goes from 0-640 -> 0-180
                # y goes from 0-480 -> 0-180
                pan = int(max(0, min(180, (x / 640.0) * 180)))
                tilt = int(max(0, min(180, (y / 480.0) * 180)))
                
                self.send({"pan": pan, "tilt": tilt})
                
        except Exception as e:
            print(f"Error extracting coordinates: {e}")
        return 

    def send(self, data):
        try:
            if self.send_queue.full():
                try:
                    self.send_queue.get_nowait()
                except queue.Empty:
                    pass
            self.send_queue.put_nowait((data.get("pan", 90), data.get("tilt", 90)))
        except queue.Full:
            pass

    def recieve(self):
        pass

    def scan(self):
        return []
        
    def showInfo(self):
        pass
        
    def getParameters(self):
        pass