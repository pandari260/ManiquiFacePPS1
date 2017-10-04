
from wsgiref.simple_server import make_server
from random import randint


FILE = 'index.html'

PORT = 8080

def test_app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = environ['wsgi.input'].read(request_body_size)
        except (TypeError, ValueError):
            request_body = "0"
        try:
            response_body = str(randint(1,20))
        except:
            response_body = "error"
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        print response_body
        return [response_body]
    else:
        response_body = open(FILE).read()
        status = '200 OK'
        headers = [('Content-type', 'text/html'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body]


def start_server(p1):
    httpd = make_server("", p1, test_app)
    httpd.serve_forever()


if __name__ == "__main__":
    start_server(PORT)
