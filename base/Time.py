from base.base import return_player

class Time:
    def __init__(self, nome):
        self.nome = nome
        self.jogadores = {"GK": [None], "DEF": [None]*3, "MEI":[None]*4, "ATA":[None]*3}

    def getNome(self):
        return self.nome

    def getJogadores(self):
        jogadores = []

        for area in self.jogadores.values():
            for jogador in area:
                jogadores.append(jogador if jogador != None else "")
                
        return jogadores
    
    def addJogador(self, time, escolha):
        posicoes = return_player(time, escolha)

        print(posicoes)