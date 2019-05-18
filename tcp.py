import socket
import address_encoding

class TCP:
    '''
    instancia TCP com interface cliente e servidor
    '''
    def __init__(self, port:int):
        self._mainSocket = self._socketInitialize()
        self.setPort(port)

    def _socketInitialize(self):
        '''
        criou a instancia do Socket no modo TCP
        '''
        newSocket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        return newSocket

    def setPort(self, port:int):
        '''
        atribui uma porta ao Socket da instancia TCP
        '''
        self.portNumber = port
        self._mainSocket.bind(('',port))

    def stream(self, applicationPackage:bin, option:str='only', definedSocket=None):
        '''
        transmite o pacote da aplicação o destino contido no header

        $ option :- 'only' somente envia (padrao)
                    'adap' envia e entra no modo listening

                    'lock' recebe um socket ja conectado
                        $ definedSocket - corresponde a um socket ja conectado
        '''
        ipDst , portDst = address_encoding.extractIpAndPort(applicationPackage)
        addressDst = (ipDst, portDst)
        if option == 'lock':
            definedSocket.send(applicationPackage)
            definedSocket.close()
        else:
            self._mainSocket.connect(addressDst)
            self._mainSocket.send(applicationPackage)
            if option == 'adap':
                return self._adapStream()
            else:
                self._mainSocket.close()
                self.__init__(self.portNumber)

    def _adapStream(self):
        packageReceived = self._mainSocket.recv(80000)
        self._mainSocket.close()
        self.__init__(self.portNumber)
        return packageReceived

    def listening(self, option:str='only', applicationPackage:bin=None, numberOfConnections:int=1, bufferSize:int=80000):
        '''
        coloca o socket no modo de listen na porta padrão definida no socket

        $ option :- 'only'  somente escuta (padrao)
                    'adap'  escuta e retorna:
                             - socket conectado, ip, porta, pacote recebido
        '''
        self._mainSocket.listen(numberOfConnections)
        connectionSocket , addressSrc = self._mainSocket.accept()
        packageReceived = connectionSocket.recv(bufferSize)
        if option == 'adap':
            return connectionSocket, addressSrc[0], addressSrc[1] , packageReceived
        else:
            connectionSocket.close()