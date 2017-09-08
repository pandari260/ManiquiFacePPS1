import math

px = 10
cm = 2


def calcularDistanciaCM(pixeles):
    return (pixeles*cm)/px
 
def calcularDistanciaLados(ladoA,ladoB):
    powLadoA = math.pow(ladoA, 2)
    powLadoB = math.pow(ladoB,2)
    return float(math.sqrt(powLadoA + powLadoB))

def calcularAngulo(ladoOpuesto,hipotenusa):
    division = ladoOpuesto/hipotenusa
    arcoSeno = math.acos(division)
    return int((arcoSeno*180)/math.pi)

def CalcularDesplazamiento(pixelesObjetoCalibracion,distanciaCabezaObjetoDetectado):
    desplazamiento =  calcularDistanciaCM(pixelesObjetoCalibracion)
    hipotenusa = calcularDistanciaLados(desplazamiento,distanciaCabezaObjetoDetectado)
    return calcularAngulo(distanciaCabezaObjetoDetectado,hipotenusa)
