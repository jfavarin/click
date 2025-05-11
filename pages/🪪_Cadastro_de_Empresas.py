import streamlit as st
import pandas as pd
from db.db import get_conn

# ---------------------
# FUNÇÕES
# ---------------------
def salvar_cadastro(dados):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO empresas (empresa, cnpj, email, telefone)
        VALUES (%s, %s, %s, %s)
        """,
        (dados['Empresa'],
         dados['CNPJ'],
         dados['Email'],
         dados['Telefone'])
    )
    conn.commit()
    cur.close()

def buscar_cadastros():
    conn = get_conn()
    # Carrega tudo em um DataFrame
    df = pd.read_sql("SELECT id, empresa, cnpj, email, telefone, criado_em FROM empresas ORDER BY criado_em DESC", conn)
    return df

# ---------------------
# INTERFACE
# ---------------------
st.set_page_config(layout="wide")
st.title("🪪 Cadastro de empresas")

with st.form("cadastro_form"):
    nome     = st.text_input('Empresa')
    cnpj     = st.text_input('CNPJ')
    email    = st.text_input('Email')
    telefone = st.text_input('Telefone')
    enviar   = st.form_submit_button('Enviar')

    if enviar:
        dados = {
            'Empresa': nome,
            'CNPJ': cnpj,
            'Email': email,
            'Telefone': telefone
        }
        salvar_cadastro(dados)
        st.success('Cadastro realizado com sucesso!')

# Exibe todos os cadastros
st.subheader('Cadastros realizados:')
df_cad = buscar_cadastros()
st.dataframe(df_cad)
