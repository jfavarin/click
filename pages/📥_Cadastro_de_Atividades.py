import streamlit as st
import pandas as pd
import os

# ---------------------
# FUNÇÕES
# ---------------------
df_status = pd.read_csv('db/status.csv')
df_services = pd.read_csv('db/servicos.csv')
# Nome do arquivo CSV onde os dados serão salvos
df_activities = pd.read_csv('db/atividades.csv')

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
    st.title("📥 Cadastro de atividades")

# Inicializa session_state
if 'atividades' not in st.session_state:
    st.session_state.atividades = df_activities.copy()

# Selectbox de serviço
servico_selecionado = st.selectbox("Selecione um serviço", df_services['Nome do Serviço'])

# Busca cliente correspondente
cliente_relacionado = df_services.loc[df_services['Nome do Serviço'] == servico_selecionado, 'Cliente'].values[0]

# Filtra dados do serviço
df_servico_selecionado = st.session_state.atividades[st.session_state.atividades['Serviço'] == servico_selecionado].reset_index(drop=True)

# Adicionar nova atividade
if st.button("➕ Adicionar nova atividade"):
    nova_atividade = pd.DataFrame([{
        'Cliente': cliente_relacionado,
        'Serviço': servico_selecionado,
        'Atividade': '',
        'Tempo': '',
        'Status': '',
        'Data concluída': '',
        'Data prevista': ''
    }])
    st.session_state.atividades = pd.concat([st.session_state.atividades, nova_atividade], ignore_index=True)
    st.rerun()

# Editor de dados
st.write(f"Atividades de **{servico_selecionado}**:")
df_editado = st.data_editor(
    df_servico_selecionado,
    use_container_width=True,
    key="editor"
)

# Atualiza session_state com as edições
if st.button("💾 Salvar alterações"):
    # Remove antigas linhas desse cliente
    st.session_state.atividades = st.session_state.atividades[st.session_state.atividades['Serviço'] != servico_selecionado]
    # Adiciona as novas linhas editadas
    df_editado['Serviço'] = servico_selecionado  # Garante que o cliente continue marcado
    st.session_state.atividades = pd.concat([st.session_state.atividades, df_editado], ignore_index=True)
    # Salva no CSV
    st.session_state.atividades.to_csv('db/atividades.csv', index=False)
    st.success("Alterações salvas com sucesso!")