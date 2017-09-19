from cv2 import *
import cv2
import numpy as np

class TrackerFace(object):


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
        self.term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)


    def getImagen(self):
        return self.imagen

    def getHist(self):
        return self.roi_hist

    def getCriterio(self):
        return self.term_crit

    def getTracker(self):
        return self.track_window