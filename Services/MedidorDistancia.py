import math
   
def calcularDistancia(puntoA,puntoB):
    dx = puntoA[0] - puntoB[0]
    dy = puntoA[1] - puntoB[1]
    return math.sqrt(math.pow(dx, 2) + math.pow(dy,2))
    
  
        
       
