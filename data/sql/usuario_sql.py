CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS Usuario (
    cod_usuario SERIAL PRIMARY KEY,
    cod_campus INTEGER REFERENCES Campus(cod_campus),
    nome_usuario VARCHAR(255) NOT NULL,
    role_usuario VARCHAR(100),
    organizacao_usuario VARCHAR(255)
);
"""

INSERIR = """
INSERT INTO Usuario (cod_campus, nome_usuario, role_usuario, organizacao_usuario)
VALUES (%s, %s, %s, %s)
RETURNING cod_usuario;
"""

ATUALIZAR = """
UPDATE Usuario
SET cod_campus = %s,
    nome_usuario = %s,
    role_usuario = %s,
    organizacao_usuario = %s
WHERE cod_usuario = %s;
"""

DELETAR = """
DELETE FROM Usuario
WHERE cod_usuario = %s;
"""

OBTER_POR_ID = """
SELECT cod_usuario, cod_campus, nome_usuario, role_usuario, organizacao_usuario
FROM Usuario
WHERE cod_usuario = %s;
"""

OBTER_TODOS = """
SELECT cod_usuario, cod_campus, nome_usuario, role_usuario, organizacao_usuario
FROM Usuario
ORDER BY nome_usuario;
"""

OBTER_POR_CAMPUS = """
SELECT cod_usuario, cod_campus, nome_usuario, role_usuario, organizacao_usuario
FROM Usuario
WHERE cod_campus = %s
ORDER BY nome_usuario;
"""

BUSCAR_POR_NOME = """
SELECT cod_usuario, cod_campus, nome_usuario, role_usuario, organizacao_usuario
FROM Usuario
WHERE nome_usuario ILIKE %s
ORDER BY nome_usuario;
"""

OBTER_POR_ROLE = """
SELECT cod_usuario, cod_campus, nome_usuario, role_usuario, organizacao_usuario
FROM Usuario
WHERE role_usuario = %s
ORDER BY nome_usuario;
"""
