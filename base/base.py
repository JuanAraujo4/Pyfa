import psycopg2 as psql
import pandas as pd
import warnings
from random import randint
from base.constantes import ENTIDADES

warnings.filterwarnings("ignore")


def __conector():
    return psql.connect(host="localhost",
                        user= "postgres",
                        password="1234",
                        database= "pyfa")

def retorna_aleatorio():

    al = randint(0, len(ENTIDADES)) - 1

    return ENTIDADES[al]


def check_player_in_entity(entity:str, player:str):
    con = __conector()
    cur = con.cursor()

    cur.execute("SELECT id, nome_curto FROM " + entity.replace(" ", "_")),

    dataframe = pd.DataFrame([dado for dado in cur.fetchall()], columns=["id", "jogador"])
    jogadores = dataframe["jogador"].to_list()
    con.close()

    for jogador in jogadores:
        if player.lower() in jogador.lower().split(" ") or player.lower() == jogador.lower():
            return True
    return False


def return_player(entity: str, player:str):

    player = player.capitalize().strip()

    con = __conector()
    cur = con.cursor()

    cur.execute(f"SELECT id, nome_curto, nomecompleto, posicoes, overall FROM " + entity.replace(" ", "_"))
    dataframe = pd.DataFrame([j for j in cur.fetchall()], columns=["id", "nome", "nomecompleto", "posicoes", "overall"])
    

    for jogador in dataframe.iterrows():
        info = jogador[1]
        nomeCurto = info[1].lower()
        nomeCompleto = info[2].lower()

        retorna = {"id": info[0], "nomeCurto": info[1], "nomeCompleto": info[2], "posicoes": info[3], "overall": info[4]}
        if player.lower() in nomeCurto.split(" ") or player.lower() == nomeCurto:
            return retorna
        elif player.lower() in nomeCompleto.split(" ") or player.lower() == nomeCompleto:
            return retorna
        
    con.close()
    return False
