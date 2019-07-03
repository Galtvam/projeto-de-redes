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
        peersList[1:],
        package,
        5554
    )


def peersPing(addressReceived, message, peersList, pingList, autorizationFlag):
    encodedID = message[:10]
    encodedFlagRoom = message[10]
    encodedIdRoom = message[11:]

    id = binToId(encodedID)
    flagRoom = bool(int(chr(encodedFlagRoom)))
    if flagRoom:
        try:
            idRoom = int(encodedIdRoom)
        except:
            idRoom = 'aquecimento'
    else:
        idRoom = None
    refreshedPeer = [addressReceived[0], id, flagRoom, idRoom]

    #checa se pode adicionar na lista
    while not autorizationFlag:
        time.sleep(0.1)

    autorizationFlag = False
    inList = False
    for peerIndex in range(len(peersList)):
        if peersList[peerIndex][0] == addressReceived[0]:
            peersList[peerIndex] = refreshedPeer
            inList = True
            break

    if not inList:
        peersList.append(refreshedPeer)
    pingList[addressReceived[0]] = time.time()
    autorizationFlag = True


def removeOfflinePeers(peersList, pingList, autorizationFlag):
    nowTime = time.time()
    iterableList = list(pingList.keys())

    #checa se pode adicionar na lista
    while not autorizationFlag:
        time.sleep(0.1)

    autorizationFlag = False
    for peerKey in iterableList:
        if (nowTime - pingList[peerKey]) > 2.5:
            removeOfPeersList(peersList, peerKey)
            del pingList[peerKey]
    autorizationFlag = True
