import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página com o ícone (favicon) alterado
st.set_page_config(
    layout="wide",
    page_title="Análise de Dados do CREFITO-3",
    page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQxehbL7lmNh2wgBb3I2l24TZ7tfw6N5c9Qw&s"  # URL do logo CREFITO
)

# Exibir o logo do CREFITO
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQxehbL7lmNh2wgBb3I2l24TZ7tfw6N5c9Qw&s", width=200)

# Introdução
st.title("Análise de Dados do CREFITO-3")
st.write("""
## Introdução
O CREFITO-3 (Conselho Regional de Fisioterapia e Terapia Ocupacional da 3ª Região) é uma autarquia federal que regulamenta e fiscaliza o exercício das profissões de fisioterapia e terapia ocupacional no estado de São Paulo. Este projeto visa analisar e visualizar dados de profissionais registrados no CREFITO-3, fornecendo insights valiosos sobre a distribuição de profissionais por status, profissão, região e cidade.

Neste aplicativo, você pode explorar:
- A distribuição de profissionais por status de registro.
- A distribuição de profissionais por profissão.
- A distribuição de profissionais por subsede/região.
- A distribuição de profissionais por cidade.
- Filtragem dos dados por status, profissão, cidade e subsede/região.
- Busca de profissionais pelo nome.
""")

# Carregar os dados
uploaded_file_1 = 'crefito_FO_results_600k.xlsx'
uploaded_file_2 = 'crefito_TO.xlsx'

if uploaded_file_1 and uploaded_file_2:
    # Ler ambos os arquivos Excel
    df1 = pd.read_excel(uploaded_file_1)
    df2 = pd.read_excel(uploaded_file_2)

    # Concatenar os dois dataframes
    df = pd.concat([df1, df2], ignore_index=True)

    # Remover linhas com valores None nas colunas relevantes
    df = df.dropna(subset=['status', 'profissao', 'Subsede_Região', 'cidade'])

    # Mostrar o dataframe sem o índice
    st.write("## Visão Geral dos Dados")
    st.dataframe(df.head(), use_container_width=True, hide_index=True)

    # Estatísticas gerais
    st.write("## Estatísticas Gerais")
    st.write(df.describe())

    # Adicionar painel expansível para filtros
    with st.expander("Filtros de Dados"):
        with st.form(key='filtros'):
            # Filtros
            status_filter = st.selectbox("Selecione o status", options=df['status'].unique())
            profession_filter = st.selectbox("Selecione a profissão", options=df['profissao'].unique())
            city_filter = st.selectbox("Selecione a cidade", options=df['cidade'].unique())
            region_filter = st.selectbox("Selecione a subsede/região", options=df['Subsede_Região'].unique())

            # Submit do formulário
            submit_button = st.form_submit_button(label='Filtrar Dados')

        # Aplicar filtros ao dataframe se o botão for pressionado
        if submit_button:
            filtered_data = df[
                (df['status'] == status_filter) &
                (df['profissao'] == profession_filter) &
                (df['cidade'] == city_filter) &
                (df['Subsede_Região'] == region_filter)
            ]
            st.write("## Dados Filtrados")
            st.dataframe(filtered_data.reset_index(drop=True), use_container_width=True, hide_index=True)

    # Separador de seções
    st.divider()

    # Distribuição de profissionais por status
    st.write("## Distribuição de Profissionais por Status")
    status_counts = df['status'].value_counts()
    fig_status = px.bar(status_counts, x=status_counts.index, y=status_counts.values,
                        labels={'x': 'Status', 'y': 'Contagem'})
    st.plotly_chart(fig_status)

    # Separador de seções
    st.divider()

    # Distribuição de profissionais por profissão
    st.write("## Distribuição de Profissionais por Profissão")
    profession_counts = df['profissao'].value_counts()
    fig_profession = px.bar(profession_counts, x=profession_counts.index, y=profession_counts.values,
                            labels={'x': 'Profissão', 'y': 'Contagem'})
    st.plotly_chart(fig_profession)

    # Separador de seções
    st.divider()

    # Distribuição por região
    st.write("## Distribuição de Profissionais por Subsede Região")
    region_counts = df['Subsede_Região'].value_counts()
    fig_region = px.bar(region_counts, x=region_counts.index, y=region_counts.values,
                        labels={'x': 'Subsede Região', 'y': 'Contagem'})
    st.plotly_chart(fig_region)

    # Separador de seções
    st.divider()

    # Profissionais por cidade
    st.write("## Distribuição de Profissionais por Cidade")
    city_counts = df['cidade'].value_counts().head(10)  # Mostrando as 10 principais cidades
    fig_city = px.bar(city_counts, x=city_counts.index, y=city_counts.values, labels={'x': 'Cidade', 'y': 'Contagem'})
    st.plotly_chart(fig_city)

# Adicionar o copyright ao final da página
st.markdown("""
    <footer style="text-align:center; font-size: 12px; margin-top: 50px;">
        &copy; 2024 David G. | <a href="https://www.linkedin.com/in/davidggoncalves/" target="_blank">LinkedIn Profile</a>
    </footer>
""", unsafe_allow_html=True)
