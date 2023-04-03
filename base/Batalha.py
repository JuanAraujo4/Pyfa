from os import system 
from base.base import retorna_aleatorio, check_player_in_entity

class Batalha:
    def __init__(self, timeCasa, timeFora):
        self.timeCasa = timeCasa
        self.timeFora = timeFora
        self.montarTimes()

    def montarTimes(self):
        times = [self.timeCasa, self.timeFora]
        for _ in range(1,11+1):
            for time in times:
                self.mostraTimes()

                time_aleatorio = retorna_aleatorio()
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
                
    
    def mostraTimes(self):
        tcNome = self.timeCasa.getNome()
        tfNome = self.timeFora.getNome() 
        tcJoga = self.timeCasa.getJogadores()
        tfJoga = self.timeFora.getJogadores()

        system("cls")
        print(f"{'BATALHA DE TIMES':^119}\n")
        
        print(f"\033[34m{tcNome:<10}\033[m{' ':^99}\033[31m{tfNome:>10}\033[m\n")
        
        print(f"GOL: {tcJoga[0]:<40}{' ':^30}{tfJoga[0]:>40} :GOL")
        print(f"LD:  {tcJoga[1]:<40}{' ':^30}{tfJoga[1]:>40}  :LD")
        print(f"ZAG: {tcJoga[2]:<40}{' ':^30}{tfJoga[2]:>40} :ZAG")
        print(f"ZAG: {tcJoga[3]:<40}{' ':^30}{tfJoga[3]:>40} :ZAG")
        print(f"LE:  {tcJoga[4]:<40}{' ':^30}{tfJoga[4]:>40}  :LE")
        print(f"VOL: {tcJoga[5]:<40}{' ':^30}{tfJoga[5]:>40} :VOL")
        print(f"MEI: {tcJoga[6]:<40}{' ':^30}{tfJoga[6]:>40} :MEI")
        print(f"MEI: {tcJoga[7]:<40}{' ':^30}{tfJoga[7]:>40} :MEI")
        print(f"PD:  {tcJoga[8]:<40}{' ':^30}{tfJoga[8]:>40}  :PD")
        print(f"CA:  {tcJoga[9]:<40}{' ':^30}{tfJoga[9]:>40}  :CA")
        print(f"PE:  {tcJoga[10]:<40}{' ':^30}{tfJoga[10]:>40}  :PE")
       
