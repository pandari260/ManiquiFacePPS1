
from cv2 import *
class Boton(object):
   
    def __init__(self, p, path):
        self.imagen = imread(path) 
    
    def insertarBotonImagen(self, x,y, img, resolucion):
        y = y/2
        x = x/2
        redimensionada = resize(self.imagen, None,fx = 0.1, fy = 0.1, interpolation = INTER_CUBIC)
        img[y:y+redimensionada.shape[0], x:x+redimensionada.shape[1]] = redimensionada
        return img





    
        
        
        