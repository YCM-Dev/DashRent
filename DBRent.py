#Importando bibliotecas Streamlit, Pandas, Matplotlib, NumPy e Seanborn
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Define o nome da página/guia 
st.set_page_config(page_title="Locacao imoveis no Brasil", layout="wide")

#Define uma função para carregar os dados para evitar que demore (caso o arquivo seja grande)
#Adiciona à função carregar_df o carregadndo os dados para a cache do navegador tornando mais leve os próximos carregamentos
@st.cache_data
def carregar_df():
  dados_rentBR = pd.read_csv('houses_to_rent_v2.csv',sep=',', decimal=',', header=0,encoding='latin-1')
  return dados_rentBR

#Cria o dataframe a partir do csv
df_rentBR = carregar_df()

#Criando container para organização e independência das seções no site
#1º Container - Configurando streamlit e carregando os dados
with st.container():
  #Título do Dashboard
  st.title('Dashboard de Imóveis para Locação - Brasil',)
  st.write('Informações sobre imóveis')

  #Inserindo um link
  st.markdown('<a href="https://www.mapa.turismo.gov.br/mapa/init.html#/home" style="display: block; text-align: right;">Conheça mais sobre as cidades brasileiras</a>', unsafe_allow_html=True)

#2º Container - Gráficos com seletor
with st.container():

 #Agrupa os dados por cidade
 imoveis_cid = df_rentBR['city'].value_counts().reset_index()
 imoveis_cid.columns = ['cidade', 'quantidade']

 #Calcula a média dos valores dos aluguéis por cidade
 media_alugueis = df_rentBR.groupby('city')['rent amount (R$)'].mean().reset_index()
 media_alugueis.columns = ['cidade', 'media_preco_aluguel']

 #Ordena os dados pela cidade
 imoveis_cid = imoveis_cid.sort_values(by='cidade')
 media_alugueis = media_alugueis.sort_values(by='cidade')

 #Exibe o gráfico de linhas no Streamlit
 #st.line_chart(imoveis_cid.set_index('cidade'))

 #Define um estilo de texto para o seletor
 st.markdown('<h3 style="font-weight: bold; font-size: 20px;">Selecione a(s) cidade(s) para a Quantidade de Imóveis:</h3>', unsafe_allow_html=True)
 #Cria um seletor para escolher as cidades do 1º gráfico de linhas de quantidade imóveis
 cid_op_quant = st.multiselect(
    '',
    options=imoveis_cid['cidade'].unique(),
    default=imoveis_cid['cidade'].unique()  #Seleciona todas por padrão
 )

 #Filtra os dados com base na seleção da cidade 1º grafico - quantidades
 if cid_op_quant:
    imoveis_filt = imoveis_cid[imoveis_cid['cidade'].isin(cid_op_quant)]
 else:
    imoveis_filt = imoveis_cid

 #Cria o gráfico de linhas pela quantidade de imóveis
 plt.figure(figsize=(10, 5))
 plt.plot(imoveis_filt['cidade'], imoveis_filt['quantidade'], marker='o')
 plt.title('Quantidade de Imóveis por Cidade para alugar')
 plt.xticks(rotation=45)
 plt.grid(False)

 #Adiciona rótulos com os valores nos pontos da linha
 for x, y in zip(imoveis_filt['cidade'], imoveis_filt['quantidade']):
    plt.text(x, y, f'{y:}', ha='center', va='bottom',fontsize=8, fontweight='bold')

 plt.tight_layout()
 st.pyplot(plt) #Exibindo o gráfico no Streamlit

 #Linha de separação personalizada
 st.markdown(
    '<hr style="border: 2px solid #2E8B57; width: 100%;"/>',  # Altere a cor e a largura aqui
    unsafe_allow_html=True
 )

 #Define o estilo do 2º seletor
 st.markdown('<h3 style="font-weight: bold; font-size: 20px;">Selecione as cidades para a Média dos Aluguéis:</h3>', unsafe_allow_html=True)
 #Cria um seletor para escolher as cidades do 2º gráfico de linhas de média dos alugueis
 cid_op_media = st.multiselect(
    ':',
    options=media_alugueis['cidade'].unique(),
    default=media_alugueis['cidade'].unique()  #Seleciona todas por padrão
 )

 #Filtra os dados com base na seleção da cidade para 2º gráfico - média
 if cid_op_media:
    media_filt = media_alugueis[media_alugueis['cidade'].isin(cid_op_media)]
 else:
    media_filt = media_alugueis

