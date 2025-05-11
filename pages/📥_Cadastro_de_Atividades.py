import streamlit as st
import pandas as pd
from services.db_helper import fetch_query, fetch_atividades_por_servico, insert_atividade, update_atividade

# ---------------------
# INTERFACE
# ---------------------
st.set_page_config(layout="wide")
st.title("📥 Cadastro de Atividades")

# Carregar dados
df_status = fetch_query("SELECT id, status FROM status ORDER BY status ASC")
df_servicos = fetch_query("""
    SELECT servicos.id, servicos.nome_servico, empresas.id AS cliente_id, empresas.empresa AS cliente
    FROM servicos
    INNER JOIN empresas ON servicos.cliente_id = empresas.id
    ORDER BY servicos.nome_servico ASC
""")

# Seleção do serviço
servico_nome = st.selectbox("Selecione um serviço", df_servicos['nome_servico'])

if servico_nome:
    servico_id = df_servicos.loc[df_servicos['nome_servico'] == servico_nome, 'id'].values[0]
    cliente_id = df_servicos.loc[df_servicos['nome_servico'] == servico_nome, 'cliente_id'].values[0]
    cliente_nome = df_servicos.loc[df_servicos['nome_servico'] == servico_nome, 'cliente'].values[0]

    st.subheader(f"Atividades de **{servico_nome}**:")

    # Buscar atividades existentes
    df_atividades = fetch_atividades_por_servico(servico_id)

    # Se ainda não tiver atividades, inicializa DataFrame
    if df_atividades.empty:
        df_atividades = pd.DataFrame(columns=[
            'id', 'cliente', 'servico', 'nome_atividade', 'tempo', 'status', 'data_prevista', 'data_concluida'
        ])

    # Botão para adicionar nova linha
    if st.button("➕ Adicionar nova atividade"):
        nova_linha = pd.DataFrame([{
            'id': None,
            'cliente': cliente_nome,
            'servico': servico_nome,
            'nome_atividade': '',
            'tempo': 0,
            'status': df_status['status'].iloc[0],  # Primeiro status por padrão
            'data_prevista': pd.to_datetime('today').date(),
            'data_concluida': None
        }])
        df_atividades = pd.concat([df_atividades, nova_linha], ignore_index=True)

    # Editor de dados
    edited_df = st.data_editor(
        df_atividades,
        use_container_width=True,
        key="editor_atividades",
        column_config={
            "status": st.column_config.SelectboxColumn(
                label="Status",
                options=df_status['status'].tolist()
            ),
            "data_prevista": st.column_config.DateColumn(
                label="Data Prevista",
                format="DD/MM/YYYY"
            ),
            "data_concluida": st.column_config.DateColumn(
                label="Data Concluída",
                format="DD/MM/YYYY"
            )
        },
        disabled=["cliente", "servico"],
        num_rows="dynamic"
    )

    # Botão salvar alterações
    if st.button("💾 Salvar alterações"):
        for idx, row in edited_df.iterrows():
            status_id = df_status.loc[df_status['status'] == row['status'], 'id'].values[0]

            if pd.isna(row['id']):
                # Linha nova: INSERT
                insert_atividade(
                    cliente_id,
                    servico_id,
                    row['nome_atividade'],
                    row['tempo'],
                    status_id,
                    row['data_prevista'],
                    row['data_concluida']
                )
            else:
                # Linha existente: UPDATE
                update_atividade(
                    row['id'],
                    row['nome_atividade'],
                    row['tempo'],
                    status_id,
                    row['data_prevista'],
                    row['data_concluida']
                )

        st.success("Alterações salvas com sucesso!")
        st.rerun()
