#coding: utf-8

def packageAssembler(operationID:bin, flag:bool, message:bin):
    '''
    operationID tranlate table:
        00001 - apresentação para rede
        00010 - ping
        00011 - resposta da apresentação
        00100 - solicitação para entrar numa sala

    flag use cases:
        ...
    '''
    if flag:
        flagPck = b'1'
    else:
        flagPck = b'0'

    if operationID == b'00001':
        return b'00001' + flagPck + message
    elif operationID == b'00010':
        return b'00010' + flagPck + message
    elif operationID == b'00011':
        return b'00011' + flagPck + message
    elif operationID == b'00100':
        return b'00100' + flagPck + message
    elif operationID == b'00110':
        return b'00110' + flagPck + message



def packageDisassembler(package:bin):
    '''
    package[:5] == operationID
    package[5:6] == flag
    package[6:] == message
    '''
    return package[:5], package[5:6], package[6:]
