import http.server
import socketserver
import threading
import socket
import http.client

list_servers = [
    {
        'Name': 'Server 1',
        'HOST': '127.0.0.1',
        'PORT': 8001,
    },
    {
        'Name': 'Server 2',
        'HOST': '127.0.0.1',
        'PORT': 8002,
    },
    {
        'Name': 'Server 3',
        'HOST': '127.0.0.1',
        'PORT': 8003,
    }
]


class BalanceadorDeCarga():
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = '127.0.0.1'
        self.PORT = 8000
        self.BUFFER_SIZE = 1024
        self.contador = 0
        self.SERVIDORES = list_servers
        self.clients = []

    def crear_servidores(self):
        for server in self.SERVIDORES:
            thread = threading.Thread(
                name=server['Name'], target=self.iniciar_servidor, args=(server['HOST'], server['PORT']))
            thread.start()

    def iniciar_servidor(self, host, port):
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer((host, port), handler) as httpd:
            print("Serving at port", port)
            httpd.serve_forever()

    def iniciar_servidor_central(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen()
        print('Esperando solicitudes...')

        self.aceptar_clientes()

    def aceptar_clientes(self):

        while True:
            client_socket, client_addr = self.socket.accept()
            name = f'Client-{len(self.clients)+1}'
            self.clients.append(name)
            thread = threading.Thread(
                name=name, target=self.recibir_solicitudes, args=(client_socket,))
            thread.start()

    def recibir_solicitudes(self, client_socket):

        while True:
            archivo = client_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            self.round_robin(archivo, client_socket)

    def round_robin(self, archivo, client_socket):

        server = self.SERVIDORES[self.contador]
        print(
            f"Al {server['Name']} se le asigno la solicitud del {threading.current_thread().name}")

        if self.contador + 1 > 2:
            self.contador = 0
        else:
            self.contador += 1

        host_http = f"{server['HOST']}:{server['PORT']}"

        conn = http.client.HTTPConnection(host_http)
        conn.request("GET", archivo)

        response = conn.getresponse()
        print(f"\n{server['Name']}: {response.status}, {response.reason}\n")

        while True:
            chunk = response.read(1024)

            if not chunk:
                break

            client_socket.sendall(chunk)

        client_socket.sendall(str.encode(f"Enviado desde el {server['Name']}"))


balanceador = BalanceadorDeCarga()
balanceador.crear_servidores()
balanceador.iniciar_servidor_central()
