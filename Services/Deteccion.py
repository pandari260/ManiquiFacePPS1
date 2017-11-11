import cv2
from cv2 import *
import numpy as np




class DetectorHaar(object):
    def __init__(self, hPath):
        self.clasificador = cv2.CascadeClassifier(hPath)
        

    def detectarTodos(self, imagen):
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY) #aplicamos filtro para poner la imagen en blanco y negro
        cv2.equalizeHist(gris, gris)
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
    
    

limite = 10

class RastreadorFacial(object):


    def __init__(self,imagen,tracker):
        self.x,self.y,self.w,self.h = tracker
        self.imagen = imagen
        self.term_crit = None
        self.roi_hist = None
        self.track_window = tracker
        self.roi = None


    def identificarBlob(self):
        self.roi = self.imagen[self.y:self.y + self.h, self.x:self.x + self.w]
        self.hsv_roi = cv2.cvtColor(self.roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(self.hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        self.roi_hist = cv2.calcHist([self.hsv_roi], [0], mask, [180], [0, 180])
        cv2.normalize(self.roi_hist, self.roi_hist, 0, 255, cv2.NORM_MINMAX)
        self.term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, limite, 1)
    
    def rastrear(self, imagen):
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], self.getHist(), [0, 180], 1)
        ret, track_window = cv2.meanShift(dst, self.getTracker(), self.getCriterio())
        x, y, w, h = track_window
        
        return ret < limite, x,y,w,h
        


    def getImagen(self):
        return self.imagen

    def getHist(self):
        return self.roi_hist

    def getCriterio(self):
        return self.term_crit

    def getTracker(self):
        return self.track_window
       