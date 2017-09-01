from cv2 import *
import cv2
import ReconocedorFacial as Reconocedor
import ValidadorDesplazamiento 
import Calculador 
import ComunicadorSerial

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
            
            if(x>=320):
                dCamaraCabeza =  Calculador.calcularDistanciaCM(180,40,x-320)
                dCabezaMano = 100
                #print "distancia: "+str(dCamaraCabeza)
                
                if validadorDesp.validarDesplazamiento((x,y)):

                    Calculador.calcularDistanciaPuntos(punto90,extremoDerecho)
                    hipotenusa = Calculador.calcularDistanciaLados(dCamaraCabeza,dCabezaMano)
                    angulo = Calculador.calcularAngulo(dCabezaMano,hipotenusa)
                    print "x"+str(angulo)
                    comunicador.enviarDatos("x"+str(angulo))

        imshow("WebCam", imagen)
       
        if waitKey(1) & 0xFF == ord('q'):
            break;
        
main()