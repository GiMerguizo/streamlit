# importar as bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt

#  criar as funções de carregamento de dados
## Cotações do ITAU - ITUB4 - 2010 a 2024

@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-07-01")
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao

@st.cache_data
def carregar_tickers_acoes():
    base_tickers = pd.read_csv("IBOV.csv", sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers

acoes = carregar_tickers_acoes()
dados = carregar_dados(acoes)

# Criar a interface do streamlit
st.write("""
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações ao longo dos anos.
""") # markdown

# Preparar as visualizações (filtros)
st.sidebar.header("Filtros")

## Filtro de acoes
lista_acoes = st.sidebar.multiselect("Escolha as ações para visualizar", dados.columns)

if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

## Filtro de datas
data_incial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_data = st.sidebar.slider("Selecione o período", min_value=data_incial, max_value=data_final, 
                                    value=(data_incial, data_final),  step=dt.timedelta(days=1))

dados = dados.loc[intervalo_data[0]:intervalo_data[1]]

## Criar o gráfico
st.line_chart(dados) # gráfico de linha

texto_performance_ativos = ""

if len(lista_acoes)==0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes)==1:
    dados = dados.rename(columns={acao_unica: "Close"})

for acao in lista_acoes:
    # performance_ativos = VALOR_FINAL / VALOR_INICIAL - 1
    performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_ativo = float(performance_ativo)
    texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: {performance_ativo:.1f}%"

st.write("""
### Performance dos Ativos
Essa foi a performance de cada ativo no período selecionado:

{texto_performance_ativos}
""") # markdown
