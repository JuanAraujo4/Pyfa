from base.Time import Time 
from base.Batalha import Batalha
from flask import Flask, jsonify
from os import system


def limpa_tela():
    system("cls")
    print(f"{'BATALHA DE TIMES':^119}\n")
    

limpa_tela()
TIME1 = Time(input("Qual é o nome do \033[04m1°Time\033[m? "))
limpa_tela()
TIME2 = Time(input("Qual é o nome do \033[04m2°Time\033[m? "))
limpa_tela()

BATALHA = Batalha(TIME1, TIME2)