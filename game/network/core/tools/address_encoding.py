#coding: utf-8

import struct

def ipToBin(ip:str):
    '''
    converte um ip na sequencia binaria
    '''
    parts = ip.split('.')
    ip = struct.pack(
        'BBBB',
        int(parts[0]),
        int(parts[1]),
        int(parts[2]),
        int(parts[3])
    )
    return ip

def binToIp(binIp:bin):
    '''
    converte do ip binario para uma string
    '''
    ipSegmentsRaw = struct.unpack(
        'BBBB',
        binIp
    )
    ipSegments = []
    for i in range(4):
        ipSegments.append(str(ipSegmentsRaw[i]))
    ip = '.'.join(ipSegments)
    return ip

def idToBin(id:str):
    translate = b''
    for i in range(10):
        try:
            translate += struct.pack('B', ord(id[i]))
        except:
            translate += struct.pack('B', 0)
    return translate

def binToId(id:bin):
    translate = ''
    for b in id:
        if b != 0:
            translate += chr(b)
    return translate
