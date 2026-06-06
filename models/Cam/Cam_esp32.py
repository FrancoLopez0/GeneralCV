import cv2
import numpy as np
import requests
from ..decorators import add_param
from ..interfaces import iCam
from ..types import ComboInputType, SliderInputType
from enum import StrEnum
import time
import threading

class ReqStatus(StrEnum):
     connected = "OK"
     disconnected = "FALSE"

class Esp32_cam(iCam):
    def __init__(self, server_url="http://192.168.1.54/"):
        super().__init__()
        if server_url.startswith("://"):
            self.server_url = "http" + server_url
        elif not server_url.startswith("http"):
            self.server_url = "http://" + server_url
        else:
            self.server_url = server_url
        self.status = ReqStatus.disconnected
        self.current_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self._running = True
        
        try:
            self.make_ping()
        except:
            pass
            
        self.thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.thread.start()

    def _stream_loop(self):
        while self._running:
            base_url = self.server_url.rstrip("/")
            stream_url = base_url if base_url.endswith("stream") else f"{base_url}/stream"

            try:
                cap = cv2.VideoCapture(stream_url)
                if cap.isOpened():
                    self.status = ReqStatus.connected
                    while self._running:
                        ret, frame = cap.read()
                        if ret and frame is not None:
                            self.current_frame = frame
                        else:
                            break
                cap.release()
            except Exception as e:
                if self._running:
                    print(f"Stream capture error: {e}")
            
            if self._running:
                self.status = ReqStatus.disconnected
                time.sleep(1)

    def getFrame(self):
        return self.current_frame

    @add_param
    def make_ping(self):
        try:
            url = self.server_url if self.server_url.endswith("/") else self.server_url + "/"
            response = requests.get(url + "ping", timeout=2)
            if response.text == ReqStatus.connected:
                self.status = ReqStatus.connected
                print(f"Ping exitoso, Estado: {self.status}")
            else:
                self.status = ReqStatus.disconnected
                print(f"Repsuesta del servidor no esperada: {response.text}")
        except Exception as e:
            self.status = ReqStatus.disconnected
            print(f"Error de red en ping: {e}")
        return self.status

    @add_param
    def set_url(self, url:str):
        if url.startswith("://"):
            self.server_url = "http" + url
        elif not url.startswith("http"):
            self.server_url = "http://" + url
        else:
            self.server_url = url

    def getParameters(self):
        return super().getParameters()
    
    def show(self):
        return super().show()
    
    def showInfo(self):
        return super().showInfo()

    def release(self):
        self._running = False
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join(timeout=1.0)

    def realese(self):
        self.release()