from base.base import return_player

class Time:
    def __init__(self, nome):
        self.nome = nome
        self.jogadores = {"GOL": [None], "LE":[None], "ZAG":[None]*2, "LD": [None], "VOL": [None],
                          "ME":[None], "MD": [None], "PE": [None], "CA":[None], "PD": [None]}

    def getNome(self):
        return self.nome

    def getJogadores(self):
        jogadores = []

        for area in self.jogadores.values():
            for jogador in area:
                jogadores.append(jogador if jogador else "")
                
        return jogadores
    
    def addPosicao(self, jogador, posicao):
        self.jogadores[posicao][self.jogadores[posicao].index(None)] = \
            jogador["nomeCurto"]
    
    def checaPosicao(self, posicao):
        try:
            self.jogadores[posicao].index(None)
        except Exception:
            return False
        else:
            return True

    def addJogador(self, time, escolha):
        jogador = return_player(time, escolha)
        posicoes = jogador["posicoes"].split(",")
        nomeJogador = jogador["nomeCurto"]

        posicoesPossiveis = []
        for posicao in posicoes:

            if posicao in ["GK"]:
                if self.checaPosicao("GOL"):
                    posicoesPossiveis.append("GOL")

            if posicao in ["CB"]:
                if self.checaPosicao("ZAG"):
                    posicoesPossiveis.append("ZAG")

            if posicao in ["RB", "RWB"]:
                if self.checaPosicao("LD"):
                    posicoesPossiveis.append("LD")

            if posicao in ["LB", "LWB"]:
                if self.checaPosicao("LE"):
                    posicoesPossiveis.append("LE")
            
            if posicao in ["CDM"]:
                if self.checaPosicao("VOL"):
                    posicoesPossiveis.append("VOL")
            
            if posicao in ["LM", "CAM", "CM"]:
                if self.checaPosicao("MD"):
                    if "MD" not in posicoesPossiveis:
                        posicoesPossiveis.append("MD")
                    
            if posicao in ["RM", "CAM", "CM"]:
                if self.checaPosicao("ME"):
                    if "ME" not in posicoesPossiveis:
                        posicoesPossiveis.append("ME")

            if posicao in ["RW", "RF"]:
                if self.checaPosicao("PD"):
                    posicoesPossiveis.append("PD")

            if posicao in ["ST", "CF"]:
                if self.checaPosicao("CA"):
                    if "CA" not in posicoesPossiveis:
                        posicoesPossiveis.append("CA")

            if posicao in ["LW", "LF"]:
                if self.checaPosicao("PE"):
                    posicoesPossiveis.append("PE")
        
        if not posicoesPossiveis:
            return False
        
        if len(posicoesPossiveis) == 1:
            self.addPosicao(jogador, posicoesPossiveis[0])
            return True
        
        if len(posicoes) > 1:
            posicaoEscolhida = input(f"Qual posição deseja colocar o {nomeJogador}? ").strip().upper()
            while posicaoEscolhida not in posicoesPossiveis:
                print(f"\n\033[31mEscolha uma dessas posicoes {posicoesPossiveis}\033[m]")

                posicaoEscolhida = input(f"Qual posição deseja colocar o \033[04m{nomeJogador}\033[m? ")

            self.addPosicao(jogador, posicaoEscolhida)
            return True
        
