from cv2 import *
import cv2
import ReconocedorFacial as Reconocedor
from Modelo.Hardware import Camara


def main():
    camara = Camara.Camara(0)
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