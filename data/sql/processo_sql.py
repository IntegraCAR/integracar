CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS Processo (
    cod_processo SERIAL PRIMARY KEY,
    codigo_edocs VARCHAR(100),
    numero_processo_florestal VARCHAR(100),
    codigo_empreendimento VARCHAR(100)
);
"""

INSERIR = """
INSERT INTO Processo (codigo_edocs, numero_processo_florestal, codigo_empreendimento)
VALUES (%s, %s, %s)
RETURNING cod_processo;
"""

DELETAR = """
DELETE FROM Processo
WHERE cod_processo = %s;
"""