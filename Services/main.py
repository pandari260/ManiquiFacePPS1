from cv2 import *
import cv2
import ReconocedorFacial as Reconocedor
from ValidadorDesplazamiento import ValidadorDesplazamiento
import Calculador
import math
import numpy as np
import Modelo.Hardware.Cabeza as Cabeza
from multiprocessing import Process, Array, Value, Event
import multiprocessing
import Orientador
import server

puntoCentro = (320,240)
color = (0,255,0)
grosorFigura = 5
fuente = cv2.FONT_HERSHEY_SIMPLEX
textoInicio = 'Para comenzar por favor coloquese frente a la cabeza y presione C para calibrar'
textoCalibracion = 'Cabeza'
textoRecalibrar = "presione R para recalibrar"
PORT = 8080

def controlarThreejs(cabeza, id, punto, diametro, puntoMedio):
    x = punto[0]
    y = punto[1]
    diametroCara = diametro.value
    posicion = Calculador.calcularPosicionCabeza(puntoCentro, (x, y), diametroCara)
    cabeza = Cabeza.Cabeza((x, y), posicion, id)
    server.start_server(PORT, cabeza, punto, diametro, puntoMedio)
    

def controlarRobot(cabeza, id, punto, diametro, puntoMedio,  eventoMover):
    while True:
        x = punto[0]
        y = punto[1]
        diametroCara = diametro.value
        if cabeza == None:
            posicion = Calculador.calcularPosicionCabeza(puntoCentro, (x, y), diametroCara)
            cabeza = Cabeza.Cabeza((x, y), posicion, id)
        
        eventoMover.wait()
        Orientador.reorientar(x, y, diametroCara, cabeza, puntoMedio)
        eventoMover.clear()
        
def main():
    vc = VideoCapture(0)
    validadorDesp = ValidadorDesplazamiento(puntoCentro)
    namedWindow("webcam")
    
    puntoDeteccion = Array('i', 2)
    diametro = Value('i')
   
    procesos = []
    eventos = []
    cantCabezas = 3
    cantCabezasWeb = 1
    cont= 0
    for i in range(0, cantCabezas):
        c = None
        eventos.append(Event())
        procesos.append(Process(target= controlarRobot,  args=(c, i,puntoDeteccion,diametro, puntoCentro, eventos[0])))
    cabezaWeb = None
    procesos.append(Process(target= controlarThreejs, args = (cabezaWeb, 3, puntoDeteccion, diametro, puntoCentro)))

    while True:
        va, imagen = vc.read()
        imagen = cv2.flip(imagen, 1)
        flag,x,y,w,h = Reconocedor.detectarCara(imagen)#bool si se encontro cara, posicion (x,y), ancho y alto
        puntoDeteccion[0] = x
        puntoDeteccion[1] = y
        diametro.value = h 
        
        cv2.circle(imagen,(x,y),4, color, grosorFigura)

        if flag:
            if(cont < cantCabezas + cantCabezasWeb ):#primero se calibran las cabezas
                cv2.putText(imagen,textoInicio,(5,15), fuente, 0.45,color,2)
                if waitKey(1) & 0xFF == ord('c'):
                    procesos[cont].start()
                    cont += 1
            else:    
                if validadorDesp.validarDesplazamiento((x,y)):
                    for e in eventos:
                        e.set()
        imshow("webcam", imagen)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()