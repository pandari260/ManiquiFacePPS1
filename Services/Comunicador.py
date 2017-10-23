import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep
import random


class Comunicador(object):

    def __init__(self, pinBase, pinLateral):
        self.servoBase = pinBase
        self.servoLateral = pinLateral
        GPIO.setmode(GPIO.BOARD)  # Ponemos la Raspberry en modo BOARD
        GPIO.setup(self.servoBase, GPIO.OUT)  # Ponemos el pin 21 como salida
        GPIO.setup(self.servoLateral, GPIO.OUT)  # Ponemos el pin 21 como salida
        self.pulsoBase = GPIO.PWM(self.servoBase, 50)  # Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
       # self.pulsoBase.start(0)  # Enviamos un pulso del 7.5% para centrar el servo
        self.pulsoLateral = GPIO.PWM(self.servoLateral, 50)  # Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
        #self.pulsoLateral.start(0)
        self.delay = 1
        self.predeBase = 0
        self.predeLate = 0

    def enviarOrientacion(self, h, v):
        if(h*v != 0):
            pBase = convertirAngulo(h)
            pLateral = convertirAngulo(v)
            print("valor de X "+str(pBase))
            print("valor de Y "+str(pLateral))
            self.pulsoBase.start(pBase)
            self.pulsoLateral.start(pLateral)
	    #self.pulsoBase.ChangeDutyCycle(pBase)
            #self.pulsoLateral.ChangeDutyCycle(pLateral)
            time.sleep(self.delay)
            



def convertirAngulo(angulo):

        resultado = (1./18.*(angulo))+2
        return resultado
     

