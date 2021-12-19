#!/usr/bin/env python3
import threading
import socket
import time
from AdivinaQuien import AdivinaQuien


class Server():
    def __init__(self, num_clients):
        self.HOST = "127.0.0.1"
        self.PORT = 65431
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.NUM_CLIENTS = num_clients
        self.num_plays = self.NUM_CLIENTS
        self.game = AdivinaQuien()
        self.barrier_start_game = threading.Barrier(
            self.NUM_CLIENTS, action=self.start_game)
        self.update_board = threading.Barrier(
            self.NUM_CLIENTS, action=self.update_num_plays)
        self.check_animals = threading.Barrier(self.NUM_CLIENTS)
        self.finish_game = False
        self.winner = None
        self.clients = []

    def update_num_plays(self):
        self.num_plays += 1
        self.current_clue = self.game.get_clue()
        print(f'\nJugada numero {self.num_plays-2}')

    def start_game(self):
        self.time1 = time.time()
        self.current_clue = self.game.get_clue()

    def init_server(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen()
        print('Animal: ', self.game.character['nombre'])
        print('Esperando solicitudes...')

        self.accept_clients()

    def accept_clients(self):

        while True:
            client_socket, client_addr = self.socket.accept()
            name = f'Client-{len(self.clients)+1}'
            self.clients.append(name)
            board = AdivinaQuien(self.game.character)
            thread = threading.Thread(
                name=name, target=self.run_game, args=(client_socket, board))
            thread.start()

    def run_game(self, client_socket, board):
        num_clients = self.NUM_CLIENTS - self.barrier_start_game.n_waiting - 1
        message = f'Esperando {num_clients} jugadores para comenzar ...'

        client_socket.sendall(str.encode(
            f'Bienvenido a Adivina Quien\n{message}'))

        # Espera hasta que se conecten todos los clientes faltantes
        self.barrier_start_game.wait()
        msg = f'{board.board_str} \nPista: {self.current_clue}'
        client_socket.sendall(str.encode(msg))

        while True:

            current_thread = threading.current_thread()
            turn = self.num_plays % self.NUM_CLIENTS

            if self.clients[turn] == current_thread.name:

                print(f'Es turno de {self.clients[turn]}')
                client_socket.sendall(str.encode('True'))
                self.question = client_socket.recv(
                    self.BUFFER_SIZE).decode('utf-8')

                self.current_answer = self.game.answer_question(self.question)

            else:
                print(f'{current_thread.name} esta esperando su turno...')
                client_socket.sendall(str.encode(
                    self.clients[turn]))

            # Espera hasta que cada socket mande una respuesta a su cliente
            self.update_board.wait()

            res = f'{self.question}, {self.current_answer}, {self.current_clue}'
            client_socket.sendall(str.encode(res))

            animals_to_discard = client_socket.recv(
                self.BUFFER_SIZE).decode('utf-8')

            board.discard_animals(animals_to_discard)

            client_socket.sendall(str.encode(board.board_str))

            if board.estado != "Jugando" and not self.winner:
                self.winner = current_thread.name
                self.finish_game = True

            self.check_animals.wait()

            if self.finish_game:
                total_time = time.time() - self.time1
                client_socket.sendall(str.encode(
                    f'Game over, {total_time:.2f} seg, {self.winner}'))
                break

        self.socket.close()


if __name__ == '__main__':
    num_clients = int(input('Numero de jugadores: '))
    server = Server(num_clients)
    server.init_server()
