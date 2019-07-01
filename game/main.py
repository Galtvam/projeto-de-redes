#coding: utf-8

from gameControl import *
from network.p2p import *

from core.tools.roomSuport import *
from core.threads.roomsList_thread import *

class Client:
    def __init__(self, nickname):
        self.myNickname = nickname
        self.listOfRooms = {}
        self.network = P2P(nickname)
        self.room = GameDashboard(self.myNickname)

        #Theads
        refreshRooms = simpleThread(self._refreshRoomsList)

        #Inicialização das Threads
        refreshRooms.start()

    def createRoom(self, idRoom:int, maxPlayers):
        time.sleep(1)
        if not(idRoom in self.listOfRooms.keys()):
            self.room.create(idRoom, maxPlayers)
            self.network.playing(idRoom)
            return True
        else:
            return False

    def _refreshRoomsList(self):
        while 1:
            time.sleep(1)
            self.listOfRooms = extractListOfRooms(self.network.peersList)
