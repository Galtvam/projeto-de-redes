#coding: utf-8

from transport.tcp import TCP
from transport.udp import UDP

from p2p_tools import *

class P2P:
    def __init__(self,):
        self.peersList = self._p2pInitialize()

        '''
        EM CONSTRUÇÃO
        '''
        self._p2pInitializeResponse()
        self._p2pInitialize()
        '''
        '''

    def _p2pInitialize(self):
        socketInit = UDP(5555)
        messageInitialize = bytes("HelloWorld","utf-8")
        socketInit.stream(
            applicationPackage=messageInitialize,
            ipDst='224.0.0.1',
            portDst=5554
        )
        socketInit.close()
        socketReceiver = TCP(5555)
        address, port, peers = socketReceiver.listening(
            option='only',
            numberOfConnections=1,
            bufferSize=80000
        )
        if len(peers) < 4:
            peersList = []
            peersList.append(address)
            return peersList
        else:
            peersList = binToListOfIpsDecode(peers)
            peersList.append(address)
            return peersList

    def _p2pInitializeResponse(self):
        socketResponse = UDP(5554)
        request, addressReceiver = socketResponse.listening()
        if request == bytes("HelloWorld", 'utf-8'):
            if len(self.peersList) == 0:
                message = bytes('','utf-8')
            else:
                message = listOfPeersToBinConverte(self.pearList)
            socketResponse.close()
            socketDistributer = TCP()
            socketDistributer.stream(
                applicationPackage=message,
                ipDst=addressReceiver[0],
                portDst=5555,
                option='only',
                definedSocket=None
            )

            self.peersList.append(addressReceiver[0])
