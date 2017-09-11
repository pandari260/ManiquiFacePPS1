import math

pxAmplitud = 640
cmPropInver = 100.0
pxPropInver = 50.0



def calcularDesplazamiento1(pixeles, cm):
    return (pixeles*cm)/pxAmplitud
 
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
    

def CalcularDesplazamiento(pixelesObjetoCalibracion,distanciaCabezaObjetoDetectado):
    desplazamiento =  calcularDesplazamiento1(pixelesObjetoCalibracion, distanciaCabezaObjetoDetectado )
    hipotenusa = calcularHipotenusa(desplazamiento,distanciaCabezaObjetoDetectado)
    return calcularAngulo(distanciaCabezaObjetoDetectado,hipotenusa)
