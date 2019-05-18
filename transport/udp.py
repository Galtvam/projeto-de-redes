import socket
import address_encoding

class UDP:
    '''
    instancia UDP com interface cliente e servidor
    '''
    def __init__(self, port:int):
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
        return newtSocket

    def setPort(self, port:int):
        '''
        atribui uma porta ao Socket da instancia UDP
        '''
        self.portNumber = port
        self._mainSocket.bind(('',port))

    def stream(self, applicationPackage:bin):
        '''
        transmite o pacote da aplicação o destino contido no header
        '''
        ipDst , portDst = address_encoding.extractIpAndPort(applicationPackage)
        addressDst = (ipDst, portDst)
        self._mainSocket.sendto(applicationPackage, addressDst)

    def listening(self):
        '''
        coloca o socket no modo de listen na porta padrão definida no socket
        '''
        packageReceived , addressSrc = self._mainSocket.recvfrom(80000)
        return packageReceived , addressSrc
