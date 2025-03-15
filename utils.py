import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def conectar_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(credentials)
    return client

def carregar_dados():
    client = conectar_google_sheets()
    planilha = client.open_by_key('1PLZZMSrp19FFvVIAOhZTVnRh7Tk7EQLoROZy4OaBCDg')
    aba = planilha.worksheet('Sheet_Pontuacao')

    # Acessar os dados da planilha
    dados = aba.get_all_values()
    
    # Convertendo em DataFrame do pandas      
    df = pd.DataFrame(dados[1:], columns[dados[0]])
    
    # Converter DATA para datetime e criar colunas derivadas
    df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce')
    df['ANO'] = df['DATA'].dt.year.astype(str)
    
    # Mapeamento de meses em português
    meses = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
        'April': 'Abril', 'May': 'Maio', 'June': 'Junho', 'July': 'Julho',
        'August': 'Agosto', 'September': 'Setembro', 'October': 'Outubro',
        'November': 'Novembro', 'December': 'Dezembro'
    }
    
    df['MÊS'] = df['DATA'].dt.strftime('%B').map(meses)
    df['QTDE'] = pd.to_numeric(df['QTDE'], errors='coerce')
    df['PONTOS'] = pd.to_numeric(df['PONTOS'], errors='coerce')
    df['DATA'] = df['DATA'].dt.strftime('%d/%m/%Y')
    
    return df
