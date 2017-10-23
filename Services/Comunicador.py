import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep
import random

servoBase = 35
servoLateral = 33
GPIO.setmode(GPIO.BOARD)   #Ponemos la Raspberry en modo BOARD
GPIO.setup(servoBase,GPIO.OUT)    #Ponemos el pin 21 como salida
GPIO.setup(servoLateral,GPIO.OUT)    #Ponemos el pin 21 como salida
pulsoBase = GPIO.PWM(servoBase,50)        #Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
pulsoBase.start(0)               #Enviamos un pulso del 7.5% para centrar el servo
pulsoLateral = GPIO.PWM(servoLateral,50)        #Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
pulsoLateral.start(0)
delay = 0.4
predeBase = 0
predeLate = 0

def convertirAngulo(angulo):
    
    resultado = (3+angulo/180.0*9)
    return resultado

def enviarOrientacion(h,v):

        pBase = convertirAngulo(h)
        pLateral = convertirAngulo(v)

        pulsoBase.ChangeDutyCycle(pBase)
        pulsoBase.ChangeDutyCycle(pLateral)  
        time.sleep(0.4)    
     
       
        
if __name__ == '__main__':
    
     try:                 
        while True:
            h = random.randint(0,180)
            v = random.randint(0,180)
            enviarOrientacion(h,v)
     
     except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
        pulsoBase.stop()                      #Detenemos el servo 
        pulsoLateral.stop()                      
        GPIO.cleanup()  
