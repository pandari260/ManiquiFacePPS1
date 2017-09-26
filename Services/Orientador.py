import Calculador
import math
from threading import Thread
from threading import Event


class Orientador(Thread):
    
    def __init__(self, c):
        Thread.__init__(self)
        self.cabeza = c
        self.puntoDeteccion = None
        self.diametroCara = None
        self.puntoMedio = (320, 240)
        self.evento = Event()

    
    def run(self):
        while True:
            self.evento.wait()
            direccionX = 1
            direccionY = 1
            if(self.puntoDeteccion[0]< self.cabeza.getCalibracion()[0]):
                direccionX = -1
            if(self.puntoDeteccion[1] < self.cabeza.getCalibracion()[1]):
                direccionY = -1
                
            distancia = Calculador.calcularDistancia(self.diametroCara/2)
            self.cabeza.puntoCalibracion = Calculador.calcularPuntoCalibracion(self.cabeza, distancia, self.puntoMedio)
    
            anguloHorizontal = Calculador.CalcularOrientacion(math.fabs(self.puntoDeteccion[0]-self.cabeza.getCalibracion()[0]),distancia)
            anguloVertical = Calculador.CalcularOrientacion(math.fabs(self.puntoDeteccion[1]-self.cabeza.getCalibracion()[1]),distancia)
    
            self.cabeza.girar(anguloHorizontal*direccionX, 'x')
            self.cabeza.girar(anguloVertical*direccionY, 'y')
            self.evento.clear()

        
        
    def Reorientar(self,x,y,h):
        self.evento.set()
        self.puntoDeteccion = (x,y)
        self.diametroCara = h
       