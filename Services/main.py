from cv2 import *
import cv2
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
from DectectorDeObjetos import DetectorDeObjetos
from Services import ReconocedorFacial
from ReconocedorFacial import ReconocerdorFacial

ancho = 320
alto = 240
puntoCentro = (ancho/2,alto/2)
color = (0,255,0)
grosorFigura = 3
fuente = cv2.FONT_HERSHEY_SIMPLEX
textoInicio = ' coloque la palma de la mano en el recuadro para calibrar'
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
    detectorCara = DetectorDeObjetos('cascade.xml')
    detectorPalma = ReconocerdorFacial('palm.xml')
    detectorPuno = ReconocerdorFacial('fist.xml')
    seEncontroPalma = False
    seEncontroPuno = False
    vc = VideoCapture(0)
    vc.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, ancho)
    vc.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, alto)
    validadorDesp = ValidadorDesplazamiento(puntoCentro)
    namedWindow("webcam")
    
    puntoDeteccion = Array('i', 2)
    diametro = Value('i')
   
    procesos = []
    eventos = []
    cantCabezas = 0
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

        seEncontroCara, x,y,w,h = detectorCara.detectar(imagen)
       
        #cv2.rectangle(imagen,(x,y),(x+w,y+h), color, grosorFigura)
        cv2.rectangle(imagen,(x+w,y),(x+2*w,y+h), color, grosorFigura)

        
       
        puntoDeteccion[0] = x+w/2
        puntoDeteccion[1] = y+h/2
        diametro.value = h 
        if seEncontroCara:
            if(cont < cantCabezas + cantCabezasWeb ):#primero se calibran las cabezas
                cv2.putText(imagen,textoInicio,(5,15), fuente, 0.45,color,2)
                recorte = imagen[y:y+h, x+w:x+2*w]
                if not seEncontroPalma:
                    seEncontroPalma, xm,ym,wm, hm = detectorPalma.detectar(recorte)
                else:
                    cv2.circle(imagen,(x+w+w/2, y+h/2),4, (0,0,255), grosorFigura)
                    if(not seEncontroPuno):
                        seEncontroPuno, xp,yp,wp,hp = detectorPuno.detectar(recorte)
                    else:
                        procesos[cont].start()
                        cont += 1
                        seEncontroPalma = False
                        seEncontroPuno = False
            else:    
                if validadorDesp.validarDesplazamiento((x,y)):
                    for e in eventos:
                        e.set()
           
            imshow("webcam", imagen)
        sleep(0.1)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()