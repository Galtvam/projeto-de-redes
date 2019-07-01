#coding: utf-8

def extractListOfRooms(peersList):
    rooms = {}
    for peer in peersList:
        if peer[2]:
            rooms[peer[3]] = peer
    return rooms
