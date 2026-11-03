"""
fontes_api.py — conectores para as bases de dados do TCC (terras raras).

PASSO 1 (uma vez):   pip install pandas requests openpyxl
PASSO 2 (testar):    python fontes_api.py testar
PASSO 3 (usar):      python fontes_api.py comexstat --fluxo import --anos 2010 2025 --xlsx imp.xlsx
                     python fontes_api.py comtrade  --reporter 76 --anos 2000 2025 --xlsx comtrade.xlsx
                     python fontes_api.py worldbank --indicador NY.GDP.MKTP.CD --xlsx pib.xlsx
                     python fontes_api.py bcb       --serie 3698 --xlsx dolar.xlsx
                     python fontes_api.py usgs      --xlsx usgs_terras_raras.xlsx

Precisa de Python 3.9 ou mais novo (python --version).

Fontes e o que exigem
    comexstat_ncm        Comex Stat (MDIC), NCM 8 dígitos .......... sem chave (POST)
    comtrade_preview     UN Comtrade, SH6, até 500 linhas/chamada ... sem chave
    comtrade_chave       UN Comtrade com chave gratuita ............. chave em https://comtradedeveloper.un.org/
    worldbank            Banco Mundial WDI ........................... sem chave
    bcb_sgs              Banco Central (câmbio, IPCA, Selic) ......... sem chave
    ibge_sidra           IBGE SIDRA (tabelas) ........................ sem chave
    ipeadata             Ipeadata (séries macro longas) .............. sem chave
    usgs_mcs_csv         USGS Mineral Commodity Summaries (CSV) ...... sem chave (download)
    usgs_ds140_xlsx      USGS Data Series 140 (histórico desde 1900) . sem chave (download)
    fred                 FRED, Fed de St. Louis ...................... chave gratuita
    census_imports_eua   Importações dos EUA por HS .................. chave gratuita
    wits_trade           WITS (Banco Mundial) ........................ sem chave

Se uma chamada der erro 429 (muitas requisições), espere um minuto e repita.
"""
from __future__ import annotations

import argparse
import io
import sys
import time
from pathlib import Path
from typing import List, Optional

if sys.version_info < (3, 9):
    sys.exit("Este script precisa de Python 3.9 ou mais novo. Seu Python: " + sys.version.split()[0])

try:
    import pandas as pd
    import requests
    import openpyxl  # noqa: F401  (usado pelo pandas para salvar .xlsx)
except ModuleNotFoundError as e:
    sys.exit(
        f"Falta instalar um pacote: {e.name}\n"
        "Rode no terminal:  pip install pandas requests openpyxl\n"
        "(se usar .venv no VS Code, ative o ambiente antes)"
    )

PASTA = Path(__file__).resolve().parent / "dados_baixados"
PASTA.mkdir(exist_ok=True)

# Códigos que o TCC usa --------------------------------------------------------
NCM_TERRAS_RARAS = {
    "25309030": "Minérios de terras raras (monazita etc.)",
    "26122000": "Minérios de tório",
    "28053010": "Mischmetal",
    "28053090": "Outros metais de terras raras",
    "28469010": "Óxido de praseodímio",
    "28469090": "Outros compostos de terras raras (inclui carbonato misto)",
    "85051100": "Ímãs permanentes de metal",
}
SH6_TERRAS_RARAS = ["2846", "280530", "850511"]
PAISES_COMTRADE = {"Brasil": 76, "China": 156, "EUA": 842, "Japão": 392, "Austrália": 36, "Mundo": 0}


def _get(url: str, params: Optional[dict] = None, tentativas: int = 4, **kw) -> requests.Response:
    """GET com nova tentativa em 429/5xx."""
    r = None
    for i in range(tentativas):
        r = requests.get(url, params=params, timeout=90, **kw)
        if r.status_code == 200:
            return r
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(15 * (i + 1))
            continue
        r.raise_for_status()
    raise RuntimeError(f"{url}: HTTP {r.status_code if r is not None else '?'} após {tentativas} tentativas")


