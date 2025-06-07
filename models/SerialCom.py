from .interfaces import iCom
from models.types import ComboInputType
import serial
import serial.tools.list_ports as list_ports
from .decorators import add_param

class SerialCom(iCom):
    def __init__(self):
        super().__init__()
        
        self.port = None
        self.badurate = 9600
        self.com = None
        self.ports = []
            
    def setBaudRate(self, baud):
        self.badurate = baud

    def setPort(self, port):
        self.port = port

    def getParameters(self):
        return super().getParameters()
    
    def recieve(self):
        return super().recieve()
    
    def send(self):
        return super().send()
    
    def showInfo(self):
        return super().showInfo()
    
    def connect(self):
        self.com = serial.Serial(self.port, self.badurate)

    @add_param
    def selectPort(self, port: ComboInputType):
        print(f'Conectando..... al puerto: {port}')
        self.setPort(port)
        self.com = serial.Serial(port, self.badurate)
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
        self.com.close()