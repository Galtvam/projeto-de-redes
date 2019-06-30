#coding: utf-8

from network.p2p import *
from gameControl import *

class Client:
    def __init__(self, nickname):
        self.myNickname = nickname
        self.network = P2P(nickname)
        self.room = GameDashboard(self.myNickname)

    def createRoom(self, idRoom:int, maxPlayers):
        self.room.create(idRoom, maxPlayers)
        self.network.playing(idRoom)
