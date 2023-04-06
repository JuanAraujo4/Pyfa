from base.Time import Time 
from base.Batalha import Batalha
from flask import Flask, jsonify
from os import system

try:
    def limpa_tela():
        system("cls")
        print(f"{'BATALHA DE TIMES':^119}\n")
    
    limpa_tela()
    TIME1 = Time(input("\033[mQual é o nome do \033[34;04m1°Time\033[m? "))
    TIME1.nome = f"\033[34;04m{TIME1.nome}\033[m"

    limpa_tela()
    TIME2 = Time(input("Qual é o nome do \033[31;04m2°Time\033[m? "))
    TIME2.nome = f"\033[31;04m{TIME2.nome}\033[m"

    limpa_tela()
    BATALHA = Batalha(TIME1, TIME2)

except KeyboardInterrupt:
    print("Batalha encerrada!")