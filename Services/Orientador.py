import Calculador
import math

class Orientador(object):
    
    def __init__(self, c):
        self.cabeza = c
        c.start()
        
    def Reorientar(self,x,y,h,puntoCentro):
        direccionX = 1
        direccionY = 1
        if(x < self.cabeza.getCalibracion()[0]):
            direccionX = -1
        if(y < self.cabeza.getCalibracion()[1]):
            direccionY = -1
            
        distancia = Calculador.calcularDistancia(h/2)
        self.cabeza.puntoCalibracion = Calculador.calcularPuntoCalibracion(self.cabeza, distancia, puntoCentro)

        anguloHorizontal = Calculador.CalcularOrientacion(math.fabs(x-self.cabeza.getCalibracion()[0]),distancia)
        anguloVertical = Calculador.CalcularOrientacion(math.fabs(y-self.cabeza.getCalibracion()[1]),distancia)

        self.cabeza.setAngulo(anguloHorizontal*direccionX, 'x')
        self.cabeza.setAngulo(anguloVertical*direccionY, 'y')