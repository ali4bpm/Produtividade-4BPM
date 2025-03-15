import streamlit as st
import pandas as pd
import numpy as np
import gspread
import plotly.express as px
import openpyxl
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from io import BytesIO
from utils import carregar_dados
# Configurando a página
st.set_page_config(page_title="Produtividade 4º BPM",page_icon="brasao.jpg",layout='wide')

# Hide Streamlit elements
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display: none;}
            .viewerBadge_container__1QSob {display: none;}
            .stToolbar {display: none;}
            .appview-container .main .block-container {padding-top: 1rem;}
            div[data-testid="stToolbar"] {display: none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Configuração de credenciais
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["connections"]["gsheets"], scope)
client = gspread.authorize(credentials)

# Mover o dicionário de tradução dos meses para antes da função carregar_dados
meses = {'January':'Janeiro', 'February':'Fevereiro', 'March': 'Março',
         'April': 'Abril', 'May': 'Maio', 'June': 'Junho', 'July': 'Julho',
         'August': 'Agosto', 'September': 'Setembro', 'October': 'Outubro',
         'November': 'Novembro', 'December': 'Dezembro'}

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    planilha = client.open_by_key('1PLZZMSrp19FFvVIAOhZTVnRh7Tk7EQLoROZy4OaBCDg')
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

# Título do aplicativo
#st.title("PRODUTIVIDADE E PONTUAÇÃO")
st.markdown("<h1 style='text-align: center;'>PRODUTIVIDADE E PONTUAÇÃO</h1>", unsafe_allow_html=True)

# Texto na página
st.write("Produtividade - 4º BPM RN")

# Sidebar com filtros
st.sidebar.image("brasao.jpg")
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
    st.write("ARMA BRANCA  (Homicídio, Tentativa de homicídio com Lesão Corporal Grave e Roubo consumado): 05 pontos")
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
    st.write("MUNIÇÃO 1 - 10: 05 pontos")
    st.write("MUNIÇÃO 11 - 20: 10 pontos")
    st.write("MUNIÇÃO 21 - 50: 15 pontos")
    st.write("MUNIÇÃO 51 - 100: 20 pontos")
    st.write("MUNIÇÃO 101 ou mais: 30 pontos")
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
    if df.empty:
        st.error("Não há dados para gerar o PDF")
        return None
        
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    
    # Ensure data is properly converted to strings
    df_copy = df.fillna('')  # Replace NaN with empty string
    df_copy = df_copy.astype(str)  # Convert all values to strings
    
    # Convert DataFrame to list with error handling
    try:
        data = [df_copy.columns.tolist()] + df_copy.values.tolist()
        
        # Validate data before creating table
        if not data or len(data[0]) == 0:
            st.error("Dados inválidos para gerar PDF")
            return None
            
        # Create table with validated data
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
        
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {str(e)}")
        return None

# Update the PDF download section
try:
    # Mostrar DataFrame
    st.dataframe(df, use_container_width=True)
    
    # Criar botão de download apenas se houver dados
    pdf = create_pdf(df)
    if pdf is not None:
        st.download_button(
            label="📥 Baixar Relatório em PDF",
            data=pdf,
            file_name="produtividade.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
except Exception as e:
    st.error(f"Erro ao exibir dados: {str(e)}")

    
# Resumo dos dados
st.divider()
st.subheader("RESUMO DOS DADOS")
st.write(f"Total de registros encontrados: {len(df)}")
st.write(f"Quantidade: {sum(df['QTDE'])}")
st.write(f"Total de Pontos: {sum(df['PONTOS'])}")


st.divider()

# Criar ranking com formato melhorado e ordenação decrescente
st.markdown("<h1 style='text-align: center;'>RANKING DE PRODUTIVIDADE</h1>", unsafe_allow_html=True)
ranking = df.groupby(['EFETIVO', 'COMPANHIA']).agg({
        'PONTOS': 'sum',
        'QTDE': 'sum'
    }).reset_index()
    
ranking = ranking.sort_values('PONTOS', ascending=False)
ranking.index = range(1, len(ranking) + 1)
ranking['PONTOS'] = ranking['PONTOS'].astype(int)

    # Mostrar ranking formatado
st.dataframe(
        ranking,
        use_container_width=True,
        column_config={
            "PONTOS": st.column_config.NumberColumn(
                "PONTOS",
                format="%d"
            )
        }
    )

try:
    # Criar botão de download apenas se houver dados
    pdf = create_pdf(ranking)
    if pdf is not None:
        st.download_button(
            label="📥 Baixar Ranking em PDF",
            data=pdf,
            file_name="ranking_produtividade.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
except Exception as e:
    st.error(f"Erro ao exibir dados do ranking: {str(e)}")

    # Gráfico horizontal melhorado com ordem decrescente
fig = px.bar(
        ranking.sort_values('PONTOS', ascending=True),
        y='EFETIVO',
        x='PONTOS',
        #title='Ranking de Produtividade por Pontuação',
        text=[f" {p:,d}" for i, p in zip(range(len(ranking), 0, -1), 
              ranking.sort_values('PONTOS', ascending=True)['PONTOS'])],
        orientation='h',
        height=600,  # Ajuste dinâmico da altura baseado no número de registros
        width=800  # Ajuste dinâmico da largura
    )
    
fig.update_layout(
        xaxis_title="Total de Pontos",
        yaxis_title="Efetivo",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white', 'size': 12},
        title={
            'text': 'Ranking de Produtividade por Pontuação',
            'x': 0.5,  # Center title
            'xanchor': 'center',
            'font': {'color': 'white', 'size': 16, 'family': 'Arial Black'}
        },
        yaxis={'tickfont': {'size': 12}},  # Aumentar fonte do eixo Y
        margin=dict(l=20, r=150, t=40, b=20),  # Margem direita maior para labels
        bargap=0.5  # Espaçamento entre barras
    )

fig.update_traces(
        marker_color='#1f77b4',
        textfont={'color': 'white', 'size': 12, 'family': 'Arial Bold'},
        textposition='outside',
        #marker_line_color='white',
        marker_line_width=1,
        hovertemplate='<b>%{y}</b><br>Pontuação: %{x:.d} pontos<extra></extra>',
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Arial',
            font_color='#1f77b4'
        )
    )

    # Remover grades e ajustar eixos
fig.update_xaxes(showgrid=False, title_font={'size': 14})
fig.update_yaxes(showgrid=False, title_font={'size': 14})

st.plotly_chart(fig, use_container_width=True)
#except Exception as e:
#st.error(f"Erro ao processar dados: {str(e)}")

# Resumo dos dados
st.divider()
st.subheader("RESUMO DOS DADOS")
st.write(f"Total de registros encontrados: {len(df)}")
st.write(f"Quantidade: {sum(df['QTDE'])}")
st.write(f"Total de Pontos: {sum(df['PONTOS'])}")


st.divider()