def _mostrar(df: pd.DataFrame, nome: str) -> pd.DataFrame:
    """Imprime o que veio da API (tamanho, colunas e as primeiras linhas) e devolve a tabela."""
    print(f"\n=== {nome}: {len(df)} linhas x {len(df.columns)} colunas ===")
    if df.empty:
        print("(vazio — a API respondeu, mas sem dados para esse filtro)")
        return df
    print("Colunas:", ", ".join(str(c) for c in df.columns))
    with pd.option_context("display.max_columns", 20, "display.width", 160):
        print(df.head(10).to_string())
    return df


# ------------------------------------------------------------------------------
# 1. Comex Stat (MDIC) — base oficial brasileira, NCM 8 dígitos, mensal desde 1997
#    Documentação: https://api-comexstat.mdic.gov.br/docs
# ------------------------------------------------------------------------------
def comexstat_ncm(ncms: List[str], fluxo: str, ano_ini: int, ano_fim: int,
                  detalhes: List[str] = ("country",), mensal: bool = False) -> pd.DataFrame:
    """fluxo = 'export' | 'import'. detalhes: 'country', 'state', 'ncm', 'economicBlock'...
    Métricas: US$ FOB e kg líquido (na importação também CIF)."""
    url = "https://api-comexstat.mdic.gov.br/general"
    metricas = ["metricFOB", "metricKG"]
    if fluxo == "import":
        metricas.append("metricCIF")
    corpo = {
        "flow": fluxo,
        "monthDetail": mensal,
        "period": {"from": f"{ano_ini}-01", "to": f"{ano_fim}-12"},
        "filters": [{"filter": "ncm", "values": list(ncms)}],
        "details": list(detalhes) + ["ncm"],
        "metrics": metricas,
    }
    r = requests.post(url, json=corpo, timeout=180)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["data"]["list"])
    df["fluxo"] = fluxo
    return _mostrar(df, f"Comex Stat {fluxo} {ano_ini}-{ano_fim}")


def comexstat_tabela_ncm(busca: str = "terras raras") -> pd.DataFrame:
    """Procura códigos NCM pela descrição (para conferir os códigos acima)."""
    r = _get("https://api-comexstat.mdic.gov.br/tables/ncm")
    df = pd.DataFrame(r.json()["data"]["list"])
    col = [c for c in df.columns if "text" in c.lower() or "desc" in c.lower()][0]
    return _mostrar(df[df[col].str.contains(busca, case=False, na=False)], f"Comex Stat tabela NCM '{busca}'")


# ------------------------------------------------------------------------------
# 2. UN Comtrade
# ------------------------------------------------------------------------------
def comtrade_preview(reporter: int, ano: int, codigos: List[str] = SH6_TERRAS_RARAS,
                     parceiro: int = 0, fluxos: str = "M,X") -> pd.DataFrame:
    """Sem chave. Um ano por chamada; parceiro 0 = Mundo. Filtra motCode 0 (todos os modais)."""
    url = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
    params = {"reporterCode": reporter, "period": ano, "partnerCode": parceiro,
              "cmdCode": ",".join(codigos), "flowCode": fluxos, "motCode": 0}
    r = _get(url, params)
    df = pd.DataFrame(r.json().get("data", []))
    if df.empty:
        return df
    df = df[df["motCode"].astype(str) == "0"]
    return _mostrar(df[["period", "reporterCode", "partnerCode", "flowCode", "cmdCode", "primaryValue", "netWgt"]], f"Comtrade reporter {reporter} {ano}")


def comtrade_serie(reporter: int, ano_ini: int, ano_fim: int, codigos: List[str] = SH6_TERRAS_RARAS) -> pd.DataFrame:
    """Vários anos pelo preview (uma chamada por ano, com pausa)."""
    partes = []
    for ano in range(ano_ini, ano_fim + 1):
        print(f"  Comtrade {reporter} {ano}...", file=sys.stderr)
        partes.append(comtrade_preview(reporter, ano, codigos))
        time.sleep(2)
    return _mostrar(pd.concat([p for p in partes if not p.empty], ignore_index=True), f"Comtrade reporter {reporter} {ano_ini}-{ano_fim}")


