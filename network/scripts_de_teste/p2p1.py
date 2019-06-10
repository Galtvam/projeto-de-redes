#coding: utf-8

from core.hlpct.package_coding import *

from core.apresentation import *
from core.hear import *

class P2P:
    def __init__(self):
        self.myId = 'servidor'
        self.inRoom = False
        self.idRoom = None
        self.peersList = [['192.168.24.102',self.myId, self.inRoom, self.idRoom]]

        print('Servidor de testes OK')
        while 1:
            self._hearing()
            print(self.peersList)

    def _p2pInitialize(self):
        return apresentation(self.myId, self.inRoom, self.idRoom)

    def _hearing(self):
        responseSocket = UDP(5554)
        request, addressReceived = responseSocket.listening()
        responseSocket.close()

        commandID, flag, newPeerID = packageDisassembler(request)

        if commandID == b'00001':
            self._p2pInitializeResponse(addressReceived, newPeerID)

        elif commandID == b'00010':
            self._ping()

    def _p2pInitializeResponse(self, addressReceived, newPeerID):
        self.peersList = apresentationResponse(self.peersList, addressReceived, newPeerID)

    def _ping(self, addressReceive):
        pass

    def playing(self, idRoom:int):
        self.inRoom = True
        self.idRoom = idRoom

    def leaving(self):
        self.inRoom = False
        self.idRoom = None


if __name__ == '__main__':
    s = P2P()
