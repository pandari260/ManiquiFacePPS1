from Modelo.Hardware.ServoMotor import ServoMotor
limites = {'x' : [90,45,135], 'y' : [90,45, 135]}# [posicion inicial, limite inferior, limite superior]

class Cabeza(object):
   

    def __init__(self):
        servoX = ServoMotor(limites['x'][0])
        servoY = ServoMotor(limites['y'][0])
        self.servos = {}
        self.servos['x'] = servoX
        self.servos['y'] = servoY
        
       
        
    def girar(self, grados, eje):
        servo = self.servos[eje]
        inf = limites[eje][1]
        sup = limites[eje][2]
        
        sum = servo.orientacion + grados
        if(sum > sup):
            servo.girar(sup)
        elif(sum < inf):
            servo.girar(inf)
        else:
            servo.girar(sum)
    
    def getX(self):
        return self.servos['x'].orientacion
    def getY(self):
        return self.servos['y'].orientacion
        
       
