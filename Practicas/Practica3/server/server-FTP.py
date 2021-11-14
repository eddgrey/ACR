#!/usr/bin/env python3

import threading
import socket
from commands import FTP_Commands


class Server():
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 2121
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def init_server(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen()
        print('Esperando solicitudes...')

        self.server_protocol_interpreter()

    def server_protocol_interpreter(self):
        """ The server protocol interpreter "listens" on Port L for a
         connection from a user-PI and establishes a control
         communication connection.  It receives standard FTP commands
         from the user-PI, sends replies, and governs the server-DTP. """

        while True:
            control_conn, client_addr = self.socket.accept()
            name = f'Client-{len(self.clients)+1}'
            self.clients.append(name)
            thread = threading.Thread(
                name=name, target=self.recieves_commands, args=(control_conn,))
            thread.start()

    def recieves_commands(self, control_conn):
        ftp_comm = FTP_Commands()

        while True:
            request = control_conn.recv(self.BUFFER_SIZE).decode('utf-8')

            if not request:
                break

            res = ftp_comm.handle_commmand(request)
            control_conn.sendall(str.encode(res))


if __name__ == '__main__':
    server = Server()
    server.init_server()
