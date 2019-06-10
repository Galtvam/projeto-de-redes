#coding: utf-8

from .hlpct.package_coding import *

from .transport.tcp import TCP
from .transport.udp import UDP

from .tools.p2p_tools import *
from .tools.ipDiscover import *

def apresentation(myId, inRoom, idRoom):
    socketInit = UDP(5555)
    messageInitialize = idToBin(myId)
    package = packageAssembler(
        b'00001',
        False,
        messageInitialize
    )

    socketInit.stream(
        applicationPackage=package,
        ipDst='224.0.0.1',
        portDst=5554
    )
    socketInit.close()
    socketReceiver = TCP(5555)
    try:
        socketReceiver._mainSocket.settimeout(1) #espera 1 segundos por uma conexão
        address, port, receivedPackage = socketReceiver.listening(
            option='only',
            numberOfConnections=1,
            bufferSize=80000
        )

        commandID, receivedFlag, receivedMessage = packageDisassembler(receivedPackage)

        if commandID == b'00011':
            peersList = binToListOfIpsDecode(receivedMessage)
            myInformations = [peersList.pop()]
            myInformations[0][1] = myId
            myInformations[0][2] = inRoom
            myInformations[0][3] = idRoom
            for client in peersList[:]:
                if client[0] == myInformations[0][0]:
                    peersList.remove(client)
            returnList = myInformations + peersList
            return returnList
        else:
            pass

    except:
        try:
            myIp = getIp()
        except:
            print("Detecção automatica de IP falhou, insira manualmente o IP!")
            myIp = input('IP: ')

        returnList = [[myIp, myId, inRoom, idRoom]]
        return returnList
