"""
    Aplicaciones para Comunicaciones de Red
    Problema 2
    Elaborado por: Pedro Eduardo Garcia Leyva
    Grupo: 3CM17
"""
import socket


class Client():
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 8000
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.HOST, self.PORT))

        while True:
            archivo = input('Nombre del archivo: ')
            self.socket.sendall(str.encode(archivo))

            if not archivo:
                self.socket.close()
                break

            response = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')
            print(response)

            server = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')
            print(server)


cliente = Client()
cliente.connect()
