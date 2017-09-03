from cv2 import *
import cv2
import ReconocedorFacial as Reconocedor
import ValidadorDesplazamiento 
import Calculador 
import math
from Modelo.Hardware.Cabeza import Cabeza
punto90 = (0,240)
color = (0,255,0)
grosorFigura = 5
distanciaCabezaObjetoDetectado = 100

def main():
    vc = VideoCapture(0)
    validadorDesp = ValidadorDesplazamiento.ValidadorDesplazamiento(punto90) 
    namedWindow("webcam")
    cabeza = Cabeza((520, 240))
    while True:
        va, imagen = vc.read()
        carasEncontradas = Reconocedor.detectarCara(imagen)
        for (x, y, w, h) in carasEncontradas:#se dibuja un rectangulo en la cara y se muestra
            cv2.rectangle(imagen, (x, y), (x+w, y+h), color, grosorFigura)#(foto, ubicacion, (largo alto), )
            cv2.circle(imagen,punto90,1, color, grosorFigura)
            cv2.circle(imagen,cabeza.getCalibracion(),1, color, grosorFigura)
            
            if validadorDesp.validarDesplazamiento((x,y)):
                angulo = Calculador.CalcularDesplazamiento(cabeza.getDistanciaCamara(), math.fabs(x-500),distanciaCabezaObjetoDetectado)
                cabeza.girar(angulo, 'x')

        imshow("webcam", imagen)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
main()