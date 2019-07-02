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
        self.room = GameDashboard(self.myNickname, self.network)

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

    def enterInRoom(self, idRoom:int, mode:int=0):
        if not(self.room.gaming):
            #mode corresponde a espectador (1) / jogadr (0)
            commandID = b'00100'
            flag = mode
            message = b''
            package = packageAssembler(commandID, flag, message)
            addr = self.listOfRooms[idRoom]
            multicastToMyNetwork([addr], package)
            #anota no fakeID o ID da sala em questão
            self.network._fakeID = idRoom
        else:
            return False

    def exitRoom(self):
        '''
        Sai da sala, se estiver em alguma
        '''
        self.network.inRoom = False
        self.network.idRoom = None
        self.room.gaming = False
        self.room.hosting = False
        self.room.room = False


    def _refreshRoomsList(self):
        while 1:
            time.sleep(1)
            self.listOfRooms = extractListOfRooms(self.network.peersList)
