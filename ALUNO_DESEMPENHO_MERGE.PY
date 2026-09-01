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