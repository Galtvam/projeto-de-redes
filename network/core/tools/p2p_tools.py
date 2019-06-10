#coding: utf-8

from .address_encoding import *

"""
cada ip na lista de IPs segue o farmato (ip:string, id:string, inRoom:bool, idRoom:int)
"""

def listOfPeersToBinConverte(peersList:list):
    message = ipToBin(peersList[0][0])
    message += idToBin(peersList[0][1])
    if len(peersList) > 1:
        for ipPeer in peersList[1:]:
            message += ipToBin(ipPeer[0])
            message += idToBin(ipPeer[1])
        return message
    return message

def binToListOfIpsDecode(encodedList:bin):
    listOfIps = []
    for i in range(0,(len(encodedList)-1),14):
        ip = binToIp(encodedList[i:i+4])
        id = binToId(encodedList[i+4:i+14])
        peer = [ip, id, False, None]
        listOfIps.append(peer)
    return listOfIps
