import streamlit as st
import pandas as pd
import os
# ---------------------
# FUNÇÕES
# ---------------------
# Nome do arquivo CSV onde os dados serão salvos
arquivo_csv = 'db/cadastros.csv'
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
    st.title("🪪 Cadastro de empresas")

#Empresa,CNPJ,Email,Telefone
with st.form(key='cadastro_form'):
    nome = st.text_input('Empresa')
    cnpj = st.text_input('CNPJ')
    email = st.text_input('Email')
    telefone = st.text_input('Telefone')
    
    # Botão de envio
    enviar = st.form_submit_button('Enviar')
    
    if enviar:
        dados = {
            'Empresa': nome,
            'CNPJ': cnpj,
            'Email': email,
            'Telefone': telefone
        }
        salvar_cadastro(dados)
        st.success('Cadastro realizado com sucesso!')

# Mostrar o arquivo CSV atual
if os.path.exists(arquivo_csv):
    st.subheader('Cadastros realizados:')
    df_cadastros = pd.read_csv(arquivo_csv)
    st.dataframe(df_cadastros)