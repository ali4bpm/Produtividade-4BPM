import streamlit as st
import pandas as pd
import numpy as np
import gspread
import openpyxl
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch

# Configurando a página
st.set_page_config(layout='wide')

# Configurar credenciais
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
client = gspread.authorize(creds)

# Mover o dicionário de tradução dos meses para antes da função carregar_dados
meses = {'January':'Janeiro', 'February':'Fevereiro', 'March': 'Março',
         'April': 'Abril', 'May': 'Maio', 'June': 'Junho', 'July': 'Julho',
         'August': 'Agosto', 'September': 'Setembro', 'October': 'Outubro',
         'November': 'Novembro', 'December': 'Dezembro'}

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    # Acessar a planilha
    planilha = client.open_by_key('1PLZZMSrp19FFvVIAOhZTVnRh7Tk7EQLoROZy4OaBCDg')
    # Acessar a aba da Planilha
    aba = planilha.worksheet('Sheet_Pontuacao')

    # Acessar os dados da planilha
    dados = aba.get_all_values()

    # Convertendo em DataFrame do pandas      
    df = pd.DataFrame(dados)  
    # Retirando a primeira linha do df
    dfTratado = pd.DataFrame(dados[1:], columns=dados[0])
    df = dfTratado
    
    # Converter DATA para datetime e criar colunas derivadas
    df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce')
    df['ANO'] = df['DATA'].dt.year.astype(str)
    df['MÊS'] = df['DATA'].dt.strftime('%B').map(meses)
    df['QTDE'] = pd.to_numeric(df['QTDE'], errors='coerce')  # Converter QTDE para número
    df['PONTOS'] = pd.to_numeric(df['PONTOS'], errors='coerce')  # Converter PONTOS para número
    # Somente após todas as operações .dt, converter DATA para string
    df['DATA'] = df['DATA'].dt.strftime('%d/%m/%Y')
    
    return df
      
df = carregar_dados()

# Importar o módulo de ranking
from ranking import criar_ranking

# Título do aplicativo
st.title("PRODUTIVIDADE E PONTUAÇÃO")

# Texto na página
st.write("Produtividade - 4º BPM RN")

# Sidebar com filtros
st.sidebar.image("brasao.jpg", use_column_width=True)
st.sidebar.subheader("FILTROS")

# Filtros corrigidos
anos_disponiveis = sorted(df['ANO'].dropna().unique())
meses_ordem_correta = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                      'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
meses_disponiveis = [mes for mes in meses_ordem_correta if mes in df['MÊS'].unique()]

# Novos filtros para COMPANHIA, EFETIVO e TIPO_OC
companhias_disponiveis = sorted(df['COMPANHIA'].dropna().unique())
efetivos_disponiveis = sorted(df['EFETIVO'].dropna().unique())
tipos_oc_disponiveis = sorted(df['TIPO_OC'].dropna().unique())

# Filtros na sidebar
anos = st.sidebar.multiselect('Ano', options=anos_disponiveis, placeholder='Selecione o Ano')
meses_selecionados = st.sidebar.multiselect('Mês', options=meses_disponiveis, placeholder='Selecione o Mês')
companhias = st.sidebar.multiselect('Companhia', options=companhias_disponiveis, placeholder='Selecione a Companhia')
efetivos = st.sidebar.multiselect('Efetivo', options=efetivos_disponiveis, placeholder='Selecione o Efetivo')
tipos_oc = st.sidebar.multiselect('Tipo de Ocorrência', options=tipos_oc_disponiveis,placeholder='Selecione a Ocorrência')

# Aplicando filtros diretamente no df
if anos:
    df = df[df['ANO'].isin(anos)]
if meses_selecionados:
    df = df[df['MÊS'].isin(meses_selecionados)]
if companhias:
    df = df[df['COMPANHIA'].isin(companhias)]
if efetivos:
    df = df[df['EFETIVO'].isin(efetivos)]
if tipos_oc:
    df = df[df['TIPO_OC'].isin(tipos_oc)]

# Criar expander para mostrar os dados
with st.expander("Sobre o Aplicativo:"):
    st.write("""Este aplicativo foi desenvolvido para mostrar a produtividade e pontuação do efetivo do 4º BPM PMRN, baseado nas Categorias, Critérios e Pontos elencados abaixo:""")
    st.write("ARMA BRANCA: 05 pontos")
    st.write("ARTESANAL CURTA: 20 pontos")
    st.write("ARTESANAL LONGA: 25 pontos")
    st.write("COLETE BALÍSTICO: 20 pontos")
    st.write("ESPINGARDA: 35 pontos")
    st.write("METRALHADORA: 40 pontos")
    st.write("FUZIL: 50 pontos")
    st.write("PISTOLA: 30 pontos")
    st.write("REVÓLVER: 25 pontos")
    st.write("RIFLE: 35 pontos")
    st.write("SIMULACRO: 06 pontos")
    st.write("ENTORPECENTE De 1g a 500g - Peso 1 (Duas ou mais Ocorrências no mesmo dia até o total contará como pontuação subsequente): 15 pontos")
    st.write("ENTORPECENTE De 500g a 2kg - Peso 2 (Duas ou mais Ocorrências no mesmo dia até o total contará como pontuação subsequente): 20 pontos")
    st.write("ENTORPECENTE De 2g a 10kg - Peso 3 (Duas ou mais Ocorrências no mesmo dia até o total contará como pontuação subsequente): 30 pontos")
    st.write("ENTORPECENTE Acima de 10kg - Peso 4: 50 pontos")
    st.write("ARROMBAMENTO: 06 pontos")
    st.write("ESTELIONATO: 07 pontos")
    st.write("FURTO: 06 pontos")
    st.write("RECEPTAÇÃO: 08 pontos")
    st.write("ROUBO: 12 pontos")
    st.write("MUNIÇÃO 1 - 10: 02 pontos")
    st.write("MUNIÇÃO 11 - 20: 04 pontos")
    st.write("MUNIÇÃO 21 - 50: 08 pontos")
    st.write("MUNIÇÃO 51 - 100: 14 pontos")
    st.write("MUNIÇÃO 101 ou mais: 24 pontos")
    st.write("FORAGIDO: 10 pontos")
    st.write("VEÍCULO ABANDONADO: 06 pontos")
    st.write("VEÍCULO (FURTO/ROUBO) APREENDIDO: 07 pontos")
    st.write("TCO/BOC 4º BPM: 06 pontos")
    st.write("TCO/BOC DELEGACIA: 03 pontos")
    st.write("BOPM: 03 pontos")
    st.write("VIOLÊNCIA DOMÉSTICA: 05 pontos")
    st.write("ESTUPRO COM FLAGRANTE: 30 pontos")
    st.write("HOMICÍDIO COM PRISÃO: 50 pontos")
    
# Função para criar PDF
def create_pdf(df):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    
    # Converter DataFrame para lista
    data = [df.columns.tolist()] + df.values.tolist()
    
    # Criar tabela
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

try:
    # Mostrar DataFrame
    st.dataframe(df, use_container_width=True)
    
    # Criar botão de download
    pdf = create_pdf(df)
    st.download_button(
        label="📥 Baixar Relatório em PDF",
        data=pdf,
        file_name="produtividade.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
except Exception as e:
    st.error("Erro ao gerar PDF. Por favor, tente novamente.")

st.divider()
st.subheader("RESUMO DOS DADOS")
st.write(f"Total de registros encontrados: {len(df)}")
st.write(f"Quantidade: {sum(df['QTDE'])}")
st.write(f"Total de Pontos: {sum(df['PONTOS'])}")


st.divider()














