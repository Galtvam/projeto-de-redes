#coding: utf-8

from socket import *
serverName = ''
serverPort = 5555
clientSocket = socket(AF_INET, SOCK_STREAM
clientSocket.connect((serverName,serverPort))
sentence = input('Input lowercase sentence:')
clientSocket.send(bytes(sentence, 'utf-8'))
modifiedSentence = clientSocket.recv(1024)
print('From Server:', modifiedSentence)
clientSocket.close()
