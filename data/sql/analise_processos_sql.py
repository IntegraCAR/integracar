CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS Analise_Processos (
    cod_analise SERIAL PRIMARY KEY,
    data_hora_inicio_analise TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_previsao_fim_analise TIMESTAMP,
    cod_campus INTEGER REFERENCES Campus(cod_campus),
    cod_usuario INTEGER REFERENCES Usuario(cod_usuario),
    cod_status INTEGER REFERENCES Status(cod_status),
    cod_notificacao INTEGER REFERENCES Notificacao(cod_notificacao),
    cod_processo INTEGER REFERENCES Processo(cod_processo)
);
"""

INSERIR = """
INSERT INTO Analise_Processos (
    data_hora_inicio_analise,
    data_previsao_fim_analise,
    cod_campus,
    cod_usuario,
    cod_status,
    cod_notificacao,
    cod_processo
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
RETURNING cod_analise;
"""

ATUALIZAR = """
UPDATE Analise_Processos
SET data_hora_inicio_analise = %s,
    data_previsao_fim_analise = %s,
    cod_campus = %s,
    cod_usuario = %s,
    cod_status = %s,
    cod_notificacao = %s,
    cod_processo = %s
WHERE cod_analise = %s;
"""

ATUALIZAR_STATUS = """
UPDATE Analise_Processos
SET cod_status = %s
WHERE cod_analise = %s;
"""

DELETAR = """
DELETE FROM Analise_Processos
WHERE cod_analise = %s;
"""

OBTER_POR_ID = """
SELECT cod_analise, data_hora_inicio_analise, data_previsao_fim_analise,
       cod_campus, cod_usuario, cod_status, cod_notificacao, cod_processo
FROM Analise_Processos
WHERE cod_analise = %s;
"""

OBTER_TODOS = """
SELECT cod_analise, data_hora_inicio_analise, data_previsao_fim_analise,
       cod_campus, cod_usuario, cod_status, cod_notificacao, cod_processo
FROM Analise_Processos
ORDER BY data_hora_inicio_analise DESC;
"""

OBTER_POR_CAMPUS = """
SELECT cod_analise, data_hora_inicio_analise, data_previsao_fim_analise,
       cod_campus, cod_usuario, cod_status, cod_notificacao, cod_processo
FROM Analise_Processos
WHERE cod_campus = %s
ORDER BY data_hora_inicio_analise DESC;
"""

OBTER_POR_USUARIO = """
SELECT cod_analise, data_hora_inicio_analise, data_previsao_fim_analise,
       cod_campus, cod_usuario, cod_status, cod_notificacao, cod_processo
FROM Analise_Processos
WHERE cod_usuario = %s
ORDER BY data_hora_inicio_analise DESC;
"""

OBTER_POR_STATUS = """
SELECT cod_analise, data_hora_inicio_analise, data_previsao_fim_analise,
       cod_campus, cod_usuario, cod_status, cod_notificacao, cod_processo
FROM Analise_Processos
WHERE cod_status = %s
ORDER BY data_hora_inicio_analise DESC;
"""

OBTER_POR_PROCESSO = """
SELECT cod_analise, data_hora_inicio_analise, data_previsao_fim_analise,
       cod_campus, cod_usuario, cod_status, cod_notificacao, cod_processo
FROM Analise_Processos
WHERE cod_processo = %s
ORDER BY data_hora_inicio_analise DESC;
"""

OBTER_ATRASADAS = """
SELECT cod_analise, data_hora_inicio_analise, data_previsao_fim_analise,
       cod_campus, cod_usuario, cod_status, cod_notificacao, cod_processo
FROM Analise_Processos
WHERE data_previsao_fim_analise < CURRENT_TIMESTAMP
  AND cod_status IN (SELECT cod_status FROM Status WHERE tipo_status != 'Concluído')
ORDER BY data_previsao_fim_analise ASC;
"""
