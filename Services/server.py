
from wsgiref.simple_server import make_server
import Orientador
from random import randint

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
        grados = Orientador.reorientar(x, y, diametroCara, cabeza, puntoMedio)
      
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [str(grados[0]),str(grados[1])]
   


def start_server():
   
    httpd = make_server("", PORT, test_app)
    httpd.serve_forever()

if __name__ == '__main__':
    start_server(8080)