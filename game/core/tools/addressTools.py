#coding: utf-8

def discoverName(addr, peersList):
    name = None
    for peer in peersList:
        if peer[0] == addr:
            name = peer[1]
    return name

def discoverIp(name, peersList):
    addr = None
    for peer in peersList:
        if peer[1] == name:
            addr = peer[0]
    return addr
