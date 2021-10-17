#!/usr/bin/env python3

"""
    Aplicaciones para Comunicaciones de Red
    Practica 2
    Elaborado por: Pedro Eduardo Garcia Leyva
    Grupo: 3CM17
"""
import socket
import time


class Client():
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 65432
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.HOST, self.PORT))

        message = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')
        print(message)

        # Despues de que todos los jugadores se conecten

        board = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')
        print(board)

        while True:
            res = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')

            if len(res) > 420:
                tablero = res[:420]
                res_aux = res[420:]
            elif len(res) < 420:
                res_aux = res
                tablero = None
            else:
                tablero = res
                res_aux = None

            if tablero:
                print(tablero)

            if res_aux and res_aux == 'True':
                casilla = input('\nEliga una casilla(d4, e5, etc): ')
                self.socket.sendall(str.encode(casilla))
            elif res_aux and (res_aux == 'Win' or res_aux == 'Lose'):
                print(f'Game over: You {res_aux}')
                break
            elif res_aux:
                print(f'Esperando a que {res_aux} seleccione una casilla...')

        self.socket.close()


if __name__ == '__main__':
    client = Client()
    client.connect()
