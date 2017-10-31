'''
Created on 31 oct. 2017

@author: Javi-PC
'''
hardcodeada = []
hardcodeada.append({"x" : 80, "y": 160, "sleep" : 1})#los valores indican posiciones en la foto
hardcodeada.append({"x" : 240, "y": 160, "sleep" : 1})

class Secuencia(object):
    def __init__(self, s, pos):
        self. pasos = s
        self.posIncial = pos
        self.it = 0
        self.diametro = 50
        
    def getNext(self):
        ret = self.pasos[self.it]
        self.it = self.it + 1
        if(self.it == len(self.pasos)):
            self.it = 0
        return ret




       
        