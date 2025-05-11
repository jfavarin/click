import streamlit as st
from services.db_helper import insert_empresa, fetch_empresas

# ---------------------
# INTERFACE
# ---------------------
st.set_page_config(layout="wide")
st.title("🪪 Cadastro de Empresas")

# FORMULÁRIO
with st.form("cadastro_form"):
    nome     = st.text_input('Empresa')
    cnpj     = st.text_input('CNPJ')
    email    = st.text_input('Email')
    telefone = st.text_input('Telefone')
    enviar   = st.form_submit_button('Enviar')

    if enviar:
        insert_empresa(nome, cnpj, email, telefone)
        st.success('Cadastro realizado com sucesso!')

# Exibe todos os cadastros
st.subheader('Cadastros realizados:')
df_cad = fetch_empresas()
st.dataframe(df_cad)
