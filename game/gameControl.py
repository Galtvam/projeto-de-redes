#coding: utf-8

import time

from core.rooms import *
from network.core.hlpct.package_coding import *
from network.core.tools.p2p_tools import *

from core.tools.addressTools import *
from core.threads.roomsList_thread import *

class GameDashboard:
    def __init__(self, myNickname, network):
        self.myNickname = myNickname
        self.gaming = False
        self.hosting = False
        self.room = False

        #ligação com a estrutura P2P
        self._network = network

        #Threads
        packages = simpleThread(self._checkPackages)

        #Inicialização das Threads
        packages.start()

    def create(self, idRoom, numberMaxOfPlayers):
        self.room = Room(idRoom, numberMaxOfPlayers, self.myNickname)
        self.gaming = True
        self.hosting = True

    def _checkPackages(self):
        while 1:
            time.sleep(0.1)
            if len(self._network._packagesQueue) > 0:
                package = self._network._packagesQueue[0]
                del self._network._packagesQueue[0]

                if package[1] == b'00100':
                    self._approveEntry(package)

    def _approveEntry(self, package):
        if (self.hosting and
            (int(package[2]) == 0) and
            not(self.room._start) and
            (len(self.room.playersList) < self.room.numPlayers)
        ):
            player = discoverName(package[0], self._network.peersList)
            self.room.newPlayer(player, package[0])

            self._sendApprovation(package[0], self.room.numPlayers)

        elif int(package[2]) == 1:
            #espectador
            pass

        else:
            #caso não haja vaga ou jogo já iniciou e ele queira jogar
            # b'00111'
            pass

    def _sendApprovation(self, addr, numPlayers):
        '''
        envia pacote aceitando a inclusão
        '''
        commandID = b'00110'
        message = bytes(str(numPlayers), 'utf-8')
        package = packageAssembler(commandID, 0, message)
        multicastToMyNetwork([addr], package)
