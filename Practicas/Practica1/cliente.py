#!/usr/bin/env python3
import socket
import os

buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientServer:
    host = input('Ingrese el host: ')
    port = int(input('Ingrese el puerto: '))

    TCPClientServer.connect((host, port))

    dif = input('Eliga la dificultad:\n1.Principiante\n2.Avanzado\n')

    TCPClientServer.sendall(str.encode(dif))

    tablero = TCPClientServer.recv(buffer_size)
    print(tablero.decode('utf-8'))

    while True:
        casilla = input('\nEliga una casilla(d4, e5, etc): ')
        TCPClientServer.sendall(str.encode(casilla))
        os.system('clear')
        data = TCPClientServer.recv(buffer_size).decode('utf-8')

        if len(data) > 420:
            print(data[:420])
            resultado = 'WIN' if data[420] == 'W' else 'LOSE'
            tiempo = data[421:]
            break

        print(data)

    print(f'Game over: You {resultado} \nTime: {tiempo} s.')
