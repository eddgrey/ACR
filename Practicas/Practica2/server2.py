#!/usr/bin/env python3
import time
import threading
import socket
from buscaminas import Buscaminas


class Server():
    def __init__(self, num_clients):
        self.HOST = "127.0.0.1"
        self.PORT = 65432
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.NUM_CLIENTS = num_clients
        self.num_plays = self.NUM_CLIENTS
        self.game = Buscaminas(9, 10)

        self.barrier_start_game = threading.Barrier(self.NUM_CLIENTS)
        self.update_board = threading.Barrier(self.NUM_CLIENTS, action=self.update_num_plays)
        self.clients = []

    def update_num_plays(self):
        self.num_plays += 1
        print(f'\nJugada numero {self.num_plays-2}')

    def init_server(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen()
        print('Esperando solicitudes...')

        self.accept_clients()

    def accept_clients(self):

        while True:
            client_socket, client_addr = self.socket.accept()
            name = f'Client-{len(self.clients)+1}'
            self.clients.append(name)
            thread = threading.Thread(name=name, target=self.run_game, args=(client_socket,))
            thread.start()

    def run_game(self, client_socket):
        num_clients = self.NUM_CLIENTS - self.barrier_start_game.n_waiting - 1
        message = f'Esperando {num_clients} jugadores para comenzar ...'

        client_socket.sendall(str.encode(f'Bienvenido a Buscaminas\n{message}'))

        # Espera hasta que se conecten todos los clientes faltantes
        self.barrier_start_game.wait()

        client_socket.sendall(str.encode(self.game.board_str))

        while True:

            current_thread = threading.current_thread()
            turn = self.num_plays % self.NUM_CLIENTS

            if self.clients[turn] == current_thread.name:
                # Seccion critica
                print(f'Es turno de {self.clients[turn]}')
                client_socket.sendall(str.encode('True'))
                casilla = client_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                self.game.seleccionar_casilla(casilla)

            else:
                print(f'{current_thread.name} esta esperando su turno...')
                client_socket.sendall(str.encode(self.clients[turn]))

            # Espera hasta que cada socket mande una respuesta a su cliente
            self.update_board.wait()

            client_socket.sendall(str.encode(self.game.board_str))

            if self.game.estado != "Jugando":
                client_socket.sendall(str.encode(self.game.estado))
                break

        self.socket.close()


if __name__ == '__main__':
    num_clients = int(input('Numero de jugadores: '))
    server = Server(num_clients)
    server.init_server()
