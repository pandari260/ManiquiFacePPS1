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
from Services.Deteccion import DetectorHaar 
from Comunicador import Comunicador 
import Boton
import time
import sys 

import Secuencia
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


#inicializacion de la camara
vc = VideoCapture(0)
vc.set(cv2.CAP_PROP_FRAME_WIDTH, ancho)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, alto)

def sacarFoto():
    _, imagen = vc.read()
    return cv2.flip(imagen, 1)


def seDebeApretar(x, y, boton):
    return (x >= boton.posX and x <= (boton.posX + boton.tamX)) and (y >= boton.posY and y <= (boton.posY + boton.tamY))

    
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
        

    
def funcionCabezasRoboticas(cRobot, cWeb):
    #detectores de objetos
    detectorCara = DetectorDeObjetos('cascade.xml')
    detectorPalma = DetectorHaar('palm.xml')
    detectorPuno = DetectorHaar('fist.xml')
    
    #banderas
    seEncontroPalma = False
    seEncontroPuno = False
    
    validadorDesp = ValidadorDesplazamiento(puntoCentro)
    
    
    #objetos compratidos entre procesos
    puntoDeteccion = Array('i', 2)
    diametro = Value('i') 
    
    #cantidad de cabezas
    cantCabezas = cRobot
    cantCabezasWeb = cWeb
    cont= 0             
               
    #declaracion de procesos
    procesos = []
    eventos = []
    
    #instansiacion de procesos
    for i in range(0, cantCabezas):
        c = None
        eventos.append(Event())
        procesos.append(Process(target= controlarRobot,  args=(c, i,puntoDeteccion,diametro, puntoCentro, eventos[0])))
    cabezaWeb = None
    procesos.append(Process(target= controlarThreejs, args = (cabezaWeb, 3, puntoDeteccion, diametro, puntoCentro)))
    
    while True:
        imagen = sacarFoto()
        

        seEncontroCara, x,y,w,h = detectorCara.detectar(imagen)
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
                        destroyWindow("ManiquiFace")
            else:    
                if validadorDesp.validarDesplazamiento((x,y)):
                    for e in eventos:
                        print("entro")
                        e.set()
            
            imshow("ManiquiFace", imagen)
        sleep(0.1)
       
        if waitKey(1) & 0xFF == ord('q'):
            sys.exit()

def funcionMovimientoPredefinido(secuencia, cant):
    #cantidad de cabezas
    cantCabezas = cant
    
    #declaracion de procesos
    procesos = []
    eventos = []
    
    #objetos compratidos entre procesos
    puntoDeteccion = Array('i', 2)
    diametro = Value('i') 

    pasoInicial = secuencia.posIncial
    puntoDeteccion[0] = pasoInicial[0]
    puntoDeteccion[1] = pasoInicial[1]
    diametro.value = secuencia.diametro

    #instansiacion de procesos
    for i in range(0, cantCabezas):
        c = None
        eventos.append(Event())
        procesos.append(Process(target= controlarRobot,  args=(c, i,puntoDeteccion,diametro, puntoCentro, eventos[0])))
        procesos[i].start()
    
    while True:
        paso = secuencia.getNext()
        x = paso["x"]
        y = paso["y"]
        
        puntoDeteccion[0] = x
        puntoDeteccion[1] = y
        diametro.value = secuencia.diametro
        
        for e in eventos:
            e.set()            
        sleep(paso["sleep"])
        
        if waitKey(1) & 0xFF == ord('q'):
            sys.exit()
        
    
def main():
    detectorPalma = DetectorDeObjetos('fist.xml')  
    fondo = cv2.imread("Fondo.png")
    
    pos1 = (10,50)
    pos2 = (240, 50)
    pos3 = (460, 50)
    botonPredefinido = Boton.Boton(funcionMovimientoPredefinido, pos1, "button_movimiento-predefinido.png", Secuencia.Secuencia(Secuencia.hardcodeada, (320,240)), 3)
    botonCabezaVirtual = Boton.Boton(funcionCabezasRoboticas, pos2, "button_cabeza-virtual.png", 0,1)
    botonCabezaRobotica = Boton.Boton(funcionCabezasRoboticas,pos3, "button_seguimiento-facial.png", 1, 0)
    fondo = botonCabezaVirtual.dibujar(fondo)
    fondo = botonPredefinido.dibujar(fondo)
    fondo = botonCabezaRobotica.dibujar(fondo)



    

    botones = []
    botones.append(botonPredefinido)
    botones.append(botonCabezaVirtual)
    botones.append(botonCabezaRobotica)
    
    seApretoUnBoton =False
    eleccion = None
    fondoConPuntero = np.copy(fondo) 
          
    while not seApretoUnBoton:
        imagen = sacarFoto()
        #texto de la interface

        seEncontroMano, xM, yM, wM, hM = detectorPalma.detectar(imagen)
        fondo[200:440,200:520] = imagen
        fondoConPuntero = np.copy(fondo) 



        if (seEncontroMano):
            cv2.putText(imagen,'Elija una opcion',(10,30), cv2.FONT_ITALIC, 1,(255,255,255),2,cv2.LINE_4)

            cv2.rectangle(imagen,(xM+wM,yM),(xM+2*wM,yM+hM), color, grosorFigura)
            
            circle(fondoConPuntero,(xM*2, yM*2), 3, (255,0,0), 3);
            for boton in botones:
                if(not seApretoUnBoton and seDebeApretar(xM*2, yM*2, boton)):
                    eleccion = boton
                    seApretoUnBoton = True
        imshow("ManiquiFace", fondoConPuntero)
        sleep(0.1)
        if waitKey(1) & 0xFF == ord('q'):
            break;
    destroyWindow("ManiquiFace")
                   
    eleccion.apretar()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