def comtrade_chave(chave: str, reporter: int, periodos: str, codigos: List[str] = SH6_TERRAS_RARAS,
                   parceiro: Optional[int] = None, fluxos: str = "M,X", freq: str = "A") -> pd.DataFrame:
    """Com chave gratuita (comtradedeveloper.un.org). periodos = '2010,2011,...' (freq 'A' anual, 'M' mensal).
    parceiro None = todos os parceiros (para ver a composição por país)."""
    url = f"https://comtradeapi.un.org/data/v1/get/C/{freq}/HS"
    params = {"reporterCode": reporter, "period": periodos, "cmdCode": ",".join(codigos),
              "flowCode": fluxos, "motCode": 0, "subscription-key": chave}
    if parceiro is not None:
        params["partnerCode"] = parceiro
    r = _get(url, params)
    return _mostrar(pd.DataFrame(r.json().get("data", [])), f"Comtrade (chave) reporter {reporter} {periodos}")


# ------------------------------------------------------------------------------
# 3. Banco Mundial — WDI. Indicadores úteis: NY.GDP.MKTP.CD (PIB US$),
#    NY.GDP.MINR.RT.ZS (rendas minerais % PIB), TX.VAL.MRCH.CD.WT (exportações de bens US$),
#    NV.IND.MANF.ZS (manufatura % PIB)
# ------------------------------------------------------------------------------
def worldbank(indicador: str, paises: str = "BRA;CHN;USA;AUS", ano_ini: int = 2000, ano_fim: int = 2025) -> pd.DataFrame:
    url = f"https://api.worldbank.org/v2/country/{paises}/indicator/{indicador}"
    r = _get(url, {"format": "json", "date": f"{ano_ini}:{ano_fim}", "per_page": 2000})
    dados = r.json()[1] or []
    return _mostrar(pd.DataFrame([{"pais": d["country"]["value"], "iso3": d["countryiso3code"],
                                   "ano": int(d["date"]), "valor": d["value"]} for d in dados]), f"Banco Mundial {indicador}")


# ------------------------------------------------------------------------------
# 4. Banco Central — SGS (3698 = dólar médio mensal; 1 = dólar diário; 433 = IPCA; 432 = Selic meta)
# ------------------------------------------------------------------------------
def bcb_sgs(serie: int, ini: str = "01/01/2000", fim: str = "31/12/2025") -> pd.DataFrame:
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados"
    r = _get(url, {"formato": "json", "dataInicial": ini, "dataFinal": fim})
    df = pd.DataFrame(r.json())
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df["valor"] = pd.to_numeric(df["valor"])
    return _mostrar(df, f"Banco Central SGS {serie}")


# ------------------------------------------------------------------------------
# 5. IBGE — SIDRA. Monte o caminho no site (https://sidra.ibge.gov.br -> botão "API" da tabela).
# ------------------------------------------------------------------------------
def ibge_sidra(caminho: str) -> pd.DataFrame:
    """caminho = o que vem depois de /values/, ex.: 't/6612/n1/all/v/9319/p/last 1'."""
    r = _get("https://apisidra.ibge.gov.br/values/" + caminho)
    dados = r.json()
    df = pd.DataFrame(dados[1:])
    df.columns = [dados[0][c] for c in df.columns]
    return _mostrar(df, f"IBGE SIDRA {caminho}")


# ------------------------------------------------------------------------------
# 6. Ipeadata — séries macro longas. Código da série no site do Ipeadata.
# ------------------------------------------------------------------------------
def ipeadata(sercodigo: str) -> pd.DataFrame:
    url = f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{sercodigo}')"
    r = _get(url)
    df = pd.DataFrame(r.json()["value"])
    df["VALDATA"] = pd.to_datetime(df["VALDATA"], utc=True).dt.date
    return _mostrar(df[["VALDATA", "VALVALOR"]].rename(columns={"VALDATA": "data", "VALVALOR": "valor"}), f"Ipeadata {sercodigo}")


