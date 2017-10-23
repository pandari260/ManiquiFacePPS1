import Calculador
import math
from threading import Thread
from threading import Event

def reorientar(x,y,diametroCara, cabeza, puntoMedio):
    if x*y*diametroCara > 0:
        distancia = Calculador.calcularDistancia(diametroCara/2)

        c = Calculador.calcularPuntoCalibracion(cabeza, distancia, puntoMedio)
        cabeza.puntoCalibracion['x'] = c[0] 
        cabeza.puntoCalibracion['y'] = c[1]
        anguloHorizontal = Calculador.CalcularOrientacion(math.fabs(x-cabeza.getCalibracion()['x']),distancia)
        anguloVertical = Calculador.CalcularOrientacion(math.fabs(y-cabeza.getCalibracion()['y']),distancia)
    
        gx = cabeza.girar(anguloHorizontal,x, 'x')
        gy = cabeza.girar(anguloVertical,y, 'y')
        return gx,gy
    return 0,0
        


       