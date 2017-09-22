import math

pxAmplitud = 640
cmPropInver = 100.0
pxPropInver = 50.0



def calcularDesplazamiento(pixeles, cm):
    return (pixeles*cm)/pxAmplitud

def calcularEjeCalibracion(posicion, distancia, puntoMedio):
    return posicion*pxAmplitud/distancia +puntoMedio
 
def calcularHipotenusa(ladoA,ladoB):
    powLadoA = math.pow(ladoA, 2)
    powLadoB = math.pow(ladoB,2)
    return float(math.sqrt(powLadoA + powLadoB))

def calcularAngulo(ladoOpuesto,hipotenusa):
    division = ladoOpuesto/hipotenusa
    arcoSeno = math.acos(division)
    return int((arcoSeno*180)/math.pi)

def calcularDistancia(px):
    return (cmPropInver*pxPropInver)/px

def calcularPosicionCabeza(puntoCentro, posicion, diametro ):
    d = calcularDistancia(diametro/2)
    x = calcularDesplazamiento(posicion[0], d) - calcularDesplazamiento(puntoCentro[0], d)
    y = calcularDesplazamiento(posicion[1], d) - calcularDesplazamiento(puntoCentro[1], d)
    return (x,y)

def calcularPuntoCalibracion(cabeza, distancia, puntoCentro):
    
    x = int(calcularEjeCalibracion(cabeza.posicion[0], distancia, puntoCentro[0]))
    y = int(calcularEjeCalibracion(cabeza.posicion[1], distancia, puntoCentro[1]))
    return (x,y)
    
    
    

def CalcularOrientacion(pixelesObjetoCalibracion,distanciaCabezaObjetoDetectado):
    desplazamiento =  calcularDesplazamiento(pixelesObjetoCalibracion, distanciaCabezaObjetoDetectado )
    hipotenusa = calcularHipotenusa(desplazamiento,distanciaCabezaObjetoDetectado)
    return calcularAngulo(distanciaCabezaObjetoDetectado,hipotenusa)