def ipeadata_buscar(texto: str) -> pd.DataFrame:
    r = _get("http://www.ipeadata.gov.br/api/odata4/Metadados")
    df = pd.DataFrame(r.json()["value"])
    return _mostrar(df[df["SERNOME"].str.contains(texto, case=False, na=False)][["SERCODIGO", "SERNOME", "PERNOME", "UNINOME"]], f"Ipeadata busca '{texto}'")


# ------------------------------------------------------------------------------
# 7. USGS — Mineral Commodity Summaries 2026, data release (CSV no ScienceBase)
#    Item: https://www.sciencebase.gov/catalog/item/696a75d5d4be0228872d3bf8   DOI 10.5066/P1WKQ63T
# ------------------------------------------------------------------------------
USGS_MCS_ITEM = "696a75d5d4be0228872d3bf8"


def usgs_mcs_csv(arquivo: str = "MCS2026_Commodities_Data.csv", filtro: Optional[str] = "rare earth") -> pd.DataFrame:
    """Baixa o CSV do ScienceBase (salva em dados_baixados/) e filtra linhas que contenham o texto."""
    url = f"https://www.sciencebase.gov/catalog/file/get/{USGS_MCS_ITEM}"
    r = _get(url, {"name": arquivo}, headers={"User-Agent": "Mozilla/5.0"})
    (PASTA / arquivo).write_bytes(r.content)
    df = pd.read_csv(io.BytesIO(r.content), low_memory=False)
    if filtro:
        mask = df.astype(str).apply(lambda col: col.str.contains(filtro, case=False, na=False)).any(axis=1)
        df = df[mask]
    return _mostrar(df, f"USGS {arquivo} (filtro: {filtro})")


# ------------------------------------------------------------------------------
# 8. USGS — Data Series 140 (histórico desde 1900, inclui valor unitário)
#    Página: https://www.usgs.gov/centers/national-minerals-information-center/historical-statistics-mineral-and-material-commodities
#    O link do XLSX de terras raras muda de edição; copie da página e passe em `url`.
# ------------------------------------------------------------------------------
def usgs_ds140_xlsx(url: str, aba=0) -> pd.DataFrame:
    r = _get(url, headers={"User-Agent": "Mozilla/5.0"})
    (PASTA / url.split("/")[-1].split("?")[0]).write_bytes(r.content)
    return _mostrar(pd.read_excel(io.BytesIO(r.content), sheet_name=aba, header=None), "USGS DS140")


# ------------------------------------------------------------------------------
# 9. FRED — Fed de St. Louis (chave gratuita em https://fred.stlouisfed.org/docs/api/api_key.html)
#    Ex.: CPIAUCSL (inflação EUA, para deflacionar preços em US$), DEXBZUS (câmbio BRL/USD)
# ------------------------------------------------------------------------------
def fred(serie: str, chave: str, ini: str = "2000-01-01") -> pd.DataFrame:
    url = "https://api.stlouisfed.org/fred/series/observations"
    r = _get(url, {"series_id": serie, "api_key": chave, "file_type": "json", "observation_start": ini})
    df = pd.DataFrame(r.json()["observations"])[["date", "value"]]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return _mostrar(df, f"FRED {serie}")


# ------------------------------------------------------------------------------
# 10. US Census — importações dos EUA por HS (chave gratuita em https://api.census.gov/data/key_signup.html)
# ------------------------------------------------------------------------------
def census_imports_eua(hs: str, periodo: str, chave: str) -> pd.DataFrame:
    """hs = '2846' (4 a 10 dígitos); periodo = '2025-06'."""
    url = "https://api.census.gov/data/timeseries/intltrade/imports/hs"
    r = _get(url, {"get": "CTY_CODE,CTY_NAME,GEN_VAL_MO,GEN_QY1_MO,UNIT_QY1", "I_COMMODITY": hs,
                   "time": periodo, "key": chave})
    dados = r.json()
    return _mostrar(pd.DataFrame(dados[1:], columns=dados[0]), f"US Census importações HS {hs} {periodo}")


