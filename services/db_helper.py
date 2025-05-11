# db/db_helper.py
import pandas as pd
from db.db import get_conn
import json

# ---------------------
# Funções Auxiliares
# ---------------------

def execute_query(query, params=None):
    """
    Executa comandos INSERT, UPDATE, DELETE
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

def fetch_query(query, params=None):
    """
    Executa SELECTs e retorna DataFrame
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    colnames = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=colnames)
    cursor.close()
    conn.close()
    return df

# ---------------------
# Funções Empresas
# ---------------------

def insert_empresa(nome_empresa, cnpj, email, telefone):
    query = """
        INSERT INTO empresas (empresa, cnpj, email, telefone)
        VALUES (%s, %s, %s, %s)
    """
    params = (nome_empresa, cnpj, email, telefone)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

def fetch_empresas():
    query = "SELECT id, empresa, cnpj, email, telefone, criado_em FROM empresas ORDER BY criado_em DESC"
    conn = get_conn()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ---------------------
# Funções Serviços
# ---------------------

def insert_servico(tipo_servico_id, nome_servico, cliente_id, status_id, valor_contrato, tags, data_vencimento):
    query = """
        INSERT INTO servicos (tipo_servico_id, nome_servico, cliente_id, status_id, valor_contrato, tags, data_vencimento)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        tipo_servico_id,
        nome_servico,
        cliente_id,
        status_id,
        valor_contrato,
        json.dumps(tags),  # salva as tags no formato JSON
        data_vencimento
    )
    execute_query(query, params)

def update_servico(id_servico, novo_status_id, nova_data_vencimento, novas_tags):
    query = """
        UPDATE servicos
        SET status_id = %s,
            data_vencimento = %s,
            tags = %s
        WHERE id = %s
    """
    params = (
        novo_status_id,
        nova_data_vencimento,
        json.dumps(novas_tags),
        id_servico
    )
    execute_query(query, params)

# ---------------------
# Funções Atividades
# ---------------------

def insert_atividade(cliente_id, servico_id, nome_atividade, tempo, status_id, data_prevista, data_concluida=None):
    query = """
        INSERT INTO atividades (cliente_id, servico_id, nome_atividade, tempo, status_id, data_prevista, data_concluida)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (cliente_id, servico_id, nome_atividade, tempo, status_id, data_prevista, data_concluida)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

def update_atividade(atividade_id, nome_atividade, tempo, status_id, data_prevista, data_concluida):
    query = """
        UPDATE atividades
        SET nome_atividade = %s,
            tempo = %s,
            status_id = %s,
            data_prevista = %s,
            data_concluida = %s
        WHERE id = %s
    """
    params = (nome_atividade, tempo, status_id, data_prevista, data_concluida, atividade_id)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

def fetch_atividades_por_servico(servico_id):
    query = """
        SELECT atividades.id, empresas.empresa AS cliente, servicos.nome_servico AS servico, 
               atividades.nome_atividade, atividades.tempo, status.status, atividades.data_prevista, atividades.data_concluida
        FROM atividades
        INNER JOIN empresas ON atividades.cliente_id = empresas.id
        INNER JOIN servicos ON atividades.servico_id = servicos.id
        INNER JOIN status ON atividades.status_id = status.id
        WHERE atividades.servico_id = %s
        ORDER BY atividades.data_prevista ASC
    """
    conn = get_conn()
    df = pd.read_sql(query, conn, params=[servico_id])
    conn.close()
    return df
