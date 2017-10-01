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
fuente = cv2.FONT_HERSHEY_SIMPLEX
textoInicio = 'Para comenzar por favor coloquese frente a la cabeza y presione C para calibrar'
textoCalibracion = 'Cabeza'
textoRecalibrar = "presione R para recalibrar"

def main():
    vc = VideoCapture(0)
    validadorDesp = ValidadorDesplazamiento.ValidadorDesplazamiento(puntoCentro)
    namedWindow("webcam")
    orientadores = []
   

    while True:
        va, imagen = vc.read()
        imagen = cv2.flip(imagen, 1)
        flag,x,y,w,h = Reconocedor.detectarCara(imagen)#bool si se encontro cara, posicion (x,y), ancho y alto

        #cv2.rectangle(imagen, (x, y), (x + w, y + h), color, 3)
        cv2.circle(imagen,(x,y),4, color, grosorFigura)

        if flag:
            if(orientadores.__len__() < 1):
                cv2.putText(imagen,textoInicio,(5,15), fuente, 0.45,color,2)
                if waitKey(1) & 0xFF == ord('c'):
                    posicion = Calculador.calcularPosicionCabeza(puntoCentro, (x,y), h)
                    nuevaCabeza = Cabeza.Cabeza((x,y), posicion, orientadores.__len__())
                    orientador = Orientador(nuevaCabeza)
                    orientador.start()
                    orientadores.append(orientador)

    
            else:
                for c in orientadores:
                    cv2.circle(imagen,(c.cabeza.getCalibracion()[0]+2,c.cabeza.getCalibracion()[1]+10),1, color, grosorFigura)
                    cv2.putText(imagen,textoCalibracion + str(c.cabeza.id),c.cabeza.getCalibracion(), fuente, 0.5,color,2)

    
                if validadorDesp.validarDesplazamiento((x,y)):
                    for c in orientadores:
                        c.Reorientar(x, y, h)
                                                
                       




        imshow("webcam", imagen)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
main()