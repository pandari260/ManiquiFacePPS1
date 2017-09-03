from Modelo.Hardware.ServoMotor import ServoMotor
limites = {'x' : [90,0,180], 'y' : [90,0,180]}
#import ComunicadorSerial


class Cabeza(object):
    
    def girar(self, grados, eje):
        inf = limites[eje][1]
        sup = limites[eje][2]
        print(sup)
        
        angulo = limites[eje][0] + grados
        if(angulo > sup):
            print("entro en superior")
            angulo = sup
        elif(angulo < inf):
            angulo = inf
    
        #self.comunicador.enviarDatos(eje+str(angulo))
        print("la cabeza giro al angulo: " + str(angulo))
   

    def __init__(self, calibracion):
        self.puntoCalibracionInicial = calibracion
        self.distanciaCamara = 115 #cambiar por la funcion que calcula la distancia
        #self.comunicador = ComunicadorSerial.ComunicadorSerial()
        self.girar(limites['x'][0], 'x')
        self.girar(limites['y'][0], 'y')
        
    def getDistanciaCamara(self):
        return self.distanciaCamara

        
       
        
    
    
    def getCalibracion(self):
        return self.puntoCalibracionInicial
   
        
       
