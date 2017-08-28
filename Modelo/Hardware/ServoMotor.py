

class ServoMotor(object):
    '''
    classdocs
    '''


    def __init__(self, grado):
        self.orientacion = grado
    
    def girar(self, grado):
        self.orientacion = grado        