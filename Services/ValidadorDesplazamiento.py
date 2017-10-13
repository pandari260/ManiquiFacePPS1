import math
class ValidadorDesplazamiento(object):
   
    def __init__(self, ubicacion):
        self.proporsion = 10
        self.ubiActual = ubicacion
        #no tendria que haver un para la  y otro para la y?
        
    def validarDesplazamiento(self,direccion):
        if(math.fabs(direccion[0]-self.ubiActual[0]) >= self.proporsion 
           or math.fabs(direccion[1]-self.ubiActual[1]) >= self.proporsion):
            self.ubiActual = direccion
            return True
        else:
            return False
        
    
    def getX(self):
        return self.ubiActual[0]
    
    def getY(self):
        return self.ubiActual[1]
