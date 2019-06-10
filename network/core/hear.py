#coding: utf-8

from .hlpct.package_coding import *

from .transport.tcp import TCP
from .transport.udp import UDP

from .tools.p2p_tools import *


def apresentationResponse(peersList, addressReceived, newPeerID):
    copyPeersList = peersList[:]
    copyPeersList.append([addressReceived[0], ''])
    message = listOfPeersToBinConverte(copyPeersList)
    package = packageAssembler(
        b'00011',
        False,
        message
    )
    socketDistributer = TCP()
    socketDistributer.stream(
        applicationPackage=package,
        ipDst=addressReceived[0],
        portDst=5555,
        option='only',
        definedSocket=None
    )
    flag = True
    for peer in peersList:
        if peer[0] == addressReceived[0]:
            peer[1] = binToId(newPeerID)
            flag = False
    if flag:
        peersList.append([addressReceived[0], binToId(newPeerID), False, None])

    return peersList
