limites = {'x' : [90,0,180], 'y' : [90,0,180]}

class Cabeza(object):
    
    def girar(self, grados, coordenada, eje):
        
        direccion = 1
        if(coordenada < self.getCalibracion()[eje]):
            direccion = direccion*-1
        inf = limites[eje][1]
        sup = limites[eje][2]
        grados = grados*direccion
        angulo = grados + limites[eje][0]
        
        if(angulo > sup):
            angulo = sup
        elif(angulo < inf):
            angulo = inf
    
        #self.comunicador.enviarDatos(eje+chr(angulo))
        print("la cabeza" + str(self.id) + " giro al angulo:" + str(angulo) + " en el eje: " + eje)
        return angulo

    def __init__(self, c, p, i):
        self.id = i
        self.puntoCalibracion = {'x' : c[0], 'y': c[1]}
        self.posicion = p
        self.girar(0, self.getCalibracion()['x'], 'x')
        self.girar(0, self.getCalibracion()['y'], 'y')
       
        
        
        
    def getDistanciaHorizontal(self):
        return self.distanciaHorizontal
    def getDistanciaVerical(self):
        return self.distanciaVertical
    def getCalibracion(self):
        return self.puntoCalibracion
   
        
       
