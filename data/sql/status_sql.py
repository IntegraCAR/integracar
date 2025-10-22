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

ATUALIZAR = """
UPDATE Status
SET tipo_status = %s,
    data_hora_ultima_atualizacao = %s
WHERE cod_status = %s;
"""

DELETAR = """
DELETE FROM Status
WHERE cod_status = %s;
"""

OBTER_POR_ID = """
SELECT cod_status, data_hora_ultima_atualizacao, tipo_status
FROM Status
WHERE cod_status = %s;
"""

OBTER_TODOS = """
SELECT cod_status, data_hora_ultima_atualizacao, tipo_status
FROM Status
ORDER BY data_hora_ultima_atualizacao DESC;
"""

OBTER_POR_TIPO = """
SELECT cod_status, data_hora_ultima_atualizacao, tipo_status
FROM Status
WHERE tipo_status = %s
ORDER BY data_hora_ultima_atualizacao DESC;
"""
