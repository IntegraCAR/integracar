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

ATUALIZAR = """
UPDATE Notificacao
SET motivo_notificacao = %s
WHERE cod_notificacao = %s;
"""

DELETAR = """
DELETE FROM Notificacao
WHERE cod_notificacao = %s;
"""

OBTER_POR_ID = """
SELECT cod_notificacao, motivo_notificacao
FROM Notificacao
WHERE cod_notificacao = %s;
"""

OBTER_TODOS = """
SELECT cod_notificacao, motivo_notificacao
FROM Notificacao
ORDER BY cod_notificacao DESC;
"""
