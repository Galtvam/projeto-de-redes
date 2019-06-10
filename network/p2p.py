#coding: utf-8

from core.hlpct.package_coding import *

from core.apresentation import *
from core.hear import *
from core.pinging import *

class P2P:
    def __init__(self, myId):
        self.myId = myId
        self.inRoom = False
        self.idRoom = None
        self.pingList = {}
        self.peersList = self._p2pInitialize()


        '''
        EM CONSTRUÇÃO
        '''
        self._p2pInitializeResponse()
        self._p2pInitialize()
        '''
        '''

    def _p2pInitialize(self):
        return apresentation(self.myId, self.inRoom, self.idRoom)

    def _hearing(self):
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
        pingPeers(self.myId, self.inRoom, self.idRoom, self.peersList)

    def _offlineDetection(self):
        removeOfflinePeers(self.peersList, self.pingList)

    def playing(self, idRoom:int):
        self.inRoom = True
        self.idRoom = idRoom

    def leaving(self):
        self.inRoom = False
        self.idRoom = None
