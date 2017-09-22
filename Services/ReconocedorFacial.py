import  numpy
import cv2
import RastreadorFacial
from cv2 import *

namedWindow("webcam")
cascadeFrontal = 'cascade.xml'
rostroFrontalCascade = cv2.CascadeClassifier(cascadeFrontal)
rastreadorCara = None
flagIdentificado = False

def detectarTodasCaras(imagen):
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY) #aplicamos filtro para poner la imagen en blanco y negro
    rostrosFrontal = rostroFrontalCascade.detectMultiScale( gris, scaleFactor = 1.2, minNeighbors = 5, minSize= (30,30), flags = cv2.CASCADE_SCALE_IMAGE)
    return rostrosFrontal;
    
def detectarCara(imagen):
    carasEncontradas = detectarTodasCaras(imagen)
    global rastreadorCara
    global flagIdentificado
    x = 0
    y = 0
    w = 0
    h = 0

    if len(carasEncontradas) == 0:
        flagIdentificado = False

    for (x, y, w, h) in carasEncontradas:
        if len(carasEncontradas) ==1:
            rastreadorCara = RastreadorFacial.RastreadorFacial(imagen, (x, y, w, h))
            rastreadorCara.identificarBlob()
            flagIdentificado = True

    if rastreadorCara != None and flagIdentificado:
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], rastreadorCara.getHist(), [0, 180], 1)
        ret, track_window = cv2.meanShift(dst, rastreadorCara.getTracker(), rastreadorCara.getCriterio())
        x, y, w, h = track_window
    return flagIdentificado,x,y,w,h
    
   