# ------------------------------------------------------------------------------
# 11. WITS (Banco Mundial) — Comtrade reformatado + tarifas, sem chave
#     Indicadores: MPRT-TRD-VL (importação US$ mil), XPRT-TRD-VL (exportação US$ mil)
# ------------------------------------------------------------------------------
def wits_trade(reporter: str = "bra", ano: int = 2023, parceiro: str = "wld", produto: str = "2846",
               indicador: str = "XPRT-TRD-VL") -> pd.DataFrame:
    url = (f"https://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-trade/reporter/{reporter}"
           f"/year/{ano}/partner/{parceiro}/product/{produto}/indicator/{indicador}")
    r = _get(url, {"format": "JSON"})
    return _mostrar(pd.json_normalize(r.json()), f"WITS {reporter} {produto} {ano}")


# ------------------------------------------------------------------------------
# Linha de comando
# ------------------------------------------------------------------------------
def testar():
    testes = [
        ("Comex Stat (anos disponíveis)", lambda: _get("https://api-comexstat.mdic.gov.br/general/dates/years").json()),
        ("Comex Stat POST (NCM 85051100, importação 2024)", lambda: comexstat_ncm(["85051100"], "import", 2024, 2024).head(3)),
        ("UN Comtrade preview (Brasil 2024)", lambda: comtrade_preview(76, 2024).head(3)),
        ("Banco Mundial (PIB Brasil)", lambda: worldbank("NY.GDP.MKTP.CD", "BRA", 2022, 2024)),
        ("Banco Central (dólar mensal 3698)", lambda: bcb_sgs(3698, "01/01/2025", "01/03/2025")),
        ("IBGE SIDRA (PIB trimestral)", lambda: ibge_sidra("t/6612/n1/all/v/9319/p/last 1").head(2)),
        ("Ipeadata (busca 'câmbio')", lambda: ipeadata_buscar("câmbio").head(3)),
        ("USGS MCS CSV (linhas de rare earth)", lambda: usgs_mcs_csv().head(3)),
        ("WITS (Brasil exportação 2846, 2023)", lambda: wits_trade().head(2)),
    ]
    ok = 0
    for nome, fn in testes:
        try:
            res = fn()
            ok += 1
            print(f"OK   {nome}\n")
        except Exception as e:  # noqa: BLE001
            print(f"ERRO {nome}: {type(e).__name__}: {str(e)[:200]}\n")
    print(f"{ok} de {len(testes)} fontes responderam.")


