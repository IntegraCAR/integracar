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

ATUALIZAR = """
UPDATE Campus
SET nome_campus = %s
WHERE cod_campus = %s;
"""

DELETAR = """
DELETE FROM Campus
WHERE cod_campus = %s;
"""

OBTER_POR_ID = """
SELECT cod_campus, nome_campus
FROM Campus
WHERE cod_campus = %s;
"""

OBTER_TODOS = """
SELECT cod_campus, nome_campus
FROM Campus
ORDER BY nome_campus;
"""

BUSCAR_POR_NOME = """
SELECT cod_campus, nome_campus
FROM Campus
WHERE nome_campus ILIKE %s
ORDER BY nome_campus;
"""
