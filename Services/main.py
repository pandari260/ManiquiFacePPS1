import  numpy
import cv2
from cv2 import *
from Modelo.Hardware.Camara import Camara
import Services.ReconocedorFacial as Reconocedor


def main():
    camara = Camara(0)
    camara.conectarCamara()
    namedWindow("webcam")
    while True:
        imagen = camara.tomarFoto()
        carasEncontradas = Reconocedor.detectarCara(imagen)
        
        for (x, y, w, h) in carasEncontradas:#se dibuja un rectangulo en la cara y se muestra
            cv2.rectangle(imagen, (x, y), (x+w, y+h), (0, 255, 0), 5)#(foto, ubicacion, (largo alto), )
            
        imshow("webcam", imagen)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
main()