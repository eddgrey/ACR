import os
import socket
import threading

users = {
    "user_01": {
        "password": 'pass_01'
    },
    "user_02": {
        "password": 'pass_02'
    }
}


class FTP_Commands():

    def __init__(self):
        self.folders = os.listdir('./file_system/')
        self.state = 'LOGOUT'
        self.user = None
        self.FTP_commands = {
            "USER": {
                "func": self.USER,
                "success": "331 User name ok, need password <CRLF>",
                "error": "332 Need account for login. <CRLF>",
            },
            "PASS": {
                "func": self.PASS,
                "success": "230 User logged in, proceed.<CRLF>",
                "error": "530 Not logged in. <CRLF>",
            },
            "PORT": {
                "func": self.PORT,
                "success": "125 Data connection already open; transfer starting. <CRLF>",
                "error": "501 Syntax error in parameters or arguments. <CRLF>",
            },
            "RETR": {
                "func": self.RETR,
                "success": "125 Data connection already open; transfer starting. <CRLF>",
                "error": "501 Syntax error in parameters or arguments. <CRLF>",
            },
            "STOR": {
                "func": self.STOR,
                "success": "150 File status okay; about to open data connection <CRLF>",
                "error": "User dont found <CRLF>",
            },
            "QUIT": {
                "func": self.QUIT,
                "success": "221 Service closing control connection. <CRLF>",
                "error": "500 Syntax error, command unrecognized. <CRLF>",
            }
        }

    def handle_commmand(self, request):

        if request:
            command, *data = request.split(" ")

        if command in self.FTP_commands.keys():
            if command == "QUIT":
                res = self.FTP_commands[command]['func'](data)
                return res

            if self.syntax_error(data):
                return "501 Syntax error in parameters or arguments. <CRLF>"

            res = self.FTP_commands[command]['func'](self.data)
            return res

        return "502 Command not implemented. <CRLF>"

    def syntax_error(self, data):

        try:
            sp, data, crlf = data

            if sp != "<SP>" or crlf != "<CRLF>":
                return True

            self.data = data

        except Exception as e:
            print(e)
            return True

    def USER(self, user):
        if user in self.folders:
            self.user_directory = os.path.join("./file_system", user)
            self.user = user
            return self.FTP_commands["USER"]["success"]

        return self.FTP_commands["USER"]["error"]

    def PASS(self, password):
        """ Since password
            information is quite sensitive, it is desirable in general
            to "mask" it or suppress typeout. """

        if not self.user:
            return "332 Need account for login. <CRLF>"

        passw = users.get(self.user)["password"]

        if password == passw:
            self.state = 'LOGIN'
            return self.FTP_commands["PASS"]["success"]

        return self.FTP_commands["PASS"]["error"]

    def STOR(self, filename):
        if self.state == "LOGOUT":
            return "530 Not logged in. <CRLF>"

        self.pending_file = filename
        self.state = "STOR"

        return self.FTP_commands["RETR"]["success"]

    def RETR(self, filename):

        if self.state == "LOGOUT":
            return "530 Not logged in. <CRLF>"

        try:
            with open(f"{self.user_directory}/{filename}", "rb") as file:
                self.pending_file = filename
                self.state = "RETR"
                return self.FTP_commands["RETR"]["success"]
        except Exception as e:
            print(e)
            return "550 Requested action not taken.\nFile unavailable (e.g., file not found, no access)."

    def PORT(self, data_port):

        if self.state == "LOGOUT":
            return "530 Not logged in. <CRLF>"

        thread = threading.Thread(
            name='user-DTP', target=self.pending, args=(data_port, self.state))
        thread.start()

        return self.FTP_commands["PORT"]["success"]

    def QUIT(self, data):
        try:
            if data[0] == "<CRLF>":
                return self.FTP_commands["QUIT"]["success"]
            else:
                return self.FTP_commands["QUIT"]["success"]
        except:
            return self.FTP_commands["QUIT"]["error"]

    def pending(self, data_port, pending_command):
        print(f'Pending file: {self.pending_file}')

        try:
            data_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_conn.connect(("127.0.0.1", int(data_port)))

        except Exception as e:
            print(e)

        path = f"{self.user_directory}/{self.pending_file}"

        if pending_command == "RETR":
            with open(path, "rb") as file:
                while True:
                    bytes_read = file.read(1024)
                    if not bytes_read:
                        break
                    data_conn.sendall(bytes_read)

        elif pending_command == "STOR":
            with open(path, "wb") as f:
                while True:
                    bytes_read = data_conn.recv(1024)
                    if not bytes_read:
                        break
                    f.write(bytes_read)

        data_conn.close()
        print("226 Closing data connection.")
