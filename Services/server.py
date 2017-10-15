
from wsgiref.simple_server import make_server
import Orientador
from random import randint
from Services import Calculador
from Services.Calculador import calcularPosicionCabeza

FILE = 'index.html'

PORT = 8080
cabeza = None
punto = None
diametro = None
puntoMedio = None


def test_app(environ, start_response):
    
    if environ['REQUEST_METHOD'] == 'POST':
       
        print(diametro.value)
        diametroCara = diametro.value

        x = punto[0]
        y = punto[1]
        posicionLateral, posicionVertical = calcularPosicionCabeza((160,120)(x,y),diametroCara)#estos valores te dicen la pocicion de la cara con respsto al punto medio (320,240)
        distanciaDeLaCara = Calculador.calcularDistancia(diametroCara/2)#este valor te dice que tan lejos esta la cara detectada
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        #return [str(grados[0]),str(grados[1])]
   


def start_server():
   
    httpd = make_server("", PORT, test_app)
    httpd.serve_forever()

if __name__ == '__main__':
    start_server(8080)