from cv2 import *
import cv2
import ReconocedorFacial as Reconocedor
import ValidadorDesplazamiento 
import Calculador 

def main():
    vc = VideoCapture(0)
    punto90 = (320,240)
    validadorDesp = ValidadorDesplazamiento.ValidadorDesplazamiento(punto90)   
    namedWindow("webcam")
    while True:
        va, imagen = vc.read()
        carasEncontradas = Reconocedor.detectarCara(imagen)
        
        for (x, y, w, h) in carasEncontradas:#se dibuja un rectangulo en la cara y se muestra
            cv2.rectangle(imagen, (x, y), (x+w, y+h), (0, 255, 0), 5)#(foto, ubicacion, (largo alto), )
            cv2.circle(imagen,punto90,1, (0, 255, 0), 5)
            dCamaraCabeza = 40
            dCabezaMano = 100
            #if validadorDesp.validarDesplazamiento((x,y)):
            puntoDetectado = (x,y)
            hipotenusa = Calculador.calcularDistancia(dCamaraCabeza,dCabezaMano)
            print hipotenusa
            print(Calculador.calcularAnguloC(dCabezaMano,hipotenusa))

        imshow("WebCam", imagen)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
main()