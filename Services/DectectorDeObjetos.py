'''
Created on 15 oct. 2017

@author: Javi-PC
'''
from ReconocedorFacial import RastreadorFacial
from ReconocedorFacial import ReconocerdorFacial
from time import sleep
class DetectorDeObjetos(object):
    
    def __init__(self, hPath):
        self.haarPath = hPath
        self.rastreadorCara = None
        self.reconocedor = ReconocerdorFacial(hPath)
        self.seDebeUsarMeanshift = False
        self.seIdentificoBlob = False
        self.seEncontroCara = False
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        
    def detectar(self, imagen):
        if(not self.seDebeUsarMeanshift):
            print("se esta reconociendo")
            self.seEncontroCara,self.x,self.y,self.w,self.h = self.reconocedor.detectarCara(imagen)#bool si se encontro cara, posicion (x,y), ancho y alto
            self.seDebeUsarMeanshift = self.seEncontroCara
        else:
            print("se esta rastreando")
            if not self.seIdentificoBlob:
                self.rastreadorCara = RastreadorFacial.RastreadorFacial(imagen, (self.x, self.y, self.w, self.h))
                self.rastreadorCara.identificarBlob()
                self.seIdentificoBlob = True
            else:
                seEncontroCara, self.x,self.y,self.w,self.h = self.rastreadorCara.rastrear(imagen)   
                if(not seEncontroCara):
                    self.seDebeUsarMeanshift = False
                    self.seIdentificoBlob = False
                    self.x = 0
                    self.y = 0
                    self.w = 0
                    self.h = 0
                    
        
       
        return self.seEncontroCara, self.x,self.y,self.w,self.h
        