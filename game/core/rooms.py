#coding: utf-8

class Room:
    def __init__(self, ID:int, numberOfPlayers:int, myNickname):
        self.ID = ID
        self.numPlayers = numberOfPlayers #numero max
        self._start = False

        self.playersList = [(myNickname,None)] #lista de nicknames

    def newPlayer(self, nickname, addr):
        self.playersList.append((nickname, addr))
        #mandar pacote b'00110' contendo infos da sala

    def sync(self, listOfPlayers):
        for player in listOfPlayers:
            self.playersList.append(player)
        self._start = True
