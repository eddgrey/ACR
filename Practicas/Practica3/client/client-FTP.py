#!/usr/bin/env python3
"""
    Aplicaciones para Comunicaciones de Red
    Practica 3
    Elaborado por: Pedro Eduardo Garcia Leyva
    Grupo: 3CM17
"""

import socket
import threading


class Client():
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 2121
        self.PORT_DATA = 2120
        self.BUFFER_SIZE = 1024
        self.control_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def user_protocol_interpreter(self):
        """The user protocol interpreter initiates the control connection
        from its port U to the server-FTP process and is responsible for
        sending FTP commands and interpreting the replies received"""

        self.control_conn.connect((self.HOST, self.PORT))
        print(f"Client connect server {self.HOST} port {self.PORT}")

        while True:
            command = input('Client: ')
            self.control_conn.sendall(str.encode(command))
            res = self.control_conn.recv(self.BUFFER_SIZE).decode('utf-8')

            if not res:
                break

            print(f'Server: {res}')

            if res[:3] == '221':
                # QUIT command
                break

            if command[:4] in ["RETR", "STOR"] and res[0] == "1":
                comm, sp, filename, crlf = command.split(' ')
                thread = threading.Thread(
                    name='user-DTP', target=self.user_data_transfer_process, args=(filename, comm))
                thread.start()

        self.control_conn.close()

    def user_data_transfer_process(self, filename, command):
        """The data transfer process "listens" on the data port for a
         connection from a server-FTP process."""

        data_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        data_conn.bind((self.HOST, self.PORT_DATA))
        data_conn.listen(1)

        data_socket, client_addr = data_conn.accept()

        path = f'./file_system/{filename}'

        if command == "RETR":
            with open(path, "wb") as f:
                while True:
                    bytes_read = data_socket.recv(self.BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)

        elif command == "STOR":
            with open(path, "rb") as file:
                while True:
                    bytes_read = file.read(self.BUFFER_SIZE)
                    if not bytes_read:
                        break
                    data_socket.sendall(bytes_read)

        data_conn.close()


if __name__ == '__main__':
    client = Client()
    client.user_protocol_interpreter()
