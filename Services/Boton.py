
from cv2 import *
import sys
class Boton(object):
   
    def __init__(self, f, p, path):
        self.imagen = imread(path)
        self.accion = f
                 
    def posicionar(self, x,y, img, resolucion):
       
        redimensionada = resize(self.imagen, None,fx = 0.1, fy = 0.1, interpolation = INTER_CUBIC)
        posY = (y/2,y/2+redimensionada.shape[0])
        posX = (x/2,x/2+redimensionada.shape[1])
        img[posY[0]:posY[1], posX[0]:posX[1]] = redimensionada
        return img, posX,posY
    def apretar(self):
        self.accion();

#funciones que ejecutan los botones
def salir():
    sys.exit()
        





    
        
        
        