#Cria colunas para os gráficos de barras e média
 col1, col2 = st.columns(2)

 with col1:
    #Cria o 2º gráfico de linhas para a média dos valores dos aluguéis
    plt.figure(figsize=(10, 5))
    plt.plot(media_filt['cidade'],media_filt['media_preco_aluguel'], marker='o', color='orange', label='Média dos Aluguéis')
    plt.title('Média dos Valores dos Aluguéis por Cidade', fontsize=16, fontweight='bold')

    #Adiciona rótulos com os valores nos pontos da linha
    for x, y in zip(media_filt['cidade'], media_filt['media_preco_aluguel']):
        plt.text(x, y, f'${y:.2f}', ha='center', va='bottom',fontsize=14, fontweight='bold')

    plt.xticks(rotation=45,fontsize=12, fontweight='bold')
    plt.grid(False)
    plt.tight_layout()
    st.pyplot(plt)

 with col2:
    #Cria 3º gráfico de barras para a média dos aluguéis por cidade em ordem decrescente
    media_filt = media_filt.sort_values(by='media_preco_aluguel', ascending=False)  # Ordenando em ordem decrescente

    #Define cores diferentes para cada cidade por meio de uma colormap
    cores = plt.cm.get_cmap('tab10', len(media_filt))

    plt.figure(figsize=(10, 5))
    bars = plt.bar(media_filt['cidade'], media_filt['media_preco_aluguel'], color=cores(np.arange(len(media_filt))),width=0.5)

    #Adiciona valores nas barras
    for bar, valor in zip(bars, media_filt['media_preco_aluguel']):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'${valor:.2f}', ha='center', va='bottom',fontsize=12, fontweight='bold')

    #Configura outros elementos do gráfico
    plt.title('Média dos Aluguéis por Ordem Decrescente)',fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, fontsize=12, fontweight='bold')
    plt.grid(axis='y')
    plt.grid(False)
    plt.tight_layout()
    st.pyplot(plt)

#Linha de separação personalizada
 st.markdown(
    '<hr style="border: 2px solid #2E8B57; width: 100%;"/>',  # Altere a cor e a largura aqui
    unsafe_allow_html=True
 )

#4º gráfico: Visualização das colunas selecionadas
st.markdown('<h3 style="font-weight: bold; font-size: 20px;">Selecione as opções:</h3>', unsafe_allow_html=True)
#Seletor para filtrar por cidade, área e valor do aluguel
cidade_op = st.multiselect('Cidade(s):', options=df_rentBR['city'].unique())
area_op = st.slider('Faixa de área (m²):', min_value=int(df_rentBR['area'].min()), max_value=int(df_rentBR['area'].max()), value=(int(df_rentBR['area'].min()), int(df_rentBR['area'].max())))
valor_op = st.slider('Faixa de valor do aluguel (R$):', min_value=int(df_rentBR['rent amount (R$)'].min()), max_value=int(df_rentBR['rent amount (R$)'].max()), value=(int(df_rentBR['rent amount (R$)'].min()), int(df_rentBR['rent amount (R$)'].max())))

#Filtra o DataFrame com base nas seleções
df_filt = df_rentBR[
    (df_rentBR['city'].isin(cidade_op) if cidade_op else True) &
    (df_rentBR['area'].between(area_op[0], area_op[1])) &
    (df_rentBR['rent amount (R$)'].between(valor_op[0], valor_op[1]))
]

# Renomeando as colunas
df_filt_renamed = df_filt.rename(columns={
    'city': 'Cidade',
    'area': 'Área (m²)',
    'rooms': 'Quartos',
    'bathroom': 'Banheiros',
    'parking spaces': 'Estacionamento',
    'floor': 'Andar/Piso',
    'animal': 'Aceita animal?',
    'furniture': 'Mobiliado?',
    'hoa (R$)':'Hora de aluguel',
    'rent amount (R$)': 'Valor do Aluguel (R$)',
    'property tax (R$)':'Imposto sobre a propriedade',
    'fire insurance (R$)': 'Seguro contra incêndio',
    'total (R$)':'Valor Total (R$)'
})

st.write(df_filt_renamed)

#Linha de separação personalizada
st.markdown(
  '<hr style="border: 2px solid #2E8B57; width: 100%;"/>',  # Altere a cor e a largura aqui
  unsafe_allow_html=True
)

# Cria o 5º gráfico de barras das médias
# Calculando as médias por cidade
med_alug = df_rentBR.groupby('city')['rent amount (R$)'].mean().reset_index()
med_alug.columns = ['cidade', 'media_aluguel']

med_tot = df_rentBR.groupby('city')['total (R$)'].mean().reset_index()
med_tot.columns = ['cidade', 'media_total']

#Une os dois DataFrames
media_combined = pd.merge(med_alug, med_tot, on='cidade')

st.markdown('<h3 style="font-weight: bold; font-size: 20px;">Média do Valor do Aluguel e Média do Valor Total por Cidade:</h3>', unsafe_allow_html=True)

plt.figure(figsize=(12, 6))
bar_width = 0.35
x = range(len(media_combined))

#Cria as barras
bars1 = plt.bar(x, media_combined['media_aluguel'], width=bar_width, label='Média do Aluguel (R$)', color='blue')
bars2 = plt.bar([p + bar_width for p in x], media_combined['media_total'], width=bar_width, label='Média do Valor Total (R$)', color='orange')

#Adiciona rótulos com os valores nas barras
for bar in bars1:
  yval = bar.get_height()
  plt.text(bar.get_x() + bar.get_width()/2, yval, f'R$ {yval:.2f}', ha='center', va='bottom', fontsize=7, fontweight='bold')

for bar in bars2:
  yval = bar.get_height()
  plt.text(bar.get_x() + bar.get_width()/2, yval, f'R$ {yval:.2f}', ha='center', va='bottom', fontsize=7, fontweight='bold')

# Configura os rótulos e título
plt.title('Comparação das Médias de Aluguel e Total por Cidade', fontsize=16, fontweight='bold')
plt.xticks([p + bar_width / 2 for p in x], media_combined['cidade'], rotation=45)
plt.legend()
st.pyplot(plt)