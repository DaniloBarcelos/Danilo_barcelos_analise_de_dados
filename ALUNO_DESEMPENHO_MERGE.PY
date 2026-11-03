"""
Disciplina: Programação para Análise de Dados
Nome do aluno: Danilo Barcelos
Matrícula: 202308875965
Email: 202308875965@alunos.ibmec.edu.br
"""
import pandas as pd
df_localidades = pd.read_excel("alunos_localidade_carro_merge.xlsx")
df_alunos= pd.read_csv("alunos_desempenho.csv")
df_localidades. head()
pd.merge(df_alunos, df_localidades, on="id_aluno")

# 1. Quais variáveis existem na base de desempenho e quais existem na base complementar?
df_localidades.info()
df_alunos.info()

# 2. Qual variável deve ser utilizada como chave para realizar o merge?
pd.merge(df_alunos, df_localidades, on="id_aluno", how="left")

# 3. Por que id_aluno é uma chave mais segura do que o nome do estudante?

# 4. Antes do merge, quantos registros existem em cada base?
df_localidades.shape
df_alunos.info()
# 5. Realize o merge utilizando id_aluno. Quantos estudantes existem na base resultante?
pd.merge(df_alunos, df_localidades, on="id_aluno", how="left")
# 6. Todos os estudantes foram associados corretamente? Como você verificou isso?
# 6. Todos os estudantes foram associados corretamente? Como você verificou isso?
pd.merge(df_alunos, df_localidades, on="id_aluno", how="outer", indicator=True)
# 7. Existe algum estudante presente apenas em uma das bases? Se houver, como você identificaria esses casos?

# 8. Qual tipo de merge é mais adequado para preservar todos os estudantes da base principal? Justifique.


import requests
import pandas as pd

df = pd.merge(df_alunos, df_localidades, on="id_aluno", how="left")

ceps = df["cep"].unique()

dados_ceps = []

for cep in ceps:
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    dados = response.json()
    dados_ceps.append(dados)
    print(cep)

print(dados_ceps)

import requests

endereco = "Rua padre zeferino"
a
url = "https://nominatim.openstreetmap.org/search"

params = {
    "q": endereco,
    "format": "json",
    "limit": 1,
    "countrycodes": "br"
}

headers = {
    "User-Agent": "meu_projeto_geocoding/1.0"
}

response = requests.get(url, params=params, headers=headers)

dados = response.json()

if len(dados) > 0:
    latitude = float(dados[0]["lat"])
    longitude = float(dados[0]["lon"])

    print("Latitude:", latitude)
    print("Longitude:", longitude)
else:
    print("Endereço não encontrado")


# ---------------------------------------------------------
# Parte 2 - APIs: ViaCEP + Nominatim + distancia ate o Ibmec
# ---------------------------------------------------------
import pandas as pd
import requests
import time
import math

pd.set_option("display.max_rows", None)      # mostra todas as linhas
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", 250)

df_alunos = pd.read_csv("alunos_desempenho.csv")
df_localidades = pd.read_excel("alunos_localidade_carro_merge.xlsx")

df = pd.merge(df_alunos, df_localidades.drop(columns=["aluno"]), on="id_aluno", how="left")

headers = {"User-Agent": "trabalho_ibmec_202308875965"}

def buscar(url, params=None):
    for tentativa in range(3):
        try:
            resposta = requests.get(url, params=params, headers=headers, timeout=20)
            if resposta.status_code == 200:
                return resposta.json()
        except Exception as e:
            print("tentativa", tentativa + 1, "falhou:", e)
        time.sleep(3)
    return None

# --- ViaCEP: endereco de cada CEP ---
ceps = df["cep"].unique()
dados_ceps = []

for cep in ceps:
    dados = buscar(f"https://viacep.com.br/ws/{cep}/json/")
    if dados is None:
        dados = {}
    dados_ceps.append({
        "cep": cep,
        "logradouro": dados.get("logradouro", ""),
        "bairro": dados.get("bairro", ""),
        "localidade": dados.get("localidade", ""),
        "uf": dados.get("uf", "")
    })
    time.sleep(0.5)

df_ceps = pd.DataFrame(dados_ceps)
df_ceps["endereco"] = (df_ceps["logradouro"] + ", " + df_ceps["bairro"] + ", " +
                       df_ceps["localidade"] + ", " + df_ceps["uf"])

