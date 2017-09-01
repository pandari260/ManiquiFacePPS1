import math

def calcularDistanciaPuntos(puntoA,puntoB):
    dx = puntoA[0] - puntoB[0]
    dy = puntoA[1] - puntoB[1]
    return math.sqrt(math.pow(dx, 2) + math.pow(dy,2))

def calcularDistanciaCM(pxTotal,cmTotal,pxIni):
    return (pxIni*cmTotal)/pxTotal
 
def calcularDistanciaLados(ladoA,ladoB):
    powLadoA = math.pow(ladoA, 2)
    powLadoB = math.pow(ladoB,2)
    return float(math.sqrt(powLadoA + powLadoB))

def calcularAngulo(ladoOpuesto,hipotenusa):
    division = ladoOpuesto/hipotenusa
    arcoSeno = math.acos(division)
    return int((arcoSeno*180)/math.pi)
