import streamlit as st
import pandas as pd
import os
# ---------------------
# FUNÇÕES
# ---------------------
#Importa nome de cliente
df_tipo = pd.read_csv('db/tipo_de_servico.csv')
df_clientes = pd.read_csv('db/cadastros.csv')
df_status = pd.read_csv('db/status.csv')
df_tags = pd.read_csv('db/tags.csv')
# Nome do arquivo CSV onde os dados serão salvos
arquivo_csv = 'db/servicos.csv'
# Função para salvar o cadastro
def salvar_cadastro(dados):
    # Se o arquivo já existe, carregamos o existente para adicionar mais dados
    if os.path.exists(arquivo_csv):
        df_existente = pd.read_csv(arquivo_csv)
        df_novo = pd.concat([df_existente, pd.DataFrame([dados])], ignore_index=True)
    else:
        df_novo = pd.DataFrame([dados])
    
    # Salva de volta no arquivo
    df_novo.to_csv(arquivo_csv, index=False)



# ---------------------
# INTERFACE
# ---------------------
# configuração da tela
st.set_page_config(layout="wide")
header = st.container()
body = st.container()

# ---------------------
# HEADER
# ---------------------
with header:
    st.title("🗂️ Cadastro de serviços")

#Dados
with st.form(key='cadastro_form'):
    tipo_servico = st.selectbox('Tipo de Serviço', df_tipo['Tipo de serviço'], index=None)
    nome_servico = st.text_input('Nome do Serviço')
    cliente = st.selectbox('Cliente', df_clientes['Empresa'], index=None)
    status = st.selectbox('Status', df_status['Status'], index=None)
    valor = st.number_input('Valor do Contrato')
    tag = st.multiselect('Tags', df_tags['Tag'])
    data_vencimento = st.date_input('Data de Vencimento')
    
    # Botão de envio
    enviar = st.form_submit_button('Enviar')
    
    if enviar:
        dados = {
            'Tipo de Serviço': tipo_servico,
            'Nome do Serviço': nome_servico,
            'Cliente': cliente,
            'Status': status,
            'Valor do Contrato': valor,
            'Tags': tag,
            'Data de Vencimento': data_vencimento
        }
        salvar_cadastro(dados)
        st.success('Cadastro realizado com sucesso!')

# Mostrar o arquivo CSV atual
if os.path.exists(arquivo_csv):
    st.subheader('Cadastros realizados:')
    df_cadastros = pd.read_csv(arquivo_csv)

    if not pd.api.types.is_datetime64_any_dtype(df_cadastros['Data de Vencimento']):
        df_cadastros['Data de Vencimento'] = pd.to_datetime(df_cadastros['Data de Vencimento'])

    edited_df = st.data_editor(
        df_cadastros,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                label="Status",
                options=df_status['Status'].tolist(),
                help="Selecione o status atual do serviço"
            ),
            "Tags": st.column_config.TextColumn(
                label="Tags",
                help="Digite as tags separadas por vírgula"
            ),
            "Data de Vencimento": st.column_config.DateColumn(
                label="Data de Vencimento",
                format="DD/MM/YYYY",
                help="Informe a nova data de vencimento"
            )
        },
        disabled=["Tipo de Serviço", "Nome do Serviço", "Cliente", "Valor do Contrato"],
        num_rows="dynamic"
    )

    if st.button('Salvar alterações'):
        edited_df.to_csv(arquivo_csv, index=False)
        st.success('Alterações salvas com sucesso!')