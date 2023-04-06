from os import listdir
import pandas as pd
import psycopg2 as psql
from constantes import *

def substituiLetrasIncomuns(texto: str) -> str:
    texto = (texto.replace("ž", "z").replace("č", "c").replace("ć", "c").replace("ž", "z").replace("š", "s")
    .replace("Đ", "D").replace("Å", "A").replace("Ä", "A").replace("Ö", "O").replace("Ø", "O").replace("Ü", "U")
    .replace("Ž", "Z").replace("Č", "C").replace("Ć", "C").replace("Ž", "Z").replace("Š", "S").replace("ó", "o")
    .replace("đ", "d").replace("å", "a").replace("ä", "a").replace("ö", "o").replace("ø", "o").replace("ü", "u")
    .replace("ń", "n").replace("ż", "z").replace("Ż", "Z").replace("Ź", "z").replace("Ń", "N").replace("ñ", "n")
    .replace("Ñ", "N").replace("é", "e").replace("É", "E").replace("Ú", "U").replace("ú", "u").replace("õ", "o")
    .replace("á", "a").replace("Á", "A").replace("Â", "A").replace("â", "a").replace("Ę", "E").replace("ę", "e")
    .replace("Ą", "A").replace("ą", "a").replace("Ł", "L").replace("ł", "l").replace("Ó", "O").replace("ó", "o")
    .replace("ś", "s").replace("Ś", "S").replace("Í", "I").replace("í", "i"))

    return texto

def retornaNomeLiga(clube : str):
    if clube in ['Manchester_United', 'Manchester_City', 'Aston_Villa', 'Tottenham_Hotspur', 'Chelsea', 'Liverpool', 'Arsenal', 'Newcastle_United']:
        return "Premier_League"
    
    elif clube in ['FC_Bayern_München', 'Borussia_Dortmund', 'RB_Leipzig']:
        return "Bundesliga"
    
    elif clube in ['FC_Barcelona', 'Atlético_de_Madrid', 'Real_Madrid_CF']:
        return "La_Liga"

    elif clube in ['FC_Porto', 'SL_Benfica']:
        return "Liga_Portugal"
    
    elif clube in ['Napoli', 'AC_Milan', 'Juventus', 'Inter']:
        return "Serie_A_Tim" 
    
    elif clube in ["Paris_Saint_Germain"]:
        return "Ligue_1"

df = pd.DataFrame()
db = None

# For para cada arquivo na pasta players
for arq in listdir(CSV):

    # Criando um Dataframe 'df_atual' para cada arquivo e depois concatenando ao 'df'
    df_atual = pd.read_csv(CSV+arq, sep=",", encoding="utf-8", low_memory=False)
    df: pd.DataFrame = pd.concat([df, df_atual])

dfTotal = pd.DataFrame()

for arq in listdir(CSV):

    # Criando um Dataframe 'df_atual' para cada arquivo e depois concatenando ao 'dfTotal'
    df_atual = pd.read_csv(CSV+arq, sep=",", encoding="utf-8", low_memory=False)
    dfTotal: pd.DataFrame = pd.concat([dfTotal, df_atual])

# Filtrando apenas colunas necessarias
dfTotal = dfTotal.loc[:, COLUNAS_NECESSARIAS_INGLES]
df = df.loc[:, COLUNAS_NECESSARIAS_INGLES]

# Renomeando as colunas para nomes em portugues.
dfTotal.columns = COLUNAS_NECESSARIAS
df.columns = COLUNAS_NECESSARIAS

# Filtrar times mais conhecidos.
df = df.query(f"clube in ({CLUBES_FAVORITOS})")
df["clube"] = df["clube"].apply(lambda x: x.replace(" ", "_").replace("-", "_"))

# Alterando letras de jogadores que tem caracteres diferentes.
df["nomeCompleto"] = df["nomeCompleto"].apply(lambda x: substituiLetrasIncomuns(x))
dfTotal["nomeCompleto"] = dfTotal["nomeCompleto"].apply(lambda x: substituiLetrasIncomuns(x))

# Adicionando nome das ligas.
df["liga"] =  df["clube"].apply(lambda x:  retornaNomeLiga(x))
    

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

# Tabela de Clubes, Selecoes e Ligas

cursor.execute("""CREATE TABLE entities(
                        id int,
                        nome varchar(50),
                        primary key(id)
                )""")

clubs = df["clube"].apply(lambda x: x).drop_duplicates()

nations = df["nacionalidade"].apply(lambda x: x if x in SELECOES_FAVORITAS else "Brazil").drop_duplicates()

leagues = df["liga"].apply(lambda x: x).drop_duplicates()

entities = pd.concat([nations, leagues, clubs]).to_list()

entities.append("All_Players") # Adicionando 'All_Players', tabela que tem todos os jogadores.

id = 0
for entity in entities:
    id += 1
    query = "INSERT INTO entities values (%s, %s);"
    cursor.execute(query, (id, entity.replace("_", " ")))

# Criando uma tabela para cada time.
for entity in entities:
    cursor.execute(f"DROP TABLE IF EXISTS " + entity)
    cursor.execute("CREATE TABLE " +  entity + """ (
        id int,
        nome_curto varchar(50), nomeCompleto varchar(100), 
        posicoes varchar(20), overall smallint, clube varchar(75), 
        nacionalidade varchar(100), pique smallint, chute smallint, 
        passe smallint, drible smallint, defesa smallint, 
        fisico smallint, faceUrl varchar(100), 
        selecao_Logo_Url varchar(100),
        liga varchar(100),
        primary key(id)
    )""")

# Inserindo os jogadores na tabela
id = 0
for player in df.iterrows():
    id += 1
    player = player[1].to_list()

    dados = [player for player in player]
    dados.insert(0, id)

    cursor.execute("INSERT INTO All_Players values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", dados)

    time = player[4]
    
    cursor.execute("INSERT INTO " + time + " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", dados)
    
    liga = player[-1]

    cursor.execute("INSERT INTO " + liga + " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", dados)

id = 0
for player in dfTotal.iterrows():
    id += 1
    player = player[1].to_list()
    nation = player[5]

    dados = [player for player in player]
    dados.insert(0, id)

    if nation in SELECOES_FAVORITAS:
        cursor.execute("INSERT INTO " + nation + " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", dados)

print("\033[32mOK\033[m")