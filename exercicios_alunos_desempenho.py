"""
Disciplina: Programação para Análise de Dados
Nome do aluno: Danilo Barcelos
Matrícula: 202308875965
Email: 202308875965@alunos.ibmec.edu.br
"""

import pandas as pd
df = pd.read_csv("alunos_desempenho.csv")

df.shape

1. EXPLORAÇÃO INICIAL
# 1. O que representa cada linha do DataFrame?
df.head()

df.tail(10)
# 2. O que representa cada coluna?
df.columns

# 3. Qual é a unidade de análise desta base?
"São as informações dos alunos"

# 4. Quantas linhas existem?

df.shape[0]

# 5. Quantas colunas existem?

df.shape[1]

# 6. O número de linhas representa exatamente o número de estudantes?  Explique.
"Sim porque cada aluno tem seu ID unico"

# 7. Liste todas as variáveis da base.
df.info()

# 8. Classifique as variáveis como identificadoras, categóricas ou quantitativas.

df["participacao_aula"].unique()

df["participou_monitoria"].unique()


2. ESTRUTURA E ORGANIZAÇÃO
# Quais variáveis são numéricas?
df.info()
# Quais variáveis aparecem como object?
"nenhuma"
# Por que aluno, curso e período não são variáveis numéricas?
"pq são categoricos"
# A presença de dados faltantes pode alterar o tipo de uma coluna? Explique.
df.isnull() . sum()
"Não"
# Qual a vantagem de selecionar apenas as variáveis necessárias para uma determinada análise?
df.columns
col = ['id_alunos', 'curso', 'periodo', 'nota_final', 'faltas']
df_filtrado = df[col]

#3. QUALIDADE DOS DADOS
#14. Quais colunas possuem valores faltantes?
df.isnull() . sum()
#15. Quantos valores faltantes existem em cada coluna?
df.isnull() . sum()
#16. Qual variável possui maior quantidade de dados faltantes?
df.isnull() . sum() .sort_values(ascending=False)
ou 
df.isnull() . sum(). idxmax()
#17. Uma coluna com aproximadamente 3% de dados ausentes deveria ser automaticamente eliminada? Explique.
"Não, pq perdeira infromações improtantes"
#18. Quantos alunos estão sem nota final?
df.isnull().sum()
#19. Podemos utilizar esses estudantes para calcular a média das notas? Explique.
"Não senão estariamos inferindo na nota final do aluno"
#20. Seria correto substituir todas as notas faltantes por zero? Justifique.
"Não senão estarimos inferindo na nota final desses alunos"

#4. REGISTROS DUPLICADOS

#21. Existem linhas completamente duplicadas?
df.duplicated().sum()
#22. Por que duplicidades podem prejudicar uma análise?
"Pq vc acrescenta uma informação ja existente na analise"
#23. Por que seria um problema encontrar dois alunos diferentes com o mesmo id_aluno?

#5. ANÁLISE DESCRITIVA BÁSICA
#24. Qual é a média da nota final?
df["nota_final"].mean()
#25. Qual é a mediana da nota final?
df["nota_final"].median()
#26. Qual é o número médio de faltas?
df["faltas"].mean()
#27. Qual é o máximo de faltas registrado?
df["faltas"].max()
#28. Qual é a maior quantidade de horas de estudo semanal?
df["horas_estudo_semana"].max()
#29. Algum valor parece estranho ou muito distante dos demais? Cite exemplos.
df["horas_estudo_semana"].describe()
#30. A média e a mediana da nota são semelhantes? O que essa comparação pode indicar?
"Sim, são semelhante e indicam que não existem muito outliers"
#31. Compare a média, a mediana e o máximo da variável faltas. O que você observa?
df["faltas"].describe()

#6. IDENTIFICAÇÃO DE OUTLIERS
#32. Existem estudantes com quantidade de faltas muito superior aos demais?
df["faltas"].describe()
df.sort_values("faltas", ascending=False).head(10)
#33. Existem valores muito elevados de horas de estudo?
df["horas_estudo_semana"].describe()
df.sort_values("horas_estudo_semana", ascending=False).head(10)
#34. Existem jornadas de trabalho extremamente altas?
df["horas_trabalho_semana"].describe()
df.sort_values("horas_trabalho_semana", ascending=False).head(10)
#35. Esses valores necessariamente são erros? Explique.
"Não. Um valor muito alto pode ser um valor verdadeiro. Antes de excluir, é necessário verificar se ele é um erro de preenchimento ou uma observação real."
#36. Quantos possíveis outliers foram encontrados para faltas pelo método do intervalo interquartil?
#37. Qual é o maior número de faltas?
df["faltas"].max()
#38. Um valor identificado como outlier deve ser automaticamente removido? Justifique.













# 36. Quantos possíveis outliers foram encontrados para faltas pelo método do intervalo interquartil?

Q1 = df["faltas"].quantile(0.25)
Q3 = df["faltas"].quantile(0.75)

IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers_faltas = df[
    (df["faltas"] < limite_inferior) |
    (df["faltas"] > limite_superior)
]

outliers_faltas.shape[0]


# 37. Qual é o maior número de faltas?
df["faltas"].max()


# 38. Um valor identificado como outlier deve ser automaticamente removido? Justifique.

"Não. Um outlier não deve ser removido automaticamente, pois ele pode representar uma observação real. Primeiro é necessário analisar se o valor é um erro ou se realmente pertence à base."