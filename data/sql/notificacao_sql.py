CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS Notificacao (
    cod_notificacao SERIAL PRIMARY KEY,
    motivo_notificacao TEXT
);
"""

INSERIR = """
INSERT INTO Notificacao (motivo_notificacao)
VALUES (%s)
RETURNING cod_notificacao;
"""

DELETAR = """
DELETE FROM Notificacao
WHERE cod_notificacao = %s;
"""