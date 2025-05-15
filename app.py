import streamlit as st
from streamlit_option_menu import option_menu
import importlib

st.set_page_config(layout="wide", page_title="Sistema de Cadastro", page_icon="📋")

# Oculta cabeçalho e rodapé
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Menu na sidebar
with st.sidebar:
    pagina_escolhida = option_menu(
        menu_title="Navegação",
        menu_icon="columns",
        options=["Cadastro de Atividades", "Cadastro de Serviços", "Cadastro de Empresas"],
        icons=["check-square-fill", "clipboard-plus-fill", "house-add-fill"]
    )

# Mapeamento de páginas
paginas = {
    "Cadastro de Atividades": "modulos.atividades",
    "Cadastro de Serviços": "modulos.servicos",
    "Cadastro de Empresas": "modulos.empresas"
}

# Carrega a página escolhida
modulo = importlib.import_module(paginas[pagina_escolhida])
modulo.app()
