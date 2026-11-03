"""
Disciplina: Programacao para Analise de Dados
Aluno: Danilo Sodre Barcelos - Matricula 202308875965

Terras raras: quanto o Brasil recebe pelo minerio que exporta e quanto esse
mesmo minerio valeria se fosse refinado. Periodo 2021 a 2025.

DE ONDE VEM CADA DADO
 - API UN Comtrade (Nacoes Unidas): valor em US$ e peso em kg das exportacoes
   https://comtradeapi.un.org/public/v1/preview/C/A/HS
 - dados_terras_raras.xlsx: preco do oxido refinado (USGS) e composicao do
   minerio da Serra Verde. O link da fonte esta dentro da propria planilha.

O arquivo dados_terras_raras.xlsx precisa estar na mesma pasta.
pip install pandas requests openpyxl matplotlib
"""

import os
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.width", 200)
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

print("Pasta onde o codigo esta rodando:", os.getcwd())
print("Arquivos nessa pasta:", os.listdir())


# 1) API - EXPORTACAO BRASILEIRA DE COMPOSTOS DE TERRAS RARAS (SH 2846)

url = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
ANO_INICIAL = 2021
ANO_FINAL = 2025

linhas = []
for ano in range(ANO_INICIAL, ANO_FINAL + 1):
    print("baixando", ano)
    params = {"reporterCode": 76, "period": ano, "partnerCode": 0,
              "cmdCode": "2846", "flowCode": "X", "motCode": 0}
    resp = requests.get(url, params=params, timeout=180)
    dados = resp.json().get("data", [])
    print("  status", resp.status_code, "- linhas recebidas:", len(dados))
    linhas = linhas + dados
    time.sleep(2)

exporta = pd.DataFrame(linhas)
print(exporta.shape)
print(exporta.columns)

col_api = ["period", "primaryValue", "netWgt"]
exporta = exporta[col_api]
exporta.columns = ["ano", "exportado_usd", "exportado_kg"]
exporta.info()
print(exporta.isnull().sum())
print("linhas repetidas:", exporta.duplicated().sum())

exporta = exporta.dropna()
exporta = exporta[exporta["exportado_kg"] > 0]
exporta["ano"] = exporta["ano"].astype(int)
exporta = exporta.sort_values(by="ano")
exporta["toneladas"] = exporta["exportado_kg"] / 1000
print(exporta)
print("anos com dado:", exporta["ano"].unique())


# 2) PLANILHA - PRECO DO OXIDO REFINADO E COMPOSICAO DO MINERIO

precos = pd.read_excel("dados_terras_raras.xlsx", sheet_name="precos")
print(precos.shape)
print(precos.head())
precos.info()
print(precos.isnull().sum())
print("elementos na planilha:", precos["elemento"].unique())
print("fonte do preco:", precos["fonte_preco"].unique())
print("os links completos estao na aba fontes da planilha")


# 3) MERGE - JUNTA A API COM A PLANILHA PELO ANO

tabela = pd.merge(precos, exporta, on="ano")
print(tabela.shape)

tabela["kg_do_elemento"] = tabela["exportado_kg"] * tabela["pct_no_minerio"] / 100
tabela["recebido_usd"] = tabela["exportado_usd"] * tabela["pct_no_minerio"] / 100
tabela["refinado_usd"] = tabela["kg_do_elemento"] * tabela["oxido_usd_kg"]
tabela["diferenca_usd"] = tabela["refinado_usd"] - tabela["recebido_usd"]

col_final = ["elemento", "ano", "kg_do_elemento", "oxido_usd_kg",
             "recebido_usd", "refinado_usd", "diferenca_usd"]
final = tabela[col_final].round(2).sort_values(by=["elemento", "ano"])
print("TABELA ANO A ANO")
print(final.to_string(index=False))


# 4) RESULTADO POR COMPONENTE

componente = tabela.groupby("elemento").agg(
    kg_exportado=("kg_do_elemento", "sum"),
    recebido_usd=("recebido_usd", "sum"),
    refinado_usd=("refinado_usd", "sum"),
    diferenca_usd=("diferenca_usd", "sum")).reset_index()
componente["vezes_mais_caro"] = componente["refinado_usd"] / componente["recebido_usd"]
componente = componente.round(2).sort_values(by="diferenca_usd", ascending=False)
print("RESULTADO POR COMPONENTE (2021 a 2025, em US$)")
print(componente.to_string(index=False))
print(componente.describe())
print("TOTAL DEIXADO NA MESA (US$):", round(componente["diferenca_usd"].sum(), 2))


# 5) RESULTADO POR ANO

por_ano = tabela.groupby("ano").agg(
    recebido_usd=("recebido_usd", "sum"),
    refinado_usd=("refinado_usd", "sum"),
    diferenca_usd=("diferenca_usd", "sum")).reset_index()
por_ano = pd.merge(por_ano, exporta[["ano", "exportado_usd"]], on="ano")
por_ano["pct_da_receita_coberta"] = por_ano["recebido_usd"] / por_ano["exportado_usd"] * 100
por_ano = por_ano.round(2)
print("RESULTADO POR ANO (US$)")
print(por_ano.to_string(index=False))
print("atencao: recebido_usd e so a parte da receita atribuida aos 9 elementos com preco,")
print("por isso e menor que exportado_usd, que e o total que o Brasil faturou no ano")

cobertura = tabela.groupby("ano").agg(pct_do_minerio_coberto=("pct_no_minerio", "sum")).reset_index()
cobertura = cobertura.round(2)
print("QUANTO DO MINERIO A ANALISE CONSEGUE PRECIFICAR EM CADA ANO (%)")
print(cobertura.to_string(index=False))

print("2022 nao aparece: o Comtrade registra US$ 16.328 com peso liquido zero")
print("disprosio e terbio nao tem preco em 2025: o USGS parou de publicar")
print("itrio, erbio, iterbio, holmio, tulio e lutecio sao 19,6% do minerio e o USGS nunca publica preco")
print("o peso usado e o peso bruto do carbonato, nao o teor de TREO contido")


# 6) GRAFICOS

por_ano["recebido_milhoes"] = por_ano["recebido_usd"] / 1000000
por_ano["refinado_milhoes"] = por_ano["refinado_usd"] / 1000000

exporta.plot(x="ano", y="toneladas", kind="bar",
             title="Brasil: toneladas de terras raras exportadas")
por_ano.plot(x="ano", y=["recebido_milhoes", "refinado_milhoes"], kind="bar",
             title="Brasil: o que recebeu x o que valeria refinado (US$ milhoes)")
plt.show()


# 7) EXCEL DE SAIDA

arquivo = pd.ExcelWriter("resultado_terras_raras.xlsx")
componente.to_excel(arquivo, sheet_name="por_componente", index=False)
por_ano.to_excel(arquivo, sheet_name="por_ano", index=False)
final.to_excel(arquivo, sheet_name="ano_a_ano", index=False)
cobertura.to_excel(arquivo, sheet_name="cobertura", index=False)
exporta.to_excel(arquivo, sheet_name="api_comtrade", index=False)
arquivo.close()
print("Salvo: resultado_terras_raras.xlsx")