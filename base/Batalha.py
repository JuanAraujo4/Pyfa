from os import system 
from base.base import retorna_aleatorio, check_player_in_entity

class Batalha:
    def __init__(self, timeCasa, timeFora):
        self.timeCasa = {"TIME":timeCasa, "GOLS": 0}
        self.timeFora = {"TIME":timeFora, "GOLS": 0}
        self.montarTimes()

    def montarTimes(self):
        times = [self.timeCasa, self.timeFora]
        for _ in range(1,11+1):
            for time in times:
                self.mostraTimes()

                time_aleatorio = retorna_aleatorio()
                while True:

                    escolha = input(f"\nEscolha um jogador do(a) \033[04m{time_aleatorio}\033[m: ")

                    if check_player_in_entity(time_aleatorio, escolha):
                        if time["TIME"].addJogador(time_aleatorio, escolha):
                            break
                        else:
                            continue
                    else:
                        print(f"\033[31mNão há jogadores com esse nome no(a) {time_aleatorio}\033[m")
                        continue
                
    
    def mostraTimes(self):
        tcNome = self.timeCasa["TIME"].getNome()
        tfNome = self.timeFora["TIME"].getNome() 
        tcJoga = self.timeCasa["TIME"].getJogadores()
        tfJoga = self.timeFora["TIME"].getJogadores()
        print(f"{tcNome:<10}{'-':^99}{tfNome:>10}")

        system("cls")
        print(f"{'BATALHA DE TIMES':^119}\n")
        
        for jogador in range(1,11+1):
            
            formatado = f"{jogador} - {tcJoga[jogador - 1]}"
            print(f"{formatado:<10}", end="")

            print(f"{'-':^99}", end="")

            formatado = f"{tfJoga[jogador - 1]} - {jogador}"
            print(f"{formatado:>10}")
       
