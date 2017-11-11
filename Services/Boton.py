
from cv2 import *
import sys

pd = 5
class Boton(object):
   
    def __init__(self, f, pos, path, *args):
        self.imagen = imread(path)
        self.accion = f
        self.posX = pos[0]
        self.posY = pos[1]
        self.tamX = self.imagen.shape[1]
        self.tamY = self.imagen.shape[0]
        self.argumentos = args
        #achicar la imagen directamente. Para no hace esto
        #self.redimensionada = resize(self.imagen, None,fx = 0.1, fy = 0.1, interpolation = INTER_CUBIC)
                 
    
    def dibujar(self, img):
        img[self.posY:self.posY + self.tamY, self.posX:self.posX+ self.tamX] = self.imagen
        return img
    def apretar(self):
        self.accion(self.argumentos[0], self.argumentos[1])


        





    
        
        
        