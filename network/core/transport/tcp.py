#coding: utf-8

import socket

class TCP:
    '''
    instancia TCP com interface cliente e servidor
    '''
    def __init__(self, port:int=None):
        '''
        caso uma porta não seja fornecida o socket ganhará uma aleatória
        '''
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

    def close(self):
        try:
            self._mainSocket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self._mainSocket.close()

    def reestart(self):
        try:
            self._mainSocket.shutdown(socket.SHUT_RDWR)
            self._mainSocket.close()
        except:
            self._mainSocket.close()
        self.__init__(port=self.portNumber)


    def setPort(self, port:int=None):
        '''
        atribui uma porta ao Socket da instancia TCP
        '''
        self.portNumber = port
        if port is not None:
            self._mainSocket.bind(('',port))

    def stream(self, applicationPackage:bin, ipDst:str, portDst:int, option:str='only', definedSocket=None):
        '''
        transmite o pacote da aplicação o destino contido no header

        $ option :- 'only' somente envia (padrao)
                    'adap' envia e entra no modo listening

                    'lock' recebe um socket ja conectado
                        $ definedSocket - corresponde a um socket ja conectado
        '''
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
                self.reestart()


    def _adapStream(self):
        packageReceived = self._mainSocket.recv(80000)
        self.reestart()
        return packageReceived

    def listening(self, option:str='only', numberOfConnections:int=1, bufferSize:int=80000):
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
            connectionSocket.shutdown(socket.SHUT_RDWR)
            connectionSocket.close()
            return addressSrc[0], addressSrc[1] , packageReceived
