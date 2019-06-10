#coding: utf-8

from core.hlpct.package_coding import *

from core.apresentation import *
from core.hear import *
from core.pinging import *

from core.threads.hearing_thread import *

class P2P:
    def __init__(self, myId):
        self.myId = myId
        self.inRoom = False
        self.idRoom = None
        self.pingList = {}
        self.peersList = self._p2pInitialize()

        listen = simpleThread(self._hearing)
        ping = simpleThread(self._pingSend)
        offline = simpleThread(self._offlineDetection)

        listen.start()
        ping.start()
        offline.start()



    def _p2pInitialize(self):
        return apresentation(self.myId, self.inRoom, self.idRoom)

    def _hearing(self):
        while 1:
            responseSocket = UDP(5554)
            request, addressReceived = responseSocket.listening()
            responseSocket.close()

            commandID, flag, message = packageDisassembler(request)

            if commandID == b'00001':
                self._p2pInitializeResponse(addressReceived, message)

            elif commandID == b'00010':
                self._pingRead(addressReceived, message)

    def _p2pInitializeResponse(self, addressReceived, newPeerID):
        apresentationResponse(self.peersList, addressReceived, newPeerID)

    def _pingRead(self, addressReceived, message):
        peersPing(addressReceived, message, self.peersList, self.pingList)

    def _pingSend(self):
        while 1:
            time.sleep(0.5)
            pingPeers(self.myId, self.inRoom, self.idRoom, self.peersList)

    def _offlineDetection(self):
        while 1:
            time.sleep(2.5)
            removeOfflinePeers(self.peersList, self.pingList)

    def playing(self, idRoom:int):
        self.inRoom = True
        self.idRoom = idRoom

    def leaving(self):
        self.inRoom = False
        self.idRoom = None

if __name__ == '__main__':
    s = P2P('player1')
