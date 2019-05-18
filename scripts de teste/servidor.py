from socket import *
serverPort = 11000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while 1:
    connectionSocket, addr = serverSocket.accept()
    print(type(addr[1]))
    sentence = connectionSocket.recv(1024)
    setence = str(sentence)
    capitalizedSentence = sentence.upper()
    connectionSocket.send(bytes(capitalizedSentence))
    connectionSocket.close()
