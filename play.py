#coding: utf-8

from game.main import *

class Play:
    def __init__(self):
        print('Bem Vindo\n')
        print('Escolha um nome de usuário! \n')
        while 1:
            nome = input('Nickname: ')
            try:
                self._c = Client(nome)
                break
            except:
                print('Nome inválido, tente novamente! \n')
        self._menu()

    def _menu(self):
        print('\n\nMENU\n\n')
        print('Opções >\n')
        print('[0] - Ver Players Online\n')
        print('[1] - Ver Lista de Salas\n')
        print('[2] - Entrar numa Sala\n')
        print('[3] - Criar uma Sala\n')
        while 1:
            try:
                option = int(input('Selecione o número de uma opção: '))
                if option == 0:
                    self._playerList()
                elif option == 1:
                    self._roomsList()
                elif option == 2:
                    self._roomsList()
                    self._enterRoom()
                elif option == 3:
                    self._createRoom()
                else:
                    raise 'InvalidOption'
            except:
                print('Erro, tente novamente!\n')

    def _playerList(self):
        list = self._c.network.peersList
        print('\n\n'+str(len(list))+' Players Online\n\n')
        for player in list:
            print(player[1]+' ;  jogando = '+str(player[2]) + ' ; sala = '+str(player[3])+'\n')
        self._menu()

    def _roomsList(self):
        rooms = self._c.listOfRooms.keys()
        print('\n\n'+str(len(rooms))+' Salas\n\n')
        for room in rooms:
            print('ID = '+str(room)+'\n')
        self._menu()

    def _enterRoom(self):
        print('\n\nEntrar numa Sala\n\n')
        try:
            id = int(input('Insira o ID da sala para entrar: '))
            opt = self._c.enterInRoom(id)
            if opt:
                print('Entrou na Sala, aguardando o líder começar!')
            else:
                print('Houve falha na tentativa de iniciar o jogo!')
                self._menu()
        except:
            self._enterRoom()

    def _createRoom(self):
        print('\n\nCriação de Sala\n\n')
        try:
            id = int(input('Escolha um ID númerico para sua sala: '))
            numPlayers = int(input('Escolha o número máximo de players (0 é inderteminado): '))
            r = self._c.createGameRoom(id, numPlayers)
            if r:
                print('\nSala criada com Sucesso!\n')
                backupNum = len(self._c.room.room.playersList)
                while 1:
                    check = len(self._c.room.room.playersList)
                    if check != backupNum:
                        print(str(check)+' Players na Sala!\n')
                        print('Deseja Iniciar a partida? caso sim insira 1 caso deseje esperar insira 0.\n')

                        backupNum = check

                        try:
                            opt = int(input('Opção: '))
                        except:
                            opt = 0

                        if opt == 1:
                            try:
                                self._c.room.startMatch()
                                print('acabou')
                            except:
                                print('É necessário ao menos 3 jogadores!')

            else:
                print('ID já utilizado!')
                self._createRoom()

        except:
            print('ID ou Quantidade de Players inválido!\n')
            self._createRoom()




if __name__ == '__main__':
    a = Play()
