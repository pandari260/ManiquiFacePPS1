
class ValidadorDesplazamiento(object):
   
    def __init__(self):
        self.proporsion = 40
        self.ubiActual = (200,300) #Ver para obtener la posicion en la que esta la cabeza
        
    def validarDesplazamiento(self,direccion):
        if((direccion[0]>=(self.ubiActual[0]+self.proporsion)) or (direccion[0]<=(self.ubiActual[0]-self.proporsion))
        or (direccion[1]>=(self.ubiActual[1]+self.proporsion)) or (direccion[1]<=(self.ubiActual[1]-self.proporsion))):
            self.ubiActual = direccion
            return True
        else:
            return False
        
    
    def getX(self):
        return self.ubiActual[0]
    
    def getY(self):
        return self.ubiActual[1]