print("CEPs consultados:", len(df_ceps))

# --- Nominatim: latitude e longitude de cada endereco ---
url = "https://nominatim.openstreetmap.org/search"

latitudes = []
longitudes = []

for endereco in df_ceps["endereco"]:
    lat, lon = None, None

    # tenta o endereco completo e depois so bairro + cidade
    for busca in [endereco, endereco.split(", ", 1)[1]]:
        params = {"q": busca, "format": "json", "limit": 1, "countrycodes": "br"}
        dados = buscar(url, params)
        time.sleep(1)   # Nominatim pede 1 requisicao por segundo

        if dados and len(dados) > 0:
            lat = float(dados[0]["lat"])
            lon = float(dados[0]["lon"])
            break

    latitudes.append(lat)
    longitudes.append(lon)

df_ceps["latitude"] = latitudes
df_ceps["longitude"] = longitudes

# confere se as coordenadas sairam diferentes entre si
print("Coordenadas distintas:", df_ceps["latitude"].nunique(), "de", len(df_ceps))

# --- Coordenada do Ibmec ---
params = {"q": "SIG Quadra 4, Brasilia, DF, Brasil", "format": "json", "limit": 1, "countrycodes": "br"}
dados = buscar(url, params)

lat_ibmec = float(dados[0]["lat"])
lon_ibmec = float(dados[0]["lon"])

print("Ibmec - SIG Quadra 4:", lat_ibmec, lon_ibmec)

# --- Distancia ate o Ibmec (Haversine, em km) ---
distancias = []

for lat, lon in zip(df_ceps["latitude"], df_ceps["longitude"]):
    if lat is None:
        distancias.append(None)
        continue
    dlat = math.radians(lat - lat_ibmec)
    dlon = math.radians(lon - lon_ibmec)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat_ibmec)) * math.cos(math.radians(lat)) * math.sin(dlon/2)**2
    distancias.append(round(6371 * 2 * math.asin(math.sqrt(a)), 2))

df_ceps["distancia"] = distancias
df_ceps.to_csv("ceps_geocodificados.csv", index=False)

print(df_ceps[["cep", "endereco", "latitude", "longitude", "distancia"]])

# --- Tabela final ---
df_final = pd.merge(df, df_ceps[["cep", "endereco", "latitude", "longitude", "distancia"]],
                    on="cep", how="left")

tabela = df_final[["id_aluno", "aluno", "faltas", "cep", "endereco",
                   "latitude", "longitude", "distancia"]].copy()

tabela.columns = ["IDAluno", "Nome", "Faltas", "CEP", "Endereco",
                  "Latitude", "Longitude", "Distancia_km"]

tabela["Latitude"] = tabela["Latitude"].round(4)
tabela["Longitude"] = tabela["Longitude"].round(4)

tabela.to_excel("tabela_final_alunos.xlsx", index=False)

print("Total de alunos na tabela:", len(tabela))

display(tabela)   # todos os 150


# regressao liner
import sqlite3
import pandas as pd
engine = sqlite3.connect("db_alunos.db")
query = "select * from tb_alunos_final"
df_final = pd.read_sql(query, engine)
df_final.columns
import statsmodels.api as sm
x = df_final["faltas"]
y = df_final['nota_final']
x = sm.add_constant(x)
modelo = sm.OLS(y, x, missing="drop").fit()
print(modelo.summary())
# definicao das colunas (variaveis independentes)
col = ['faltas','horas_estudo_semana', 'participacao_aula',
       'horas_trabalho_semana', 'horas_sono_noite',
       'distancia_faculdade_km', 'valor_carro_10mil']
x = df_final[col]
y = df_final['nota_final']
x = sm.add_constant(x)
modelo = sm.OLS(y, x, missing="drop").fit()
print(modelo.summary())

#correlacao
df_final_numerico = df_final[col]
df_final_numerico.corr()
import seaborn as sns
sns.heatmap(df_final_numerico.corr())

#histograma 
sns.histplot(df_final_numerico, x="faltas")

#boxplot 
sns.boxplot(df_final_numerico)

# dispersão
col = ['nota_final', 'faltas']
df_final_regressao = df_final[col]
sns.regplot(data=df_final_regressao, x='nota_final', y='faltas')