#coding: utf-8

import time

from core.rooms import *
from network.core.hlpct.package_coding import *
from network.core.tools.p2p_tools import *

from core.tools.addressTools import *
from core.tools.roomSuport import *
from core.tools.print_tools import *
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
        thread = simpleThread(self._reestarThread)
        #Inicialização das Threads
        thread.start()

    def create(self, idRoom, numberMaxOfPlayers):
        self.room = Room(idRoom, numberMaxOfPlayers, self.myNickname)
        self.gaming = True
        self.hosting = True

        off = simpleThread(self._offlineRemove)
        off.start()

    def startMatch(self):
        numberOfPlayers = len(self.room.playersList)
        ''' linha de teste '''
        if numberOfPlayers >= 2:
            self.room._start = True
            self.room.playersAlive = self.room.playersList
            self._sendStartMatch(numberOfPlayers)
            print('A partida iniciará em breve!')
            time.sleep(2)
            self.poll()

        else:
            return False

    def poll(self):
        self.room.permissionToVote = True
        t = simpleThread(self._stopwatch1)

        if len(self.room.countVotes.keys()) == 0:
            candidates = candidatesExtractor(self.room.playersAlive, self.room.master)
            if len(candidates) == 1:
                '''
                Só tem duas pessoas jogando
                '''
                self.room.permissionToVote = False
                self.room.countVotes[candidates[0]] = 1
            for person in candidates:
                self.room.countVotes[person] = 0

        if len(candidates) > 1:
            beautifulPrintCandidates(candidates)
            vote = int(input('número: '))
            try:
                if self.room.permissionToVote:
                    chose = candidates[vote]
                    self.room.countVotes[chose] += 1
                    self._sendVote(chose)
                else:
                    print('tempo de votação acabou!')
            except:
                print('Voto Inválido')

        self.room.permissionToVote = False


    def _reestarThread(self):
            try:
                packages = simpleThread(self._checkPackages)
                #Inicialização das Threads
                packages.start()

            except:
                self._reestarThread()

    def _checkPackages(self):
        while 1:
            time.sleep(0.1)
            if len(self._network._packagesQueue) > 0:
                package = self._network._packagesQueue[0]
                del self._network._packagesQueue[0]

                if package[1] == b'00100':
                    self._approveEntry(package)
                elif package[1] == b'00110':
                    self._sync(package)
                elif package[1] == b'01000':
                    self._voteComputing(package[2])

    def _approveEntry(self, package):
        if (self.hosting and
            (int(package[2]) == 0) and
            not(self.room._start) and
            ((len(self.room.playersList) < self.room.numPlayers) or (self.room.numPlayers == 0))
        ):
            player = discoverName(package[0][0], self._network.peersList)
            self.room.newPlayer(player, package[0][0])

            self._sendApprovation(package[0], self.room.numPlayers)

            if len(self.room.playersList) == self.room.numPlayers:
                self.startMatch()

        elif int(package[2]) == 1:
            #espectador
            '''
            faltando
            '''
            pass

        else:
            #caso não haja vaga ou jogo já iniciou e ele queira jogar
            # b'00111'
            self._sendReject(package[0])

    def _sendApprovation(self, addr, numPlayers):
        '''
        envia pacote aceitando a inclusão
        '''
        commandID = b'00110'
        message = bytes(str(numPlayers), 'utf-8')
        package = packageAssembler(commandID, 0, message)
        multicastToMyNetwork([addr], package)

    def _sendReject(self, addr):
        '''
        envia pacote rejeitando a inclusão
        '''
        commandID = b'00111'
        message = b' '
        package = packageAssembler(commandID, 0, message)
        print(package)
        multicastToMyNetwork([addr], package)

    def _sendStartMatch(self, numberOfPlayers):
        '''
        envia pacote iniciando o warmup
        '''
        commandID = b'00110'
        flag = b'1'
        message = bytes(str(numberOfPlayers), 'utf-8')
        package = packageAssembler(commandID, flag, message)
        players = self.room.playersList[1:]
        multicastToMyNetwork(players, package, match=True)

    def _sendVote(self, vote):
        '''
        envia pacote com o voto
        '''
        commandID = b'01000'
        flag = b'0'
        message = bytes(str(vote), 'utf-8')
        package = packageAssembler(commandID, flag, message)
        players = self.room.playersList[1:]
        multicastToMyNetwork(players, package, match=True)

    def _voteComputing(vote):
        try:
            self.room.countVotes[str(vote)] += 1
        except:
            pass

    def _sync(self, package):
        message = package[3]
        numberOfPlayerinMatch = int(message)
        roomID = self._network.idRoom
        playersList = extractPlayersInRoom(roomID, self._network.peersList[1:])

        self.room = Room(roomID, numberOfPlayerinMatch, self.myNickname)
        self.room.sync(playersList)

        off = simpleThread(self._offlineRemove)
        off.start()

        time.sleep(2)
        self.poll()

    def _offlineRemove(self):
        while 1:
            time.sleep(0.5)
            offlineDetection(self._network.peersList, self.room.playersList)

    def _pollResult(self):
        winner = []
        for candidate in self.room.countVotes.keys():
            if len(winner) == 0 and self.room.countVotes[candidate] != 0:
                winner.append(candidate)
            else:
                if self.room.countVotes[candidate] > self.room.countVotes[winner[0]]:
                    winner = [candidate]
                elif self.room.countVotes[candidate] == self.room.countVotes[winner[0]]:
                    winner.append(candidate)

        if len(winner) == 0:
            '''
            o jogo acaba mas não sei como
            '''
        elif len(winner) > 1:
            '''
            houve empate
            '''
            newDict = {}
            for person in winner:
                newDict[person] = 0
            self.room.countVotes = newDict
            self.poll()
        else:
            '''
            teve vencedor
            '''
            self.room.lastMaster = self.room.master
            self.room.master = winner[0]
            self.room.countVotes = {}
            print('O novo líder é: ' + str(self.room.master) + '\n')

    def _stopwatch1(self):
        '''
        Relógio da votação, dura 10 segundos
        '''
        time.sleep(10)
        self.room.permissionToVote = False
        self._pollResult()
