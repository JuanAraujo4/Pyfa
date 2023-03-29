import psycopg2 as psql
import pandas as pd
import warnings
from random import randint

warnings.filterwarnings("ignore")

def __conector():
    return psql.connect(host="localhost",
                        user= "postgres",
                        password="1234",
                        database= "pyfa")

def retorna_aleatorio():

    con = __conector()
    cur = con.cursor()

    cur.execute("SELECT nome FROM entities;")

    clubs_or_nation = pd.Series([club[0] for club in cur.fetchall()]).drop_duplicates().to_list()
    al = randint(0,len(clubs_or_nation))

    con.close()
    return clubs_or_nation[al]


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

    cur.execute(f"SELECT nome_curto, posicoes, overall FROM " + entity.replace(" ", "_"))
    dataframe = pd.DataFrame([j for j in cur.fetchall()], columns=["id", "jogadores", "posicoes", "overall"])
    jogadores = dataframe["jogadores"]

    procurado = ""
    for jogador in jogadores:
        if player.lower() in jogador.lower().split(" ") or player.lower() == jogador.lower():
            procurado = jogador
    
    
    
    con.close()
    return False
