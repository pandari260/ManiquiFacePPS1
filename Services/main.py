from cv2 import *
import cv2
import ReconocedorFacial as Reconocedor
import ValidadorDesplazamiento 
import Calculador 
import ComunicadorSerial
import math

def main():
    vc = VideoCapture(0)
    punto90 = (320,240)
    extremoDerecho = (500,240)

    validadorDesp = ValidadorDesplazamiento.ValidadorDesplazamiento(punto90) 
    comunicador = ComunicadorSerial.ComunicadorSerial()
  
    namedWindow("webcam")
    while True:
        va, imagen = vc.read()
        carasEncontradas = Reconocedor.detectarCara(imagen)
        for (x, y, w, h) in carasEncontradas:#se dibuja un rectangulo en la cara y se muestra
            cv2.rectangle(imagen, (x, y), (x+w, y+h), (0, 255, 0), 5)#(foto, ubicacion, (largo alto), )
            cv2.circle(imagen,punto90,1, (0, 255, 0), 5)
            cv2.circle(imagen,extremoDerecho,1, (0, 255, 0), 5)
            
            if validadorDesp.validarDesplazamiento((x,y)):
                desplazamiento =  Calculador.calcularDistanciaCM(500,115,math.fabs(x-500))
                dCabezaMano = 100
                hipotenusa = Calculador.calcularDistanciaLados(desplazamiento,dCabezaMano)
                angulo = Calculador.calcularAngulo(dCabezaMano,hipotenusa)
                print "x "+str(angulo)
                comunicador.enviarDatos("x"+str(angulo))

        imshow("webcam", imagen)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
main()