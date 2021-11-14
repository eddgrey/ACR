"""
    Aplicaciones para Comunicaciones de Red
    Practica4
    Elaborado por: Pedro Eduardo Garcia Leyva
    Grupo: 3CM17
"""


import socket

HOST = "127.0.0.1"
PORT = 1161
BUFFER_SIZE = 1024
request_ID = 0


def make_request(request):

    version, community, PDU_type, *var_bind = request.split(' ')

    if PDU_type == 'set-request':
        OID, value = var_bind
        SNMP_PDU = [PDU_type, str(request_ID), '0', '0', OID, value]
    else:
        OID = var_bind[0]
        SNMP_PDU = [PDU_type, str(request_ID), '0', '0', OID]

    request = [version, community] + SNMP_PDU

    return ' '.join(request)


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as gestor:

    request = input('snmp ')

    data_to_send = make_request(request)
    gestor.sendto(str.encode(data_to_send), (HOST, PORT))

    response, address = gestor.recvfrom(BUFFER_SIZE)
    print(response.decode())

    request_ID += 1
