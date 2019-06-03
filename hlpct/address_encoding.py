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

def portToBin(port:int):
    '''
    converte uma porta numa sequencia de 2 bytes
    '''
    return struct.pack('H', port)

def binToPort(portBin:bin):
    '''
    converte uma sequencia de 2 bytes no numero da porta
    '''
    port = struct.unpack('H', portBin)
    return port[0]

def extractIpAndPort(applicationPackage:bin):
    '''
    extrai o IP e a Porta do pacote HLPCT retornando uma string
    e um inteiro respectivamente.
    '''
    ipDst = binToIp(applicationPackage[:4])
    portDst = binToPort(applicationPackage[4:6])
    return ipDst , portDst
