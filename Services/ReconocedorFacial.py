import  numpy
import cv2
import RastreadorFacial
from cv2 import *



class ReconocerdorFacial(object):
    def __init__(self, hPath):
        self.clasificador = cv2.CascadeClassifier(hPath)
        

    def detectarTodos(self, imagen):
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY) #aplicamos filtro para poner la imagen en blanco y negro
        rostrosFrontal = self.clasificador.detectMultiScale( gris, scaleFactor = 1.2, minNeighbors = 5, minSize= (30,30), flags = cv2.CASCADE_SCALE_IMAGE)
        return rostrosFrontal;
        
    def detectar(self,imagen):
        seIndentifico = False
        rostrosFrontal = self.detectarTodos(imagen)
        if len(rostrosFrontal) == 1:
            seIndentifico = True
            for (x,y,w,h) in rostrosFrontal:
                return seIndentifico, x,y,w,h
            
        return False,0,0,0,0
    
    
        
       