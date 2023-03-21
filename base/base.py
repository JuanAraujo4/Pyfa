import psycopg2 as psql
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

def __conector():
    return psql.connect(host="localhost",
                        user= "postgres",
                        password="1234",
                        database= "pyfa")

def retorna_aleatorio():

    con = __conector()
    cur = con.cursor()

    cur.execute("SELECT clube FROM player;")

    clubs_or_nation = pd.Series([club[0] for club in cur.fetchall()]).drop_duplicates().to_list()

    con.close()
    return clubs_or_nation


def check_player_in_entity(entity, player):
    con = __conector()
    cur = con.cursor()

    cur.execute("SELECT id, nome_curto, clube FROM player WHERE clube = %s OR nacionalidade = %s;", 
                (entity, entity)),

    dataframe = pd.DataFrame([dado for dado in cur.fetchall()], columns=["id", "jogador", "clube"])
    jogadores = dataframe["jogador"].to_list()
    con.close()

    for jogador in jogadores:
        if player.lower() in jogador.lower().split(" "):
            return True 
    return False


def return_player(player):

    player = player.capitalize().strip()

    con = __conector()
    cur = con.cursor()

    cur.execute(f"SELECT * FROM player WHERE nome_curto LIKE '%{player}%';")

    jogador = pd.DataFrame([j for j in cur.fetchall()])

    con.close()
    return jogador
