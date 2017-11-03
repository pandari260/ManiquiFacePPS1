import math

pxAmplitud = 320
AmplitudPropInver = 60.0
pxPropInver = 40.0
distanciaPropInver = 100

def calcularDistancia(px):
    ret = (pxPropInver*distanciaPropInver)/px
    return ret

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



def calcularPosicionCabeza(puntoCentro, posicion, diametro ):
    amplitud = calcularAmplitud(calcularDistancia(diametro/2))
    
 
    x = calcularDesplazamiento(posicion[0], amplitud) - calcularDesplazamiento(puntoCentro[0], amplitud)
    y = calcularDesplazamiento(posicion[1], amplitud) - calcularDesplazamiento(puntoCentro[1], amplitud)
    return (x,y)

def calcularPuntoCalibracion(cabeza, distancia, puntoCentro):
    
    amplitud = calcularAmplitud(distancia)
    x = int(calcularEjeCalibracion(cabeza.posicion[0], amplitud, puntoCentro[0]))
    y = int(calcularEjeCalibracion(cabeza.posicion[1], amplitud, puntoCentro[1]))
    return (x,y)

def calcularAmplitud(d):
     return (d * AmplitudPropInver)/distanciaPropInver


    
def CalcularOrientacion(pixelesObjetoCalibracion,distanciaCabezaObjetoDetectado):
    amplitud = calcularAmplitud(distanciaCabezaObjetoDetectado)
    desplazamiento =  calcularDesplazamiento(pixelesObjetoCalibracion,  amplitud)
    hipotenusa = calcularHipotenusa(desplazamiento,distanciaCabezaObjetoDetectado)
    return calcularAngulo(distanciaCabezaObjetoDetectado,hipotenusa)
