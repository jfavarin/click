import streamlit as st
import pandas as pd
from services.db_helper import fetch_query, insert_servico, update_servico

# ---------------------
# INTERFACE
# ---------------------
st.set_page_config(layout="wide")
header = st.container()
body = st.container()

# Carregar tabelas
df_tipo = fetch_query("SELECT id, tipo_servico FROM tipo_servico ORDER BY tipo_servico ASC")
df_clientes = fetch_query("SELECT id, empresa FROM empresas ORDER BY empresa ASC")
df_status = fetch_query("SELECT id, status FROM status ORDER BY status ASC")
df_tags = fetch_query("SELECT id, tag FROM tags ORDER BY tag ASC")

# ---------------------
# HEADER
# ---------------------
with header:
    st.title("🗂️ Cadastro de Serviços (Banco de Dados)")

# FORMULÁRIO
with st.form(key='cadastro_form'):
    tipo_servico_nome = st.selectbox('Tipo de Serviço', df_tipo['tipo_servico'], index=None)
    nome_servico = st.text_input('Nome do Serviço')
    cliente_nome = st.selectbox('Cliente', df_clientes['empresa'], index=None)
    status_nome = st.selectbox('Status', df_status['status'], index=None)
    valor = st.number_input('Valor do Contrato', min_value=0.0, format="%.2f")
    tags_selecionadas = st.multiselect('Tags', df_tags['tag'])
    data_vencimento = st.date_input('Data de Vencimento')

    enviar = st.form_submit_button('Enviar')

    if enviar:
        tipo_servico_id = df_tipo.loc[df_tipo['tipo_servico'] == tipo_servico_nome, 'id'].values[0]
        cliente_id = df_clientes.loc[df_clientes['empresa'] == cliente_nome, 'id'].values[0]
        status_id = df_status.loc[df_status['status'] == status_nome, 'id'].values[0]
        
        insert_servico(tipo_servico_id, nome_servico, cliente_id, status_id, valor, tags_selecionadas, data_vencimento)
        st.success('Cadastro realizado com sucesso!')

# TABELA DE CADASTROS EXISTENTES
st.subheader('📄 Cadastros realizados:')

df_cadastros = fetch_query("""
    SELECT
        servicos.id,
        empresas.empresa AS cliente,
        tipo_servico.tipo_servico AS tipo_servico,
        servicos.nome_servico,
        status.status AS status,
        servicos.valor_contrato,
        servicos.tags,
        servicos.data_vencimento
    FROM servicos
    INNER JOIN empresas ON servicos.cliente_id = empresas.id
    INNER JOIN tipo_servico ON servicos.tipo_servico_id = tipo_servico.id
    INNER JOIN status ON servicos.status_id = status.id
    ORDER BY servicos.criado_em DESC
""")

if not df_cadastros.empty:
    edited_df = st.data_editor(
        df_cadastros,
        column_config={
            "status": st.column_config.SelectboxColumn(
                label="Status",
                options=df_status['status'].tolist(),
                help="Selecione o status atual do serviço"
            ),
            "tags": st.column_config.TextColumn(
                label="Tags",
                help="Lista de tags (não editável)"
            ),
            "data_vencimento": st.column_config.DateColumn(
                label="Data de Vencimento",
                format="DD/MM/YYYY",
                help="Informe a nova data de vencimento"
            )
        },
        disabled=["cliente", "tipo_servico", "nome_servico", "valor_contrato", "tags"],
        num_rows="dynamic"
    )

    if st.button('Salvar alterações'):
        for index, row in edited_df.iterrows():
            novo_status_id = df_status.loc[df_status['status'] == row['status'], 'id'].values[0]
            tags_lista = row['tags']
            if isinstance(tags_lista, str):
                tags_lista = [tag.strip() for tag in tags_lista.strip('[]').replace('"', '').split(",")]
            update_servico(row['id'], novo_status_id, row['data_vencimento'], tags_lista)
        st.success('Alterações salvas com sucesso!')
