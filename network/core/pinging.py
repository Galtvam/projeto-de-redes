#coding: utf-8
import time

from .hlpct.package_coding import *

from .transport.udp import UDP

from .tools.p2p_tools import *

def pingPeers(myID:str, inRoom:bool, idRoom:int, peersList:list):
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
    multicastToMyNetwork(
        peersList,
        package,
        5554
    )


def peersPing(addressReceived, message, peersList, pingList):
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
    
    inList = False
    for peer in peersList:
        if peer[0] == addressReceived[0]:
            peer = refreshedPeer
            inList = True
            break

    if not inList:
        peersList.append(refreshedPeer)
    pingList[addressReceived[0]] = time.time()

def removeOfflinePeers(peersList:list, pingList:dict):
    nowTime = time.time()
    iterableList = list(pingList.keys())
    for peerKey in iterableList:
        if (nowTime - pingList[peerKey]) > 2.5:
            removeOfPeersList(peersList, peerKey)
            del pingList[peerKey]
