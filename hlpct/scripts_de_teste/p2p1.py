from transport.tcp import TCP
from transport.udp import UDP

from p2p_tools import *

class P2P:
    def __init__(self,):
        self.inRoom = False
        self.idRoom = None
        self.peersList = [['192.168.24.102','jubileu', self.inRoom, self.idRoom]]

        print('ok')
        while 1:
            self._p2pInitializeResponse()
            print(self.peersList)


    def _p2pInitialize(self):
        socketInit = UDP(5555)
        messageInitialize = idToBin(self.myId)
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

        peersList = binToListOfIpsDecode(peers)
        myInformations = [peersList.pop()]
        myInformations[0][1] = self.myId
        myInformations[0][2] = self.inRoom
        myInformations[0][3] = self.idRoom
        for client in peersList[:-1]:
            if client[0] == myInformations[0]:
                peersList.remove(client)
        returnList = myInformations + peersList
        return returnList

    def _p2pInitializeResponse(self):
        socketResponse = UDP(5554)
        request, addressReceiver = socketResponse.listening()

        copyPeersList = self.peersList[:]
        copyPeersList.append([addressReceiver[0], ''])
        message = listOfPeersToBinConverte(copyPeersList)
        socketResponse.close()
        socketDistributer = TCP()
        socketDistributer.stream(
            applicationPackage=message,
            ipDst=addressReceiver[0],
            portDst=5555,
            option='only',
            definedSocket=None
        )

        flag = True
        for peer in self.peersList:
            if peer[0] == addressReceiver[0]:
                peer[1] = binToId(request)
                flag = False
        if flag:
            self.peersList.append([addressReceiver[0], binToId(request), False, None])

if __name__ == '__main__':
    s = P2P()
