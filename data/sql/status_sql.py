CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS Status (
    cod_status SERIAL PRIMARY KEY,
    data_hora_ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_status VARCHAR(50) NOT NULL
);
"""

INSERIR = """
INSERT INTO Status (tipo_status, data_hora_ultima_atualizacao)
VALUES (%s, %s)
RETURNING cod_status;
"""

DELETAR = """
DELETE FROM Status
WHERE cod_status = %s;
"""