def _salvar(df: pd.DataFrame, xlsx: Optional[str]):
    if xlsx:
        df.to_excel(xlsx, index=False)
        print(f"\nSalvo em: {xlsx}  ({len(df)} linhas)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("testar", help="testa todas as fontes sem chave")

    p = sub.add_parser("comexstat", help="Comex Stat por NCM (padrão: os 7 NCM de terras raras)")
    p.add_argument("--ncm", nargs="+", default=list(NCM_TERRAS_RARAS))
    p.add_argument("--fluxo", choices=["import", "export"], default="export")
    p.add_argument("--anos", nargs=2, type=int, default=[2010, 2025], metavar=("INI", "FIM"))
    p.add_argument("--mensal", action="store_true")
    p.add_argument("--xlsx")

    p = sub.add_parser("comtrade", help="UN Comtrade (preview, sem chave), vários anos")
    p.add_argument("--reporter", type=int, default=76, help="76 Brasil, 156 China, 842 EUA, 392 Japão, 36 Austrália")
    p.add_argument("--anos", nargs=2, type=int, default=[2000, 2025], metavar=("INI", "FIM"))
    p.add_argument("--codigos", nargs="+", default=SH6_TERRAS_RARAS)
    p.add_argument("--xlsx")

    p = sub.add_parser("worldbank", help="Banco Mundial WDI")
    p.add_argument("--indicador", default="NY.GDP.MKTP.CD")
    p.add_argument("--paises", default="BRA;CHN;USA;AUS")
    p.add_argument("--anos", nargs=2, type=int, default=[2000, 2025], metavar=("INI", "FIM"))
    p.add_argument("--xlsx")

    p = sub.add_parser("bcb", help="Banco Central SGS")
    p.add_argument("--serie", type=int, default=3698)
    p.add_argument("--ini", default="01/01/2000")
    p.add_argument("--fim", default="31/12/2025")
    p.add_argument("--xlsx")

    p = sub.add_parser("usgs", help="USGS MCS 2026 (CSV do ScienceBase), filtrado por texto")
    p.add_argument("--arquivo", default="MCS2026_Commodities_Data.csv")
    p.add_argument("--filtro", default="rare earth")
    p.add_argument("--xlsx")

    args = ap.parse_args()
    if args.cmd in (None, "testar"):
        testar()
    elif args.cmd == "comexstat":
        _salvar(comexstat_ncm(args.ncm, args.fluxo, args.anos[0], args.anos[1], mensal=args.mensal), args.xlsx)
    elif args.cmd == "comtrade":
        _salvar(comtrade_serie(args.reporter, args.anos[0], args.anos[1], args.codigos), args.xlsx)
    elif args.cmd == "worldbank":
        _salvar(worldbank(args.indicador, args.paises, args.anos[0], args.anos[1]), args.xlsx)
    elif args.cmd == "bcb":
        _salvar(bcb_sgs(args.serie, args.ini, args.fim), args.xlsx)
    elif args.cmd == "usgs":
        _salvar(usgs_mcs_csv(args.arquivo, args.filtro), args.xlsx)


if __name__ == "__main__":
    main()






# puxar_dados.py
# Só puxa os dados das APIs e mostra o que veio de cada uma:
# quantas linhas, quantas colunas, nomes das colunas e as primeiras linhas.
# No fim salva tudo em dados_apis.xlsx (uma aba por fonte + uma aba "resumo").
#
# Antes de rodar:  pip install pandas requests openpyxl

import requests        # chamar as APIs
import pandas as pd    # tabelas
import time            # pausa entre chamadas
import io              # ler o CSV do USGS que vem pela internet

ANO_INI = 2010
ANO_FIM = 2025

# NCM (8 dígitos) de terras raras — Comex Stat
NCM = ["25309030", "26122000", "28053010", "28053090", "28469010", "28469090", "85051100"]
# SH (6 dígitos) — UN Comtrade
SH6 = "2846,280530,850511"

tabelas = {}   # nome da fonte -> tabela
resumo = []    # linhas da aba "resumo"


def mostrar(nome, tabela):
    """Imprime o que veio e guarda para salvar depois."""
    print(f"\n===== {nome}: {len(tabela)} linhas x {len(tabela.columns)} colunas =====")
    print("Colunas:", list(tabela.columns))
    print(tabela.head(8).to_string())
    tabelas[nome] = tabela
    resumo.append({"fonte": nome, "linhas": len(tabela), "colunas": len(tabela.columns), "status": "OK"})


def falhou(nome, erro):
    print(f"\n===== {nome}: ERRO -> {type(erro).__name__}: {str(erro)[:150]}")
    resumo.append({"fonte": nome, "linhas": 0, "colunas": 0, "status": f"ERRO {type(erro).__name__}"})


# ---------------------------------------------------------- 1. Comex Stat (MDIC) — exportação e importação por NCM e país
def comexstat(fluxo):
    corpo = {
        "flow": fluxo,
        "monthDetail": False,
        "period": {"from": f"{ANO_INI}-01", "to": f"{ANO_FIM}-12"},
        "filters": [{"filter": "ncm", "values": NCM}],
        "details": ["country", "ncm"],
        "metrics": ["metricFOB", "metricKG"],
    }
    r = requests.post("https://api-comexstat.mdic.gov.br/general", json=corpo, timeout=180)
    r.raise_for_status()
    return pd.DataFrame(r.json()["data"]["list"])


for fluxo in ["export", "import"]:
    try:
        mostrar(f"comexstat_{fluxo}", comexstat(fluxo))
    except Exception as e:
        falhou(f"comexstat_{fluxo}", e)


# ---------------------------------------------------------- 2. UN Comtrade — Brasil e China, um ano por chamada
def comtrade(reporter, ano, fluxo):
    params = {"reporterCode": reporter, "period": ano, "partnerCode": 0,
              "cmdCode": SH6, "flowCode": fluxo, "motCode": 0}
    r = requests.get("https://comtradeapi.un.org/public/v1/preview/C/A/HS", params=params, timeout=90)
    r.raise_for_status()
    t = pd.DataFrame(r.json()["data"])
    if len(t):
        t = t[t["motCode"].astype(str) == "0"]
        t = t[["period", "reporterCode", "flowCode", "cmdCode", "primaryValue", "netWgt"]]
    return t


for nome, reporter, fluxo in [("comtrade_brasil", 76, "M,X"), ("comtrade_china_exporta", 156, "X")]:
    try:
        partes = []
        for ano in range(ANO_INI, ANO_FIM + 1):
            print(f"{nome} {ano}...")
            partes.append(comtrade(reporter, ano, fluxo))
            time.sleep(2)
        mostrar(nome, pd.concat(partes, ignore_index=True))
    except Exception as e:
        falhou(nome, e)


# ---------------------------------------------------------- 3. Banco Mundial — PIB e rendas minerais (% PIB)
def worldbank(indicador):
    url = f"https://api.worldbank.org/v2/country/BRA;CHN;USA;AUS/indicator/{indicador}"
    r = requests.get(url, params={"format": "json", "date": f"{ANO_INI}:{ANO_FIM}", "per_page": 1000}, timeout=90)
    r.raise_for_status()
    dados = r.json()[1]
    return pd.DataFrame([{"pais": d["country"]["value"], "ano": int(d["date"]), "valor": d["value"]} for d in dados])


for nome, ind in [("worldbank_pib_usd", "NY.GDP.MKTP.CD"), ("worldbank_rendas_minerais_pct_pib", "NY.GDP.MINR.RT.ZS")]:
    try:
        mostrar(nome, worldbank(ind))
    except Exception as e:
        falhou(nome, e)


# ---------------------------------------------------------- 4. Banco Central — dólar médio mensal (série 3698)
try:
    r = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.3698/dados",
                     params={"formato": "json", "dataInicial": f"01/01/{ANO_INI}", "dataFinal": f"31/12/{ANO_FIM}"}, timeout=90)
    r.raise_for_status()
    mostrar("bcb_dolar_mensal", pd.DataFrame(r.json()))
