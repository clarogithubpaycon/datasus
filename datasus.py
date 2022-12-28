import streamlit as st
from streamlit.errors import StreamlitAPIException
import pandas as pd
import plotly.express as px
from FuncsForSPO.fpython.functions_for_py import formata_para_real, remove_duplicados_na_lista
import warnings
warnings.filterwarnings("ignore")

st.image('https://upload.wikimedia.org/wikipedia/commons/a/ae/SUS_apenas_preenchimento.svg',width=200)
st.title('DATASUS')
# BARRA LATERAL
bar = st.sidebar
bar.title('Filtre os resultados aqui...')
page = bar.selectbox('Selecione o Dashboard.', ['Internações', 'Estoque de Medicamentos'])
bar.markdown("""---""")

# BARRA LATERAL


if page == 'Internações':
    df = pd.read_csv('internacoes.csv', sep=';', encoding='Windows-1252')
    mes = bar.selectbox('Selecione o mês.', set(df['MÊS'].to_list()))
    especialidade = bar.selectbox('Filtre pela Especialidade.', set(df['ESPECIALIDADE'].to_list()))
    st.subheader('Análise de Dados sob Internações no SUS.')
    df_especialidade = df.loc[df['ESPECIALIDADE'] == especialidade]
    df_2 = df.loc[df['MÊS'] == mes]
    click = st.button('Atualizar')
    st.table(df_2)
    st.table(df_especialidade)
    if click:
        sucesso = st.success('Site atualizado!', icon='✅')

    st.markdown('#### Consultas por Especialidade')
    st.bar_chart(df_2, x='ESPECIALIDADE', y='TOTAL')
elif page == 'Estoque de Medicamentos':
    # Create dfs
    df2 = pd.read_csv('estoque.csv', sep=';', encoding='mbcs')
    # df2['Data Última Atualização'] = pd.to_datetime(df2['Data Última Atualização'])

    municipio_list = list(set(df2['Município'].to_list()))
    medicamentos_list = list(set(df2['Nome do medicamento'].to_list()))
    apresentacao_medicamento_list = list(set(df2['Unidade de apresentação'].to_list()))
    
    st.markdown('#### Estoque de Medicamentos do Rio Grande do Sul')
    linhas = bar.slider('Limite de linhas.', max_value=len(df2.index), min_value=10)
    # SET DATAFRAME LIMIT
    df2 = df2.head(linhas+1)
    municipio = bar.multiselect('Filtro por Município',municipio_list, help='Quando não não existir nenhuma seleção, será todos os itens.')
    medicamentos = bar.multiselect('Filtro por Medicamento',medicamentos_list, help='Quando não não existir nenhuma seleção, será todos os itens.')
    tipo_medicamento = bar.multiselect('Filtro Pela Apresentação',apresentacao_medicamento_list, help='Quando não não existir nenhuma seleção, será todos os itens.')
    
    print()
    print(f'municipio_list = {municipio}')
    print(f'medicamentos_list = {medicamentos}')
    print(f'tipo_medicamento_list = {tipo_medicamento}')
    # filtro municipio
    if len(municipio) == 0:
        pass
    else:
        df2 = df2.loc[df2['Município'].isin(municipio)]
    
    # filtro medicamento
    if len(medicamentos) == 0:
        pass
    else:
        df2 = df2.loc[df2['Nome do medicamento'].isin(medicamentos)]

    # filtro tipo do medicamento
    if len(tipo_medicamento) == 0:
        pass
    else:
        df2 = df2.loc[df2['Unidade de apresentação'].isin(tipo_medicamento)]

    
    click = st.button('Atualizar')
    if click:
        sucesso = st.success('Site atualizado!', icon='✅')
        # st.balloons()
    # Tabela e dash da tabela completa (limitado por linhas)
    with st.expander('Tabela', expanded=False):
        try:
            if df2.empty:
                st.warning('Sem medicamentos, amplie o filtro...')
            else:
                st.dataframe(df2.head(linhas+1))
        except AttributeError:
            st.warning('Sem medicamentos, amplie o filtro...')

    with st.expander('Gráficos', expanded=True):
        try:
            # SET DATAFRAMES AND VARS

            estoque_sum = df2['Quantidade em estoque'].sum()
            representacao_sum = df2['Unidade de apresentação'].sum()
            representacao_sum = df2['Unidade de apresentação'].sum()
            estoque_formatado = formata_para_real(estoque_sum)

            st.markdown('##### Métricas')

            container = st.container()
            a,b,c = container.columns(3)
            a.metric(label="Total no Estoque", value=estoque_formatado)
            b.metric(label="Quantidade de Apresentações.", value=len(remove_duplicados_na_lista(df2['Unidade de apresentação'])))
            b.metric(label="Quantidade de Medicamentos.", value=len(remove_duplicados_na_lista(df2['Nome do medicamento'])))
            c.metric(label="Total de Municípios", value=len(remove_duplicados_na_lista(df2['Município'])))
            # print()
            # print(remove_duplicados_na_lista(df2['Unidade de apresentação']))
            # print(remove_duplicados_na_lista(df2['Nome do medicamento']))
            # print(remove_duplicados_na_lista(df2['Município']))
            # print()
            
            st.markdown("""---""")
            st.markdown('#### Estoque de Medicamentos.')
            st.bar_chart(df2, x='Nome do medicamento', y='Quantidade em estoque', use_container_width=True)
            st.markdown("""---""")
            print(len(medicamentos))
            print(df2['Quantidade em estoque'].sum())
            if estoque_sum == 0:
                st.warning(f'Não existe estoque pelas apresentações indicadas! [ESTOQUE: {estoque_sum}]', icon="⚠️")
            else:
                st.markdown('#### Estoque por Apresentação.')
                fig = px.pie(df2, values='Quantidade em estoque', names='Unidade de apresentação', hole=.5)            
                st.plotly_chart(fig, True)
        except StreamlitAPIException:
            st.warning('Sem medicamentos, amplie o filtro...')
            
    click = st.button('Atualizar', key=2)
    if click:
        sucesso = st.success('Site atualizado!', icon='✅')
