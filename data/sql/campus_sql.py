CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS Campus (
    cod_campus SERIAL PRIMARY KEY,
    nome_campus VARCHAR(255) NOT NULL
);
"""

INSERIR = """
INSERT INTO Campus (nome_campus)
VALUES (%s)
RETURNING cod_campus;
"""

OBTER_POR_NOME = """
SELECT cod_campus, nome_campus
FROM Campus
WHERE nome_campus = %s;
"""

DELETAR = """
DELETE FROM Campus
WHERE cod_campus = %s;
"""
