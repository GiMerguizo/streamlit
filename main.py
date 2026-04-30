# importar as bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf

#  criar as funções de carregamento de dados
## Cotações do ITAU - ITUB4 - 2010 a 2024

@st.cache_data
def carregar_dados(empresa):
    dados_acao = yf.Ticker(empresa)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-07-01")
    cotacoes_acao = cotacoes_acao[["Close"]]
    return cotacoes_acao


dados = carregar_dados("ITUB4.SA")
print(dados)

# Preparar as visualizações

# Criar a interface do streamlit
st.write("""
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações do Itaú (ITUB4) ao longo dos anos.
""") # markdown

## Criar o gráfico
st.line_chart(dados) # gráfico de linha
