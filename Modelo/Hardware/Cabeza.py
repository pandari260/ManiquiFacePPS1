import ServoMotor
limites = {'x' : [90,0,180], 'y' : [90,0,180]}
import ComunicadorSerial
from threading import Thread
from threading import Event



class Cabeza(Thread):
    
    def girar(self, grados, eje):
        inf = limites[eje][1]
        sup = limites[eje][2]
        angulo = self.posiciones[eje]
        
        if(angulo > sup):
            print("entro en superior")
            angulo = sup
        elif(angulo < inf):
            angulo = inf
    
        self.comunicador.enviarDatos(eje+chr(angulo))
   

    def __init__(self, calibracion):
        Thread.__init__(self)
        self.puntoCalibracionInicial = calibracion
        self.distanciaHorizontal = 115 #cambiar por la funcion que calcula la distancia
        self.distanciaVertical = 53
        self.comunicador = ComunicadorSerial.ComunicadorSerial()
        self.posiciones = {}
        self.posiciones['x'] = limites['x'][0]
        self.posiciones['y'] = limites['y'][0]
        self.girar(self.posiciones['x'], 'x')
        self.girar(self.posiciones['y'], 'y')
        self.evento = Event()
       
        
        
    def run(self):
        while True:
            self.evento.wait()
            self.girar(self.posiciones['x'], 'x')
            self.girar(self.posiciones['y'], 'y')
            self.evento.clear()
    
    def setAngulo(self, angulo, eje):
        self.posiciones[eje] = angulo + limites[eje][0]
        self.evento.set()
        
    def getDistanciaHorizontal(self):
        return self.distanciaHorizontal
    def getDistanciaVerical(self):
        return self.distanciaVertical
    def getCalibracion(self):
        return self.puntoCalibracionInicial
   
        
       
