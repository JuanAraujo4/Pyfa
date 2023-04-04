from os import system 
from base.base import retorna_aleatorio, check_player_in_entity

class Batalha:
    def __init__(self, timeCasa, timeFora):
        self.timeCasa = timeCasa
        self.timeFora = timeFora
        self.montarTimes()
        self.sorteados = []

    def montarTimes(self) -> None:
        times = [self.timeCasa, self.timeFora]
        for _ in range(1,11+1):
            for time in times:
                self.mostraTimes()
                
                time_aleatorio = retorna_aleatorio()
                
                while time_aleatorio in self.sorteados():
                    time_aleatorio = retorna_aleatorio()
                
                self.sorteados.append(time_aleatorio)

                while True:
                    if time == self.timeCasa:
                        print(f"\n\033[34m{time.getNome()}: \033[m", end="")
                    else:
                        print(f"\n\033[31m{time.getNome()}: \033[m", end="")

                    escolha = input(f"Escolha um jogador do(a) \033[04m{time_aleatorio}\033[m: ")

                    if check_player_in_entity(time_aleatorio, escolha):
                        if time.addJogador(time_aleatorio, escolha):
                            break
                        else:
                            print(f"\033[31mNão é possivel adicionar esse jogador nessa posição {time_aleatorio}\033[m")
                            continue
                    else:
                        print(f"\033[31mNão há jogadores com esse nome no(a) {time_aleatorio}\033[m")
                        continue
                
    
    def mostraTimes(self) -> None:
        tcNome = self.timeCasa.getNome()
        tfNome = self.timeFora.getNome() 
        tcJoga = self.timeCasa.getJogadores()
        tfJoga = self.timeFora.getJogadores()

        system("cls")
        print(f"{'BATALHA DE TIMES':^119}\n")
        
        print(f"\033[34m{tcNome:<10}\033[m{' ':^99}\033[31m{tfNome:>10}\033[m\n")
        ps = ["GO", "LD", "ZA", "ZA", "LE", "VO", "MD", "ME", "PD", "CA", "PE"]

        for i in range(0, 11):
            print(f"{ps[i]}: {tcJoga['nome'][i]:<44}{tcJoga['overall'][i]:>10}", end="")
            print(' - ', end="")
            print(f"{tfJoga['nome'][i]:<10}{tfJoga['overall'][i]:>44} :{ps[i]}")       
