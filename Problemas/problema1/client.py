
#!/usr/bin/env python3

"""
    Aplicaciones para Comunicaciones de Red
    Problema 1
    Elaborado por: Pedro Eduardo Garcia Leyva
    Grupo: 3CM17
"""

import socket
import speech_recognition as sr
import warnings

warnings.filterwarnings("ignore")


class Client():
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 65431
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def connect(self):
        self.socket.connect((self.HOST, self.PORT))

        message = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')
        print(message)

        # Despues de que todos los jugadores se conecten

        board = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')
        print(board)

        while True:
            res = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')
            datos = res.split(",")

            if len(datos) == 1:
                if res == 'True':
                    for i in range(3):
                        input('Di tu pregunta: ')
                        question = self.recognize_speech()
                        if question['transcription']:
                            break
                        if not question['success']:
                            break
                        print('Repitelo: ')
                    print(question['transcription'])
                    self.socket.sendall(str.encode(question['transcription']))

                else:
                    if len(res) > 30:
                        print(res)
                    else:
                        print(f'Esperando a que {res} mande una pregunta...')

            elif len(datos) >= 3:
                if datos[0] == 'Game over':
                    print(f'Game over')
                    print('El ganador es: ', datos[2])
                    print(f'Duracion de la partida: {datos[1]}')
                    break
                else:
                    print(f'\n============================')
                    print(f'Pregunta: {datos[0]}')
                    print(f'Respuesta: {datos[1]}')
                    print(f'=============================\n')
                    descartar = input('Personajes para descartar: ')
                    self.socket.sendall(str.encode(descartar))
                    print(f'\nPista: {datos[2]}\n')
            else:
                print(res)

        self.socket.close()

    def recognize_speech(self):

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        try:
            response["transcription"] = self.recognizer.recognize_google(
                audio, language='es-MX')
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["error"] = "Unable to recognize speech"

        return response


if __name__ == '__main__':
    client = Client()
    client.connect()
