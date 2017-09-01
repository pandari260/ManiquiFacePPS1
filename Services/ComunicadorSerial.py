import serial
class ComunicadorSerial:
  
    def __init__(self,puerto):
        self.arduino = serial.Serial(puerto, 9600)
    
    def enviarDatos(self,valor):
        self.arduino.write(bytes(valor))
       