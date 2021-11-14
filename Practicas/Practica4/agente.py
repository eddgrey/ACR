import socket
import threading

HOST = '127.0.0.1'
PORT = 1161
BUFFER_SIZE = 1024

request_ID = 0

Error_Status = {
    0: 'noError',
    1: 'tooBig',
    2: 'noSuchName',
    3: 'badValue',
    4: 'readOnly',
    5: 'genErr'
}

"""
2 - Integer32
4 - OCTET STRING
6 - OBJECT IDENTIFIER
67 - TimeTicks
"""


def load_data():
    mib = {}
    communities = {}

    with open('./public.snmprec', 'r') as file:
        lines = file.readlines()
        for line in lines:
            OID, tag, value = line.split('|')
            mib[OID] = {'tag': tag, 'value': value.strip()}

    with open('./snmpd.conf', 'r') as file:
        lines = file.readlines()
        for line in lines:
            try:
                data, community = line.split(' ')
                index = data.find('community')

                if index == -1:
                    return 'Error '

                communities[community.strip()] = {'permissions': data[:index]}
            except Exception as e:
                print('Error: ', e)

    return communities, mib


def handle_request(request, communities, mib):

    try:
        version, comm, *SNMP_PDU = request.split(' ')
        PDU_type, request_ID, err_status, err_index, *var_binds = SNMP_PDU

    except Exception as e:
        return 'Error: genErr'

    if PDU_type == 'set-request':
        OID, value = var_binds
    else:
        OID = var_binds[0]

    community = communities.get(comm)
    object = mib.get(OID)

    if version != 'v1':
        return 'Error: version does not match'

    if not community:
        return 'Error: community not found'

    if not object:
        return 'Error Status: noSuchName'

    if PDU_type == 'get-request' and 'r' in community['permissions']:
        return OID + ' = ' + object['value']

    elif PDU_type == 'set-request':

        if 'w' in community['permissions']:
            type = mib[OID]['tag']

            if (type == '2' or type == '67') and not value.isdigit():
                return 'Error: badValue'

            elif (type == '6'):
                oid = value.split('.')
                if len(oid) < 5:
                    return 'Error: badValue'
                for n in oid:
                    if not n.isdigit():
                        return 'Error: badValue'

            mib[OID]['value'] = value

            with open('./public.snmprec', 'w') as file:
                for OID, values in mib.items():
                    data = '|'.join([OID] + list(values.values())) + '\n'
                    file.write(data)

            return 'Successful operation'

        return 'Error: readOnly'

    else:
        return 'Error: genErr'


def deamon_SNMPD():

    print('Demonio SNMPD se esta ejecutando...')
    communities, mib = load_data()

    deamon_snmpd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    deamon_snmpd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    deamon_snmpd.bind((HOST, PORT))

    while (True):
        request, address = deamon_snmpd.recvfrom(BUFFER_SIZE)
        response = handle_request(request.decode(), communities, mib)
        deamon_snmpd.sendto(str.encode(response), address)


deamon = threading.Thread(name='deamon_SNMPD', target=deamon_SNMPD)
deamon.setDaemon(True)
deamon.start()

input('Press enter to exit')
