
from cv2 import *
import sys

pd = 5
class Boton(object):
   
    def __init__(self, f, path):
        self.imagen = imread(path)
        self.accion = f
        self.posX = None
        self.posY = None
        #achicar la imagen directamente. Para no hace esto
        self.redimensionada = resize(self.imagen, None,fx = 0.1, fy = 0.1, interpolation = INTER_CUBIC)
                 
    def posicionar(self, x,y, img, resolucion):
       
        self.posY = (y/pd,y/pd+self.redimensionada.shape[0])
        self.posX = (x/pd,x/pd+self.redimensionada.shape[1])
        
        return self.posX,self.posY
    def dibujar(self, img):
        img[self.posY[0]:self.posY[1], self.posX[0]:self.posX[1]] = self.redimensionada
        return img
    def apretar(self):
        self.accion();

#funciones que ejecutan los botones
def salir():
    sys.exit()
    
def movimientoPredefinido():
    print("se apreto el boton")
    pass

        





    
        
        
        