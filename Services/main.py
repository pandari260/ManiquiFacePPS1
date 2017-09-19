from cv2 import *
import cv2
import ReconocedorFacial as Reconocedor
import ValidadorDesplazamiento 
import Calculador 
import math
import numpy as np
import ManiquiFacePPS1.Modelo.Hardware.Cabeza as Cabeza

punto90 = (0,240)
color = (0,255,0)
grosorFigura = 5
distanciaCabezaObjetoDetectado = 100
textoInicio = 'Para comenzar por favor coloquese frente a la cabeza y presione C para calibrar'
textoCalibracion = 'Punto de calibracion: '
textoRecalibrar = "presione R para recalibrar"

def main():
    vc = VideoCapture(0)
    validadorDesp = ValidadorDesplazamiento.ValidadorDesplazamiento(punto90) 
    namedWindow("webcam")
    cabeza = None
    track_window = None
    term_crit = None
    flag = False
    roi_hist = None

    while True:
        va, imagen = vc.read()
        imagen = cv2.flip(imagen, 1)
        carasEncontradas = Reconocedor.detectarCara(imagen)

        for (x, y, w, h) in carasEncontradas:
            if len(carasEncontradas) ==1:
                track_window = (x, y, w, h)
                roi = imagen[y:y + h, x:x + w]
                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
                roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
                cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
                term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
                flag = True

        if(flag == True):
            ret, imagen = vc.read()
            imagen = cv2.flip(imagen, 1)

            hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
            ret, track_window = cv2.meanShift(dst, track_window, term_crit)
            x, y, w, h = track_window
            cv2.rectangle(imagen, (x, y), (x + w, y + h), (0,255,0), 3)

        if(cabeza == None):
            fuente = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(imagen,textoInicio,(5,15), fuente, 0.45,(0,255,0),2)
            if waitKey(1) & 0xFF == ord('c'):
                cabeza = Cabeza.Cabeza((x,y))
                cabeza.start()

        else:
            cv2.putText(imagen,textoCalibracion,cabeza.getCalibracion(), fuente, 1,(0,255,0),2)

            cv2.circle(imagen,(cabeza.getCalibracion()[0]+2,cabeza.getCalibracion()[1]+10),1, color, grosorFigura)

            if validadorDesp.validarDesplazamiento((x,y)):
                direccionX = 1;
                direccionY = 1
                if(x < cabeza.getCalibracion()[0]):
                    direccionX = -1
                if(y < cabeza.getCalibracion()[1]):
                    direccionY = -1

                distancia = Calculador.calcularDistancia(h/2)
                anguloHorizontal = Calculador.CalcularDesplazamiento(math.fabs(x-cabeza.getCalibracion()[0]),distancia)
                anguloVertical = Calculador.CalcularDesplazamiento(math.fabs(y-cabeza.getCalibracion()[1]),distancia)

                cabeza.setAngulo(anguloHorizontal*direccionX, 'x')
                cabeza.setAngulo(anguloVertical*direccionY, 'y')


        imshow("webcam", imagen)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
main()