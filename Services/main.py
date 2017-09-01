from cv2 import *
import cv2
import ReconocedorFacial as Reconocedor
import ValidadorDesplazamiento 
import MedidorDistancia as Medidor

def main():
    vc = VideoCapture(0)
    validadorDesp = ValidadorDesplazamiento.ValidadorDesplazamiento()   
    namedWindow("webcam")
    while True:
        va, imagen = vc.read()
        carasEncontradas = Reconocedor.detectarCara(imagen)
        
        for (x, y, w, h) in carasEncontradas:#se dibuja un rectangulo en la cara y se muestra
            cv2.rectangle(imagen, (x, y), (x+w, y+h), (0, 255, 0), 5)#(foto, ubicacion, (largo alto), )
            cv2.circle(imagen,(320,240),1, (0, 255, 0), 5)
            if validadorDesp.validarDesplazamiento((x,y)):
                puntoCentro = (320,240)
                puntoDetectado = (x,y)
                print (Medidor.calcularDistancia(puntoCentro,puntoDetectado))  

        imshow("WebCam", imagen)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
main()