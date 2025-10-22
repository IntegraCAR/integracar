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

ATUALIZAR = """
UPDATE Processo
SET codigo_edocs = %s,
    numero_processo_florestal = %s,
    codigo_empreendimento = %s
WHERE cod_processo = %s;
"""

DELETAR = """
DELETE FROM Processo
WHERE cod_processo = %s;
"""

OBTER_POR_ID = """
SELECT cod_processo, codigo_edocs, numero_processo_florestal, codigo_empreendimento
FROM Processo
WHERE cod_processo = %s;
"""

OBTER_TODOS = """
SELECT cod_processo, codigo_edocs, numero_processo_florestal, codigo_empreendimento
FROM Processo
ORDER BY cod_processo DESC;
"""

BUSCAR_POR_EDOCS = """
SELECT cod_processo, codigo_edocs, numero_processo_florestal, codigo_empreendimento
FROM Processo
WHERE codigo_edocs ILIKE %s
ORDER BY cod_processo DESC;
"""

BUSCAR_POR_PROCESSO_FLORESTAL = """
SELECT cod_processo, codigo_edocs, numero_processo_florestal, codigo_empreendimento
FROM Processo
WHERE numero_processo_florestal ILIKE %s
ORDER BY cod_processo DESC;
"""
