CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS Usuario (
    cod_usuario SERIAL PRIMARY KEY,
    cod_campus INTEGER REFERENCES Campus(cod_campus),
    cod_orientador INTEGER NULL,
    nome_usuario VARCHAR(255) NOT NULL,
    email_usuario VARCHAR(255) NOT NULL,
    senha_usuario VARCHAR(255) NOT NULL,
    cpf_usuario VARCHAR(11) NOT NULL,
    role_usuario VARCHAR(100) NULL,
    organizacao_usuario VARCHAR(255) NULL,
    FOREIGN KEY (cod_orientador) REFERENCES Usuario(cod_usuario)
);
"""

INSERIR = """
INSERT INTO Usuario (cod_campus, cod_orientador, nome_usuario, email_usuario, senha_usuario, cpf_usuario, role_usuario, organizacao_usuario)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
RETURNING cod_usuario;
"""

ATUALIZAR = """
UPDATE Usuario
SET cod_campus = %s, 
    cod_orientador = %s, 
    nome_usuario = %s, 
    email_usuario = %s, 
    senha_usuario = %s, 
    cpf_usuario = %s, 
    role_usuario = %s, 
    organizacao_usuario = %s
WHERE cod_usuario = %s;
"""

OBTER_POR_EMAIL = """
SELECT cod_usuario, cod_campus, cod_orientador, nome_usuario, email_usuario, senha_usuario, cpf_usuario, role_usuario, organizacao_usuario
FROM Usuario
WHERE email_usuario = %s;
"""

OBTER_POR_NOME = """
SELECT cod_usuario, cod_campus, cod_orientador, nome_usuario, email_usuario, senha_usuario, cpf_usuario, role_usuario, organizacao_usuario
FROM Usuario
WHERE nome_usuario = %s;
"""

DELETAR = """
DELETE FROM Usuario
WHERE cod_usuario = %s;
"""