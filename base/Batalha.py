from os import system 
from base.base import retorna_aleatorio, check_player_in_entity
from base.Time import Time 

class Batalha:
    def __init__(self, timeCasa:Time, timeFora:Time):
        self.timeCasa = timeCasa
        self.timeFora = timeFora
        self.montarTimes()

    def montarTimes(self) -> None:
        times = [self.timeCasa, self.timeFora]
        sorteados = []
        for _ in range(1,11+1):
            for time in times:
                self.mostraTimes()
                
                time_aleatorio = retorna_aleatorio()
                
                while time_aleatorio in sorteados:
                    time_aleatorio = retorna_aleatorio()
                
                sorteados.append(time_aleatorio)

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

        self.mostraTimes()
        tcOver = str(self.timeCasa.mediaOver())
        tfOver = str(self.timeFora.mediaOver())
        if int(tcOver) > int(tfOver):
            print(f"\n\033[32m{'Total: ' + tcOver:<70} \033[31m{tfOver + ' :Total':>70}\033[m")
            print(f"O time {self.timeCasa.getNome()} ganhou!")
        elif int(tcOver) < int(tfOver):
            print(f"\n\033[31m{'Total: ' + tcOver:<70} \033[32m{tfOver + ' :Total':>70}\033[m")
            print(f"O time {self.timeFora.getNome()} ganhou!")
        else:
            print(f"{'Total: ' + tcOver:<70} {tfOver + ' :Total':>70}")
            print("Deu empate!")

    
    def mostraTimes(self) -> None:
        tcNome = self.timeCasa.getNome()
        tfNome = self.timeFora.getNome() 
        tcJoga = self.timeCasa.getJogadores()
        tfJoga = self.timeFora.getJogadores()

        system("cls")
        print(f"{'BATALHA DE TIMES':^119}\n")
        
        print(f"{tcNome:<70} {tfNome:>70}")
        ps = ["GO", "LD", "ZA", "ZA", "LE", "VO", "ME", "ME", "PD", "CA", "PE"]

        for i in range(0, 11):
            print(f"{ps[i]}: {tcJoga['nome'][i]:<44}{tcJoga['overall'][i]:>10}", end="")
            print(' - ', end="")
            print(f"{tfJoga['overall'][i]:<10}{tfJoga['nome'][i]:>44} :{ps[i]}")       
