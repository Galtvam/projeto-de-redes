#coding: utf-8

import socket

class UDP:
    '''
    instancia UDP com interface cliente e servidor
    '''
    def __init__(self, port:int=None):
        self._mainSocket = self._socketInitialize()
        self.setPort(port)

    def _socketInitialize(self):
        '''
        criou a instancia do Socket no modo UDP
        '''
        newSocket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )
        return newSocket

    def close(self):
        self._mainSocket.close()

    def reestart(self):
        self._mainSocket.close()
        self.__init__(port=self.portNumber)

    def setPort(self, port:int=None):
        '''
        atribui uma porta ao Socket da instancia UDP
        '''
        self.portNumber = port
        if port is not None:
            self._mainSocket.bind(('',port))

    def stream(self, applicationPackage:bin, ipDst:str, portDst:int):
        '''
        transmite o pacote da aplicação o destino contido no header
        '''
        addressDst = (ipDst, portDst)
        self._mainSocket.sendto(applicationPackage, addressDst)

    def listening(self):
        '''
        coloca o socket no modo de listen na porta padrão definida no socket
        '''
        packageReceived , addressSrc = self._mainSocket.recvfrom(80000)
        return packageReceived , addressSrc
