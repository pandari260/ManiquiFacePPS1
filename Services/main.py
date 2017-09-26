from cv2 import *
import cv2
import ReconocedorFacial as Reconocedor
import ValidadorDesplazamiento 
import Calculador
import math
import numpy as np
import Modelo.Hardware.Cabeza as Cabeza
from Orientador import Orientador

puntoCentro = (320,240)
color = (0,255,0)
grosorFigura = 5
textoInicio = 'Para comenzar por favor coloquese frente a la cabeza y presione C para calibrar'
textoCalibracion = 'Punto de calibracion: '
textoRecalibrar = "presione R para recalibrar"

def main():
    vc = VideoCapture(0)
    validadorDesp = ValidadorDesplazamiento.ValidadorDesplazamiento(puntoCentro)
    namedWindow("webcam")
    cabeza = None
    orientador = None
   

    while True:
        va, imagen = vc.read()
        imagen = cv2.flip(imagen, 1)
        flag,x,y,w,h = Reconocedor.detectarCara(imagen)#bool si se encontro cara, posicion (x,y), ancho y alto

        cv2.rectangle(imagen, (x, y), (x + w, y + h), (0,255,0), 3)
        if flag:
            if(cabeza == None):
                fuente = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(imagen,textoInicio,(5,15), fuente, 0.45,color,2)
                if waitKey(1) & 0xFF == ord('c'):
                    posicion = Calculador.calcularPosicionCabeza(puntoCentro, (x,y), h)
                    cabeza = Cabeza.Cabeza((x,y), posicion)
                    orientador = Orientador(cabeza)
                    orientador.start()
    
            else:
    
                cv2.circle(imagen,(cabeza.getCalibracion()[0]+2,cabeza.getCalibracion()[1]+10),1, color, grosorFigura)
    
                if validadorDesp.validarDesplazamiento((x,y)):
                    orientador.Reorientar(x, y, h)
                    cv2.putText(imagen,textoCalibracion,cabeza.getCalibracion(), fuente, 1,color,2)



        imshow("webcam", imagen)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
main()