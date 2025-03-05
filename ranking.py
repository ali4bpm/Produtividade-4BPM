import streamlit as st
import pandas as pd
import plotly.express as px

def criar_ranking(df):
    # Agrupar por EFETIVO e somar os PONTOS
    ranking = df.groupby('EFETIVO')['PONTOS'].sum().reset_index()
    
    # Ordenar por PONTOS em ordem decrescente
    ranking = ranking.sort_values('PONTOS', ascending=True)
    
    # Criar gráfico de barras horizontal
    fig = px.bar(ranking, 
                 x='PONTOS', 
                 y='EFETIVO',
                 orientation='h',
                 title='Ranking por Pontuação',
                 labels={'PONTOS': 'Total de Pontos', 'EFETIVO': 'Efetivo'},
                 color='PONTOS',
                 color_continuous_scale='bluered')
    
    # Adicionar rótulos de dados em branco com Time New Roman
    for i in fig.data:
        i.text = i.x  # Usando i.x ao invés de i.y para mostrar os valores dos pontos
        i.textposition = 'outside'
        i.textfont = dict(family='Times New Roman', size=16, color='white')
    
    # Personalizar layout
    fig.update_layout(
        height=700,
        showlegend=False,
        plot_bgcolor='black',
        hoverlabel=dict(bgcolor="black", font_size=14),
        title_x=0.5
    
    )
   
 
    
    return fig
   

# Exibir o gráfico no lugar do dataframe em produtividade.py
# st.plotly_chart(criar_ranking(df), use_container_width=True)
