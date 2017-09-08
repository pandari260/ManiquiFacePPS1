from cv2 import *
import cv2
import ReconocedorFacial as Reconocedor
import ValidadorDesplazamiento 
import Calculador 
import math
import Modelo.Hardware.Cabeza as Cabeza
punto90 = (0,240)
color = (0,255,0)
grosorFigura = 5
distanciaCabezaObjetoDetectado = 100

def main():
    vc = VideoCapture(0)
    validadorDesp = ValidadorDesplazamiento.ValidadorDesplazamiento(punto90) 
    namedWindow("webcam")
    cabeza = Cabeza.Cabeza((520,240))
    cabeza.start()
    while True:
        va, imagen = vc.read()
        imagen = cv2.flip(imagen, 1)
        carasEncontradas = Reconocedor.detectarCara(imagen)
        for (x, y, w, h) in carasEncontradas:#se dibuja un rectangulo en la cara y se muestra
            cv2.rectangle(imagen, (x, y), (x+w, y+h), color, grosorFigura)#(foto, ubicacion, (largo alto), )
            cv2.circle(imagen,punto90,1, color, grosorFigura)
            cv2.circle(imagen,cabeza.getCalibracion(),1, color, grosorFigura)
            
            if validadorDesp.validarDesplazamiento((x,y)):
                direccionX = 1;
                direccionY = 1
                if(x < cabeza.getCalibracion()[0]):
                    direccionX = -1
                if(y < cabeza.getCalibracion()[1]):
                    direccionY = -1
                    
                    
                anguloHorizontal = Calculador.CalcularDesplazamiento(cabeza.getDistanciaHorizontal(), math.fabs(x-520),distanciaCabezaObjetoDetectado)
                anguloVertical = Calculador.CalcularDesplazamiento(cabeza.getDistanciaHorizontal(), math.fabs(y-240),distanciaCabezaObjetoDetectado)

                cabeza.setAngulo(anguloHorizontal*direccionX, 'x')
                cabeza.setAngulo(anguloVertical*direccionY, 'y')


        imshow("webcam", imagen)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
main()