except Exception as e:
    falhou("bcb_dolar_mensal", e)


# ---------------------------------------------------------- 5. USGS — Mineral Commodity Summaries 2026 (CSV), só linhas de terras raras
try:
    r = requests.get("https://www.sciencebase.gov/catalog/file/get/696a75d5d4be0228872d3bf8",
                     params={"name": "MCS2026_Commodities_Data.csv"}, headers={"User-Agent": "Mozilla/5.0"}, timeout=180)
    r.raise_for_status()
    usgs = pd.read_csv(io.BytesIO(r.content), low_memory=False)
    print(f"\nUSGS arquivo completo: {len(usgs)} linhas x {len(usgs.columns)} colunas")
    so_tr = usgs[usgs.astype(str).apply(lambda col: col.str.contains("rare earth", case=False, na=False)).any(axis=1)]
    mostrar("usgs_terras_raras", so_tr)
except Exception as e:
    falhou("usgs_terras_raras", e)


# ---------------------------------------------------------- salva tudo
with pd.ExcelWriter("dados_apis.xlsx") as xw:
    pd.DataFrame(resumo).to_excel(xw, sheet_name="resumo", index=False)
    for nome, t in tabelas.items():
        t.to_excel(xw, sheet_name=nome[:31], index=False)

print("\n===== RESUMO =====")
print(pd.DataFrame(resumo).to_string(index=False))
print("\nSalvo: dados_apis.xlsx")