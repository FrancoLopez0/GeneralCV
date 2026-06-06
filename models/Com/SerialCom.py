from ..interfaces import iCom
from models.types import ComboInputType
import serial
import serial.tools.list_ports as list_ports
from ..decorators import add_param
import struct

def send_angles(ser, angles):
    # Empaquetar datos: inicio (0xFF), ángulos (cada uno como 2 bytes), checksum, fin (0xFE)
    packet = bytearray()
    packet.append(0xFF)  # Byte de inicio
    
    checksum = 0xFF
    for angle in angles:
        angle_bytes = struct.pack('>H', angle)  # 2 bytes (big-endian)
        packet.extend(angle_bytes)
        checksum ^= angle_bytes[0]  # XOR para checksum
        checksum ^= angle_bytes[1]
    
    packet.append(checksum)
    packet.append(0xFE)  # Byte de fin
    
    ser.write(packet)  # Enviar el paquete

class SerialCom(iCom):
    def __init__(self):
        super().__init__()
        
        self.port = None
        self.badurate = 115200
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
    
    def send(self, values):
        if not self.com or not self.com.is_open:
            return super().send()

        try:
            packet = bytearray()
            packet.append(0xFF)  # Byte de inicio
            
            checksum = 0xFF
            for val in values:
                # Limitamos entre 0.0 y 1.0 por si el modelo tira algún valor basura
                v = max(0.0, min(1.0, float(val)))
                
                # Empaquetar como float de 4 bytes (big-endian)
                float_bytes = struct.pack('>f', v)
                packet.extend(float_bytes)
                
                # XOR para checksum con los 4 bytes
                for b in float_bytes:
                    checksum ^= b
            
            packet.append(checksum)
            packet.append(0xFE)  # Byte de fin
            
            self.com.write(packet)
            
        except Exception as e:
            print(f"Error empaquetando/enviando serial: {e}")
            
        return super().send()
    
    def showInfo(self):
        return super().showInfo()
    
    def process(self, cvResponse):
        # try:
        # print(cvResponse)
        try:
            if cvResponse:
                self.send(cvResponse)
        except:
            pass
        # except:
        #     pass
        # self.send = cvResponse.fingers_state[1]
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
