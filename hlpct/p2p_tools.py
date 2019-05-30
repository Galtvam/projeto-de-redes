from address_encoding import *

def listOfPeersToBinConverte(peersList:list):
    message = ipToBin(peersList[0])
    if len(peersList) > 1:
        for ipPeer in peersList[1:]:
            message += ipToBin(ipPeer)
        return message
    return message

def binToListOfIpsDecode(encodedList:bin):
    listOfIps = []
    for index in range(0,(len(listOfIps)-1),4):
        ip = binToIp(encodedList[i:i+4])
        listOfIps.append(ip)
    return listOfIps
