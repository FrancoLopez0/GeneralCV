from ..interfaces import iCom
from ..decorators import add_param
import threading
import queue
import requests
import time

class ServoTrackingCom(iCom):
    def __init__(self, server_url = "http://192.168.1.87:81/"):
        super().__init__()

        self.server_url = server_url

        self.frame_width = 640
        self.frame_height = 480

        # Factor de velocidad/suavidad (Kp - Ganancia proporcional)
        # Un valor más alto hace que se mueva más rápido pero puede temblar.
        self.pan_step = 0.05
        self.tilt_step = 0.05
        self.delay_ms = 50

        # Background thread for HTTP requests to prevent UI freezing
        # We use an Event and a shared variable to always send the latest target, 
        # dropping intermediate frames to minimize latency.
        self.latest_target = None
        self.target_lock = threading.Lock()
        self.target_event = threading.Event()

        self._running = True
        self.worker_thread = threading.Thread(target=self._send_worker, daemon=True)
        self.worker_thread.start()

    def _send_worker(self):
        while self._running:
            self.target_event.wait()
            self.target_event.clear()

            if not self._running:
                break

            with self.target_lock:
                if self.latest_target is None:
                    continue
                values = self.latest_target
                self.latest_target = None

            try:
                # Ensure the url ends with /relative
                base_url = self.server_url.rstrip('/')
                url = f"{base_url}/relative?x={values['pan']}&y={values['tilt']}"
                requests.get(url, timeout=1.0)
            except requests.exceptions.RequestException as e:
                print(f"HTTP request failed: {e}")

            time.sleep(self.delay_ms / 1000.0)

    @add_param
    def force_reconnect(self, trigger: bool = False):
        if trigger:
            print("Forcing reconnection of Servo tracking...")
            self._running = False
            self.target_event.set()
            if hasattr(self, 'worker_thread') and self.worker_thread.is_alive():
                self.worker_thread.join(timeout=1.0)
            
            self._running = True
            self.worker_thread = threading.Thread(target=self._send_worker, daemon=True)
            self.worker_thread.start()

    def process(self, cvResponse):
        # try:
        # print(cvResponse)
        try:
            if cvResponse and hasattr(cvResponse, 'center') and cvResponse.center:
                x = cvResponse.center.get('x')
                y = cvResponse.center.get('y')

                if x is not None and y is not None:
                    print(f"Raw coordinates: X={x}, Y={y}")

                    new_deltas = self.calculate_deltas(x, y)

                    if new_deltas:
                        self.send(new_deltas)

        except Exception as e:
            print(f"Error extracting coordinates: {e}")
    
    def calculate_deltas(self, x, y):

        # Nota: Dependiendo de cómo estén montados tus servos, 
        # puede que necesites invertir el signo (+ o -).
        delta_pan = int(x * self.pan_step)
        delta_tilt = int(y * self.tilt_step)

        return {
            "pan": delta_pan, 
            "tilt": delta_tilt
        }

    def send(self, values):
        print(f"Sending relative deltas to servos -> Pan: {values['pan']}, Tilt: {values['tilt']}")
        with self.target_lock:
            self.latest_target = values
        self.target_event.set()
    
    @add_param
    def set_delay_ms(self, delay: int):
        self.delay_ms = delay

    def recieve(self):
        return

    def scan(self):
        return

    def getParameters(self):
        return super().getParameters()
    
    def showInfo(self):
        return super().showInfo()
