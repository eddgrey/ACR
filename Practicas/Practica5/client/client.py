import logging
import grpc
import os
import operaciones_pb2
import operaciones_pb2_grpc

msg = """
================================================
        Sistema de Archivos Distribuidos        
================================================
"""


def Escribir():
    msg = 'Nombre del archivo: '
    while True:
        linea = input(msg)

        if linea:
            yield operaciones_pb2.CamposDeEntrada(entrada1=linea)
        else:
            break
        msg = ''


def Auth(stub, usuario, password):
    response = stub.Auth(operaciones_pb2.CamposDeEntrada(
        entrada1=usuario, entrada2=password))

    return response.salida1


def Read(stub, args):
    response = stub.Read(operaciones_pb2.CamposDeEntrada(entrada1=args[0]))

    for line in response:
        print(line.salida1)


def Write(stub, args):

    response = stub.Write(Escribir())
    print(response.salida1)


def Create(stub, args):
    response = stub.Create(operaciones_pb2.CamposDeEntrada(entrada1=args[0]))
    print(response.salida1)


def Rename(stub, args):
    response = stub.Rename(operaciones_pb2.CamposDeEntrada(
        entrada1=args[0], entrada2=args[1]))
    print(response.salida1)


def Remove(stub, args):
    response = stub.Remove(operaciones_pb2.CamposDeEntrada(entrada1=args[0]))
    print(response.salida1)


def Mkdir(stub, args):
    response = stub.Mkdir(operaciones_pb2.CamposDeEntrada(entrada1=args[0]))
    print(response.salida1)


def Rmdir(stub, args):
    response = stub.Rmdir(operaciones_pb2.CamposDeEntrada(entrada1=args[0]))
    print(response.salida1)


def Readdir(stub, args):
    response = stub.Readdir(operaciones_pb2.CamposDeEntrada(entrada1=''))

    for dir in response:
        print(dir.salida1)


commands = {
    'read': Read,
    'write': Write,
    'create': Create,
    'rename': Rename,
    'remove': Remove,
    'mkdir': Mkdir,
    'rmdir': Rmdir,
    'readdir': Readdir
}


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = operaciones_pb2_grpc.OperacionesStub(channel)
        print(msg)
        user = input('Nombre de usuario: ')
        password = input('Password: ')
        print()

        if Auth(stub, user, password) == 'Ok':
            while True:
                command, *args = input('>>> ').split(' ')
                func = commands.get(command.lower())

                if not func:
                    if command == 'exit':
                        break
                    elif len(command) > 0:
                        print('command not found')

                    continue

                try:
                    func(stub, args)
                except:
                    print('Error')
        else:
            print('user not found')


if __name__ == '__main__':
    logging.basicConfig()
    run()
