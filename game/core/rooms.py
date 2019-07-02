#coding: utf-8

class Room:
    def __init__(self, ID:int, numberOfPlayers:int, myNickname):
        # status da partida
        self.ID = ID
        self.numPlayers = numberOfPlayers #numero max
        self._start = False

        # todos os jogadores
        self.playersList = [(myNickname,None)] #lista de nicknames

        # infos da partida
        # jogadores vivos
        self.playersAlive = []
        # rodada
        self.round = 1
        # mestre
        self.lastMaster = None
        self.master = None
        # votação
        self.permissionToVote = False
        self.countVotes = {}


    def newPlayer(self, nickname, addr):
        self.playersList.append((nickname, addr))
        #mandar pacote b'00110' contendo infos da sala

    def sync(self, listOfPlayers):
        for player in listOfPlayers:
            self.playersList.append(player)
        self._start = True
        self.playersAlive = self.playersList
