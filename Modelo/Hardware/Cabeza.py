limites = {'x' : [90,0,180], 'y' : [90,0,180]}
import ComunicadorSerial
from threading import Thread



class Cabeza(object):
    
    def girar(self, grados, eje):
        inf = limites[eje][1]
        sup = limites[eje][2]
        angulo = grados + limites[eje][0]
        
        if(angulo > sup):
            print("entro en superior")
            angulo = sup
        elif(angulo < inf):
            angulo = inf
    
        #self.comunicador.enviarDatos(eje+chr(angulo))
        print("la cabeza giro al angulo:" + str(angulo) + " en el eje" + eje)

    def __init__(self, calibracion, p):
        self.puntoCalibracion = calibracion
        #self.comunicador = ComunicadorSerial.ComunicadorSerial()
        self.posicion = p
        self.girar(limites['x'][0], 'x')
        self.girar(limites['y'][0], 'y')
       
        
        
        
    def getDistanciaHorizontal(self):
        return self.distanciaHorizontal
    def getDistanciaVerical(self):
        return self.distanciaVertical
    def getCalibracion(self):
        return self.puntoCalibracion
   
        
       
