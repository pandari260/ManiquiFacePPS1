import serial
class ComunicadorSerial:
  
    def __init__(self):
        self.arduino = serial.Serial('/dev/ttyUSB0', 9600)
    
    def enviarDatos(self,valor):
        self.arduino.write(bytes(valor))
       