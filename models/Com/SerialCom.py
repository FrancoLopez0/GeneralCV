from ..interfaces import iCom
from models.types import ComboInputType
import serial
import serial.tools.list_ports as list_ports
from ..decorators import add_param

class SerialCom(iCom):
    def __init__(self):
        super().__init__()
        
        self.port = None
        self.badurate = 9600
        self.com = None
        self.ports = []
        self.char_init = 255
        self.char_deinit = 0

        self.scan()
            
    def setBaudRate(self, baud):
        self.badurate = baud

    def setPort(self, port):
        self.port = port

    def getParameters(self):
        return super().getParameters()
    
    def recieve(self):
        return super().recieve()
    
    def send(self, value):
        self.com.write(value)
        return super().send()
    
    def showInfo(self):
        return super().showInfo()
    
    def process(self, cvResponse):
        return

    @add_param
    def connect(self, port: ComboInputType, baudrate: ComboInputType = ["9600", "115200"]):
        print(f'Conectando..... al puerto: {port} a {int(baudrate)}')
        self.setPort(port)
        self.com = serial.Serial(port, int(baudrate))
        if self.com.is_open:
            print("CONECTADO")
        else:
            print("Error de conexion")
        return 

    def scan(self):
        rawPorts = list(list_ports.comports())
        self.ports = []
        for port in rawPorts:
            print(f"Puerto: {port.device}, Descripción: {port.description}, GUID: {port.hwid}")
            self.ports.append(port.device)
        
        return self.ports

    @add_param
    def close(self):
        print(f'Cerrando puerto: {self.port}')
        pwm = 0

        if self.com.is_open:
            self.com.write(pwm.to_bytes())
            self.com.close()
            print("Desconectado")
        else:
            pass
        return 

# if __name__ == "__main__":
#     print("Escanenado puertos....")
#     rawPorts = list(list_ports.comports())
#     self.ports = []
#         for port in rawPorts:
#             print(f"Puerto: {port.device}, Descripción: {port.description}, GUID: {port.hwid}")
#             self.ports.append(port.device)
