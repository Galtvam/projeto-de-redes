#coding: utf-8

def extractListOfRooms(peersList):
    rooms = {}
    for peer in peersList:
        if peer[2] and (peer[3] != None):
            rooms[peer[3]] = peer
    return rooms

def extractPlayersInRoom(roomID, peersList):
    players = []
    for peer in peersList:
        if peer[2] and (peer[3] == roomID):
            nickname = peer[1]
            ip = peer[0]
            players.append((nickname, ip))
    return players

def offlineDetection(peersList, playersList):
    for player in playersList[1:]:
        mark = False
        for peer in peersList:
            if peer[0] == player[1]:
                mark = True
                break
        if not(mark):
            playersList.remove(player)

def candidates(playersList, lastMaster):
    cand = []
    if len(playersList) > 2:
        for player in playersList[1:]:
            if player[0] != lastMaster:
                cand.append(player[0])
    else:
        for player in playersList:
            if player[0] != lastMaster:
                cand.append(player[0])
                cand[player[0]] = 1
    return cand
