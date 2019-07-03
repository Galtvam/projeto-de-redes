#coding: utf-8

import time

from .core.rooms import *
from .network.core.hlpct.package_coding import *
from .network.core.tools.p2p_tools import *

from .core.tools.addressTools import *
from .core.tools.roomSuport import *
from .core.tools.print_tools import *
from .core.threads.roomsList_thread import *

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
        if numberOfPlayers >= 3:
            self.room._start = True
            self.room.playersAlive = self.room.playersList
            self._sendStartMatch(numberOfPlayers)
            print('A partida iniciará em breve!\n')
            time.sleep(2)
            self.poll()

        else:
            raise 'PlayersNumInvalid'

    def poll(self):
        self.room.permissionToVote = True
        t = simpleThread(self._stopwatch1)
        t.start()

        if len(self.room.countVotes.keys()) == 0:
            candidates = candidatesExtractor(self.room.playersAlive, self.room.master)
            if len(candidates) == 1:
                '''
                Só tem duas pessoas jogando
                '''
                self.room.permissionToVote = False
                self.room.countVotes[candidates[0]] = 1

            else:
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
                    print('Tempo de votação acabou!')
            except:
                print('Voto Inválido')

        self.room.permissionToVote = False

    def _startRound(self):
        self.room.round += 1
        print('Rodada '+str(self.room.round))
        if self.myNickname == self.room.master:
            # sou o líder
            print('Você é o líder...')
            correctWord = input('Palavra da rodada: ')
            print('Separe as silábas por "-" \n')
            correctDivision = input('Divisão silábica correta: ')
            sizeWord = str(len(correctWord))
            self.room._answer = correctDivision
            self._sendStartRound(sizeWord, correctWord, correctDivision)
            print('Aguardando respostas!')

            timer = simpleThread(self._stopwatch2)
            timer.start()


        else:
            print('Aguardando o líder selecionar a palavra!')
            # sou só um jogador
            while not(self.room.startRound):
                time.sleep(0.5)

            for alives in self.room.playersAlive:
                if self.myNickname == alives[0]:
                    # estou jogando ainda
                    self.room._canAnswer = True

                    #tempo da rodada
                    timer = simpleThread(self._stopwatch2)
                    selection = simpleThread(self._answer)
                    timer.start()
                    if self.room.startRound:
                        selection.start()
                    break

    def _answer(self):
        #posso jofar
        print('Faça a divisão silabica da palavra: '+self.room.word+'\n')
        print('OBS: As silabas devem ser separadas por "-"\n')
        userAnswer = input('resposta: ')
        if self.room._canAnswer:
            #dentro do Tempo
            self.room.playersList[0][2] = userAnswer
            self._sendAnswer(userAnswer)
        else:
            #fora do tempo
            print('Você excedeu o tempo para a resposta!')


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
                elif package[1] == b'10000':
                    word, answer = wordPackageExtractor(package[2])
                    self.room.word = word
                    self.room._answer = answer
                    self.room.startRound = True
                elif package[1] == b'10001':
                    origin = package[0][0]
                    nameOrigin = discoverName(origin, self._network.peersList)
                    self._answerComputing(nameOrigin, package[2])


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

    def _sendStartRound(self, sizeWord, word, division):
        '''
        envia pacote com respostas da rodada, inicia a rodada
        '''
        commandID = b'10000'
        flag = b'1'
        message = sizeWord + word + division
        encodedMessage = bytes(message, 'utf-8')
        package = packageAssembler(commandID, flag, encodedMessage)
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

    def _sendAnswer(self, answer):
        '''
        envia pacote com o voto
        '''
        commandID = b'10001'
        flag = b'0'
        message = bytes(str(answer), 'utf-8')
        package = packageAssembler(commandID, flag, message)
        players = self.room.playersList[1:]
        multicastToMyNetwork(players, package, match=True)


    def _voteComputing(self, vote):
        try:
            self.room.countVotes[str(vote)] += 1
        except:
            pass

    def _sync(self, package):
        print('A partida iniciará em breve!\n')
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
        try:
            while 1:
                time.sleep(0.5)
                offlineDetection(self._network.peersList, self.room.playersList)
        except:
            pass

    def _pollResult(self):
        winner = []
        for candidate in self.room.countVotes.keys():
            if len(winner) == 0 and self.room.countVotes[candidate] > 0:
                winner.append(candidate)
            else:
                try:
                    if self.room.countVotes[candidate] > self.room.countVotes[winner[0]]:
                        winner = [candidate]
                    elif self.room.countVotes[candidate] == self.room.countVotes[winner[0]]:
                        winner.append(candidate)
                except:
                    pass

        if len(winner) == 0:

            print('O jogo acabou sem vencedores!')
            print('Obrigado por jogar, reinicie o client para se divertir mais!')

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
            self._startRound()

    def _answerComputing(self, name, answer):
        word = ''
        for l in answer:
            word += chr(l)
        for user in self.room.playersAlive:
            if user[0] == name:
                user[2] = word
                break

    def _roundResult(self):
        eliminated = []
        for player in self.room.playersAlive:
            if (player[2] != self.room._answer) and (player[0] != self.room.master):
                eliminated.append(player)

        print('A resposta correta era: '+self.room._answer + '\n')
        for loser in eliminated:
            self.room.playersAlive.remove(loser)
            print(loser[0] + ' foi eliminado.\n')

        if len(self.room.playersAlive) == 1:
            print('Vencedor: '+self.room.playersAlive[0][0]+'\n')
            print('Obrigado por jogar, reinicie o client para se divertir mais!')
        else:
            # acabou o round, chama votação
            self.room.word = ''
            self.room._answer = ''
            self.room._canAnswer = False
            beautifulTable(self.room.playersAlive)
            self.poll()


    def _stopwatch1(self):
        '''
        Relógio da votação, dura 10 segundos
        '''
        time.sleep(10)
        self.room.permissionToVote = False
        self._pollResult()

    def _stopwatch2(self):
        '''
        Relógio da resposta em uma rodada, dura 15 segundos
        '''
        time.sleep(15)
        self.room._canAnswer = False
        self.room.startRound = False
        ''' chama o fim da rodada '''
        self._roundResult()
