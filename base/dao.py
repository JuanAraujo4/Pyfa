from os import listdir
import pandas as pd
import psycopg2 as psql

pd.options.display.max_columns = 1000
csv = "./players/"
df = pd.DataFrame()
db = None

try:
    # For para cada arquivo na pasta players
    for arq in listdir(csv):

        # Criando um Dataframe 'df_atual' para cada arquivo e depois concatenando ao 'df'
        df_atual = pd.read_csv(csv+arq, sep=",", encoding="utf-8", low_memory=False)
        df: pd.DataFrame = pd.concat([df, df_atual])
        # df["pace"] = df["pace"].fillna(0)
        # df["shooting"] = df["shooting"].fillna(0)
        # df["passing"] = df["passing"].fillna(0)
        # df["dribbling"] = df["dribbling"].fillna(0)
        # df["defending"] = df["defending"].fillna(0)
        # df["physic"] = df["physic"].fillna(0)

    # Filtrando apenas colunas necessarias
    df = df.loc[:, ["Known As", "Full Name", "Positions Played", "Overall", "Club Name", "Club Jersey Number",
                    "Nationality", "Pace Total", "Shooting Total", "Passing Total", "Dribbling Total",
                    "Defending Total", "Physicality Total", "Image Link", "National Team Image Link"]]

    # Renomeando as colunas para nomes em portugues.
    df.columns = ["nomeCurto", "nomeCompleto", "posicoes", "overall", "clube", "numeroCamisa",
                  "nacionalidade", "pique", "chute", "passe", "drible", "defesa", "fisico", "faceUrl",
                  "selecaoLogoUrl"]

    # Filtrar times mais conhecidos.
    df = df.query("clube in ('Paris Saint-Germain', 'FC Bayern München', 'Manchester United', "
                  "'Manchester City', 'Aston Villa', 'Atlético de Madrid', 'FC Barcelona', "
                  "'Tottenham Hotspur', 'Chelsea', 'Real Madrid CF', 'Liverpool', 'Borussia Dortmund',"
                  "'Juventus', 'Inter', 'Napoli', 'Arsenal', 'AC Milan', 'FC Porto', 'Ajax',"
                  "'RB Leipzig', 'Newcastle United', 'SL Benfica')")
    
    # Colocando os nomes dos jogadores em letra minusculo.
    df["nomeCurto"] = df["nomeCurto"].apply(lambda x: x.lower())
     
    # Trocando nome das ligas para um nome mais facil.
    # df["liga"] = df["liga"].apply(lambda x: 'Espanhola' if x == 'Spain Primera Division' else x)
    # df["liga"] = df["liga"].apply(lambda x: 'Bundesliga' if x == 'German 1. Bundesliga' else x)
    # df["liga"] = df["liga"].apply(lambda x: 'Francesa' if x == 'French Ligue 1' else x)
    # df["liga"] = df["liga"].apply(lambda x: 'Premier League' if x == 'English Premier League' else x)
    # df["liga"] = df["liga"].apply(lambda x: 'Italiana' if x == 'Italian Serie A' else x)

    # Conectando ao banco de dados
    dbPostgres = psql.connect(host="localhost", user="postgres", password="1234")
    cursorPostgres = dbPostgres.cursor()
    dbPostgres.autocommit = True

    # Deletando database caso exista e recriando, e desconectando da base postgres
    cursorPostgres.execute("DROP DATABASE IF EXISTS pyfa;")
    cursorPostgres.execute("CREATE DATABASE pyfa;")
    cursorPostgres.close()
    dbPostgres.close()

    # Conectando a base pyfa
    db = psql.connect(host="localhost", user="postgres", password="1234", database="pyfa")
    db.autocommit = True
    cursor = db.cursor()


    # Criando tabela 'player'
    cursor.execute("""CREATE TABLE player(
                        id int,
                        nome_curto varchar(50), nomeCompleto varchar(100), 
                        posicoes varchar(20), overall smallint, clube varchar(75), 
                        numero_camisa smallint, 
                        nacionalidade varchar(100), pique smallint, chute smallint, 
                        passe smallint, drible smallint, defesa smallint, 
                        fisico smallint, faceUrl varchar(100), 
                        selecao_Logo_Url varchar(100),
                        primary key(id)
                   )""")

    # Inserindo os jogadores na tabela
    id = 0
    for player in df.iterrows():
        id+=1
        player = player[1].to_list()

        dados = [player for player in player]
        dados.insert(0, id)

        query = "INSERT INTO player values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        cursor.execute(query, dados)

    # Tabela de Clubes

    cursor.execute("""CREATE TABLE club(
                            id int,
                            nome varchar(50),
                            primary key(id)
                    )""")

    clubs = pd.Series(dtype=str)
    for player in df.iterrows():
        clube = player[1].to_list()[4]

        clubs = pd.concat([clubs, pd.Series([clube])])
    clubs.drop_duplicates(inplace=True)

    id = 0
    for club in clubs.to_list():
        id += 1
        query = "INSERT INTO club values (%s, %s);"
        cursor.execute(query, (id, club))

    # Tabela de Selecoes
    cursor.execute("""CREATE TABLE nation(
                                id int,
                                nome varchar(50),
                                primary key(id)
                        )""")

    nations = pd.Series(dtype=str)
    for player in df.iterrows():
        nation = player[1].to_list()[6]

        nations = pd.concat([nations, pd.Series([nation])])
    nations.drop_duplicates(inplace=True)

    id = 0
    for nation in nations.to_list():
        id += 1
        query = "INSERT INTO nation values (%s, %s);"
        cursor.execute(query, (id, nation))

except psql.DatabaseError:
   print("\033[31mNao foi possivel conectar ao banco de dados.\033[m")

except FileNotFoundError:
    print(f'\033[31mO arquivo "{csv}" nao foi encontrado.\033[m')

except KeyboardInterrupt:
    print("\033[31mNao foi possivel fazer as alteracoes pois o programa foi parado.\033[m")

except Exception as err:
    print(f"Houve o erro: {err}.")

else:
    print("\033[32mOK!\033[m")
    cursor.close()
    db.close()
