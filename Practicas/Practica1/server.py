#!/usr/bin/env python3

import socket
import time
import sys
import os
from buscaminas import Buscaminas

HOST = "127.0.0.1"
PORT = 65432
buffer_size = 1024


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()

    print("El servidor TCP está disponible y en espera de solicitudes")

    Client_conn, Client_addr = TCPServerSocket.accept()

    with Client_conn:
        print("Conectado a", Client_addr)
        print('Bienvenido a Buscaminas')

        dificultad = Client_conn.recv(buffer_size).decode('utf-8')

        if dificultad == '1':
            tam, num_minas = (9, 10)
        elif dificultad == '2':
            tam, num_minas = (16, 40)
        else:
            sys.exit('Dificultad no valida')

        game = Buscaminas(tam, num_minas)

        tablero = game.imprimir_tablero()
        print(f'Se envio el tablero al cliente {Client_addr}\n')
        Client_conn.sendall(str.encode(tablero))

        t1 = None

        while True:
            # os.system('clear')

            print(f'Esperando respuesta...')

            casilla = Client_conn.recv(buffer_size).decode('utf-8')

            if not t1:
                t1 = time.time()

            casilla_valida = game.seleccionar_casilla(casilla)

            if casilla == 'd4':
                game.estado = 'Win'
            if casilla_valida:
                print(f'Se valido la casilla {casilla} ...')
            else:
                print(f'La casilla {casilla} no es valida')

            tablero = game.imprimir_tablero()
            print(f'Se actualizo el tablero...\n\n')

            Client_conn.sendall(str.encode(tablero))

            if game.estado in ['Win', 'Lose']:
                t2 = time.time()
                tiempo_total = str(round(t2 - t1, 2))
                Client_conn.sendall(str.encode(f'W{str(tiempo_total)}'))
                break

        print(f'Game over : You {game.estado}')
        print(f'Time: {tiempo_total}')
