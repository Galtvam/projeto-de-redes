#coding: utf-8

def extractListOfRooms(peersList):
    rooms = {}
    for peer in peersList:
        if peer[2] and (peer[3] != None):
            rooms[peer[3]] = peer
    return rooms

def extractPlayersInRoom(roomID, peerList):
    players = []
    for peer in peersList:
        if peer[2] and (peer[3] == roomID):
            nickname = peer[1]
            ip = peer[0]
            players.append((nickname, ip))
    return players
