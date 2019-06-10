#coding: utf-8

from .hlpct.package_coding import *

from .transport.udp import UDP

from .tools.address_encoding import *

def pingPeers(myID:str, inRoom:bool, idRoom:int):
    pingerSocket = UDP()
    idMessage = idToBin(myID)
    if inRoom:
        flagRoom = b'1'
        idOfRoom = bytes(str(idRoom), 'utf-8')
    else:
        flagRoom = b'0'
        idOfRoom = b'0'

    message = idMessage + flagRoom + idOfRoom
    package = packageAssembler(
        b'00010',
        False,
        message
    )
    pingerSocket.stream(
        applicationPackage=package,
        ipDst='224.0.0.1',
        portDst=5554
    )

    pingerSocket.close()


def peersPing(addressReceived, message, peersList):
    encodedID = message[:10]
    encodedFlagRoom = message[10]
    encodedIdRoom = message[11:]

    id = binToId(encodedID)
    flagRoom = bool(int(encodedFlagRoom))
    if flagRoom:
        idRoom = int(encodedIdRoom)
    else:
        idRoom = None
    refreshedPeer = [addressReceived[0], id, flagRoom, idRoom]

    for peer in peersList:
        if peer[0] == addressReceived[0]:
            peer = refreshedPeer
