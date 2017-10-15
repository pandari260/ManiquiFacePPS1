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
from time import sleep
import RastreadorFacial

ancho = 320
alto = 240
puntoCentro = (ancho/2,alto/2)
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
    server.cabeza = cabeza
    server.diametro = diametro
    server.punto = punto
    server.puntoMedio = puntoMedio
    server.start_server()
    

def controlarRobot(cabeza, id, punto, diametro, puntoMedio,  eventoMover):
    while True:
        x = punto[0]
        y = punto[1]
        diametroCara = diametro.value
        if cabeza == None and x*y*diametroCara > 0:
            posicion = Calculador.calcularPosicionCabeza(puntoCentro, (x, y), diametroCara)

            cabeza = Cabeza.Cabeza((x, y), posicion, id)
        
        eventoMover.wait()
        Orientador.reorientar(x, y, diametroCara, cabeza, puntoMedio)
        eventoMover.clear()
        
def main():
    vc = VideoCapture(0)
    vc.set(cv2.CAP_PROP_FRAME_WIDTH, ancho)
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT, alto)
    validadorDesp = ValidadorDesplazamiento(puntoCentro)
    namedWindow("webcam")
    
    puntoDeteccion = Array('i', 2)
    diametro = Value('i')
   
    procesos = []
    eventos = []
    cantCabezas = 3
    cantCabezasWeb = 1
    cont= 0
    rastreadorCara = None
    for i in range(0, cantCabezas):
        c = None
        eventos.append(Event())
        procesos.append(Process(target= controlarRobot,  args=(c, i,puntoDeteccion,diametro, puntoCentro, eventos[0])))
    cabezaWeb = None
    procesos.append(Process(target= controlarThreejs, args = (cabezaWeb, 3, puntoDeteccion, diametro, puntoCentro)))
    seDebeUsarMeanshift = False
    seIdentificoBlob = False
    seEncontroCara = False
    while True:

        va, imagen = vc.read()
        imagen = cv2.flip(imagen, 1)
        cv2.circle(imagen,puntoCentro,4, color, grosorFigura)

        
        if(not seDebeUsarMeanshift):
            #print("se esta identificando")
            seEncontroCara,x,y,w,h = Reconocedor.detectarCara(imagen)#bool si se encontro cara, posicion (x,y), ancho y alto
            seDebeUsarMeanshift = seEncontroCara
        else:
            if not seIdentificoBlob:
                rastreadorCara = RastreadorFacial.RastreadorFacial(imagen, (x, y, w, h))
                rastreadorCara.identificarBlob()
                seIdentificoBlob = True
            else:
                #print("se esta rastreando")
                seEncontroCara, x,y,w,h = rastreadorCara.rastrear(imagen)   
                if(not seEncontroCara):
                    seDebeUsarMeanshift = False
                    seIdentificoBlob = False
            cv2.circle(imagen,(x+w/2,y+h/2),4, color, grosorFigura)
        
       
        puntoDeteccion[0] = x+w/2
        puntoDeteccion[1] = y+h/2
        diametro.value = h 

        if seEncontroCara:
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
        sleep(0.25)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()