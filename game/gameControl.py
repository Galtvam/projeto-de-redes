#coding: utf-8

from core.rooms import *

class GameDashboard:
    def __init__(self, myNickname):
        self.myNickname = myNickname
        self.gaming = False
        self.room = False

    def create(self, idRoom, numberMaxOfPlayers):
        self.room = Room(idRoom, numberMaxOfPlayers, self.myNickname)
        self.gaming = True
