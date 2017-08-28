import  numpy
import cv2
from cv2 import *

namedWindow("webcam")
cascadeFrontal = 'myhaar.xml'
rostroFrontalCascade = cv2.CascadeClassifier(cascadeFrontal)
def detectarCara(imagen):
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY) #aplicamos filtro para poner la imagen en blanco y negro
    rostrosFrontal = rostroFrontalCascade.detectMultiScale( gris, scaleFactor = 1.2, minNeighbors = 5, minSize= (30,30), flags = cv2.CASCADE_SCALE_IMAGE)
    return rostrosFrontal;
    