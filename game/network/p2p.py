#coding: utf-8

from .core.hlpct.package_coding import *

from .core.apresentation import *
from .core.hear import *
from .core.pinging import *

from .core.threads.hearing_thread import *
from .core.threads.apresentation_thread import *
from .core.threads.ping_thread import *

class P2P:
    def __init__(self, myId):
        self.myId = myId
        self.inRoom = False
        self.idRoom = None
        self._fakeID = None
        self.pingList = {}
        self.peersList = self._p2pInitialize()
        self._autorizationFlag = True

        #pacotes aguardando leitura
        #(addressReceived, commandID, flag, message)
        self._packagesQueue = []

        #Threads
        listen = simpleThread(self._hearing)
        ping = simpleThread(self._pingSend)
        offline = simpleThread(self._offlineDetection)

        #Inicialização das Threads
        listen.start()
        ping.start()
        offline.start()



    def _p2pInitialize(self):
        return apresentation(self.myId, self.inRoom, self.idRoom)

    def _hearing(self):
        conversationList = []
        responseSocket = UDP(5554)
        while 1:
            try:
                request, addressReceived = responseSocket.listening()

                commandID, flag, message = packageDisassembler(request)

                if commandID == b'00001':
                    t = apresentationThread(self._p2pInitializeResponse, addressReceived, message)
                    conversationList.append(t)
                    t.start()

                elif commandID == b'00010':
                    t = pingReadThread(self._pingRead, addressReceived, message)
                    conversationList.append(t)
                    t.start()

                elif commandID == b'00100':
                    '''
                    Recebeu uma solicitação para entrar na sala
                    '''
                    self._packagesQueue.append((addressReceived, commandID, flag))

                elif commandID == b'00110':
                    '''
                    aceito na sala
                    '''
                    if int(flag) == 0:
                        self.inRoom = True
                    else:
                        self.idRoom = self._fakeID
                        self._fakeID = None
                        #fase de warmup

            except:
                print('Ocorreu um erro fatal, reabra o seu jogo!')
                responseSocket.close()

    def _p2pInitializeResponse(self, addressReceived, newPeerID):
        apresentationResponse(self.peersList, addressReceived, newPeerID, self._autorizationFlag)

    def _pingRead(self, addressReceived, message):
        peersPing(addressReceived, message, self.peersList, self.pingList, self._autorizationFlag)

    def _pingSend(self):
        while 1:
            time.sleep(0.5)
            self.peersList[0][2] = self.inRoom
            self.peersList[0][3] = self.idRoom
            pingPeers(self.myId, self.inRoom, self.idRoom, self.peersList)

    def _offlineDetection(self):
        while 1:
            time.sleep(2.5)
            removeOfflinePeers(self.peersList, self.pingList, self._autorizationFlag)

    def playing(self, idRoom:int):
        self.inRoom = True
        self.idRoom = idRoom

    def leaving(self):
        self.inRoom = False
        self.idRoom = None

if __name__ == '__main__':
    s = P2P('debug')
