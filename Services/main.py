from cv2 import * 
import cv2 
from ValidadorDesplazamiento import ValidadorDesplazamiento 
import Calculador 
import numpy as np 
import Cabeza as Cabeza 
from multiprocessing import Process, Array, Value, Event 
import multiprocessing 
import Orientador 
import server 
from time import sleep 
from DectectorDeObjetos import DetectorDeObjetos 
from ReconocedorFacial import ReconocerdorFacial 
from Comunicador import Comunicador 
import Boton
import time
import sys 
ancho = 320.0 
alto = 240.0 
puntoCentro = (ancho/2,alto/2) 
color = (0,255,0) 
grosorFigura = 3 
fuente = cv2.FONT_HERSHEY_SIMPLEX 
textoInicio = ' coloque la palma de la mano en el recuadro para calibrar' 
textoCalibracion = 'Cabeza' 
textoRecalibrar = "presione R para recalibrar" 
PORT = 8080
def estaEnRango(valor, rango):
    print("valor: " + str(valor))
    print("rango: " + str(rango))
    return valor >= rango[0] and valor <= rango[1]
    
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
    #comunicador = Comunicador(35,33)
    predeV = None
    predeH = None   
    while True:
        x = punto[0]
        y = punto[1]
        diametroCara = diametro.value
        if cabeza == None and x*y*diametroCara > 0:
            posicion = Calculador.calcularPosicionCabeza(puntoCentro, (x, y), diametroCara)

            cabeza = Cabeza.Cabeza((x, y), posicion, id)
            
        eventoMover.wait()
        gx, gy = Orientador.reorientar(x, y, diametroCara, cabeza, puntoMedio)

        if(predeH != None and gx!=0 and gy!=0):
            if(abs(predeH-gx)>=5 or abs(predeV-gy)>=2):
                #comunicador.iniciarOrientacion()
                if(gx > predeH):
                    while(gx > predeH):
                        print("predecesor:"+str(predeH))
                        print("X:"+str(gx))
                        predeH +=5
                        #comunicador.enviarOrientacion(predeH,gy)
    
                elif(gx < predeH):
                    while(gx < predeH):
                        print("predecesor2:"+str(predeH))
                        print("X2:"+str(gx))
                        predeH -=5
                        #comunicador.enviarOrientacion(predeH,gy)
                predeH = gx
                predeV = gy
                #comunicador.enviarOrientacion(predeH,gy)
        #comunicador.detenerOrientacion()

        if(predeH == None and predeV == None):
            predeH = gx
            predeV = gy
        eventoMover.clear()
        
def main():
    #detectores de objetos
    detectorCara = DetectorDeObjetos('cascade.xml')
    detectorPunio = DetectorDeObjetos('fist.xml')
    detectorPalma = ReconocerdorFacial('palm.xml')
    detectorPuno = ReconocerdorFacial('fist.xml')
    
    #banderas
    seEncontroPalma = False
    seEncontroPuno = False
    
    #inicializacion de la camara
    vc = VideoCapture(0)
    vc.set(cv2.CAP_PROP_FRAME_WIDTH, ancho)
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT, alto)
    validadorDesp = ValidadorDesplazamiento(puntoCentro)
    namedWindow("webcam")
    
    #objetos compratidos entre procesos
    puntoDeteccion = Array('i', 2)
    diametro = Value('i')
   
   #declaracion de procesos
    procesos = []
    eventos = []
    
    #cantidad de cabezas
    cantCabezas = 1
    cantCabezasWeb = 0
    cont= 0
    
    #botones
    botonSalir = Boton.Boton(Boton.salir,(ancho, alto), "manito.png")
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
        imagen, ranX, ranY = botonSalir.posicionar(x, y, imagen, (ancho,alto))
        seEncontroPunio, xP,yP,wP,hP = detectorPunio.detectar(imagen)
        cv2.rectangle(imagen,(xP,yP),(xP+wP,yP+hP), color, grosorFigura)

        print("-------------------------------------------")
        if(seEncontroPunio and estaEnRango(xP,ranX) and estaEnRango(yP, ranY)):
            botonSalir.apretar()
   
        puntoDeteccion[0] = x+w/2
        puntoDeteccion[1] = y+h/2
        diametro.value = h 
        if seEncontroCara:
            if(cont < cantCabezas + cantCabezasWeb ):#primero se calibran las cabezas
                cv2.rectangle(imagen,(x+w,y),(x+2*w,y+h), color, grosorFigura)
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
                        print("entro")
                        e.set()
            
            imshow("webcam", imagen)
        sleep(0.1)
       
        if waitKey(1) & 0xFF == ord('q'):
            sys.exit()
 
        
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
