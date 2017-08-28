import cv2
class Camara(object):
   


    def __init__(self, t):
        self.tipo = t #indica cual con cual de las camaras instaldas se quiere conectar 0 si solo hay 1
        self.conexion = None
    
    def conectarCamara(self):
        self.conexion = cv2.VideoCapture(self.tipo)
    
    def tomarFoto(self):
        val, imagen = self.conexion.read()
        return imagen
    
    
    
        