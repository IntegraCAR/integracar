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

DELETAR = """
DELETE FROM Analise_Processos
WHERE cod_analise = %s;
"""

ATUALIZAR = """
UPDATE Analise_Processos
SET data_hora_inicio_analise = COALESCE(CAST(%s AS TIMESTAMP), data_hora_inicio_analise),
    data_previsao_fim_analise = COALESCE(CAST(%s AS TIMESTAMP), data_previsao_fim_analise)
WHERE cod_processo = %s
RETURNING cod_analise, cod_status;
"""

ATUALIZAR_STATUS_EXISTENTE = """
UPDATE Status
SET tipo_status = %s,
    data_hora_ultima_atualizacao = date_trunc('second', CURRENT_TIMESTAMP AT TIME ZONE 'America/Sao_Paulo')
WHERE cod_status = %s;
"""

OBTER_TODOS_DETALHADO = """
SELECT
    ap.cod_analise,
    ap.data_hora_inicio_analise,
    ap.data_previsao_fim_analise,
    ap.cod_processo,
    p.codigo_edocs,
    p.numero_processo_florestal,
    p.codigo_empreendimento,
    ap.cod_status,
    s.tipo_status,
    s.data_hora_ultima_atualizacao,
    ap.cod_usuario,
    u.nome_usuario,
    u.role_usuario,
    ap.cod_campus,
    c.nome_campus,
    ap.cod_notificacao,
    n.motivo_notificacao
FROM Analise_Processos ap
LEFT JOIN Processo p ON ap.cod_processo = p.cod_processo
LEFT JOIN Status s ON ap.cod_status = s.cod_status
LEFT JOIN Usuario u ON ap.cod_usuario = u.cod_usuario
LEFT JOIN Campus c ON ap.cod_campus = c.cod_campus
LEFT JOIN Notificacao n ON ap.cod_notificacao = n.cod_notificacao
ORDER BY ap.data_hora_inicio_analise DESC;
"""

OBTER_POR_PROCESSO = """
SELECT
    ap.cod_analise,
    ap.data_hora_inicio_analise,
    ap.data_previsao_fim_analise,
    ap.cod_processo,
    p.codigo_edocs,
    p.numero_processo_florestal,
    p.codigo_empreendimento,
    ap.cod_status,
    s.tipo_status,
    s.data_hora_ultima_atualizacao,
    ap.cod_usuario,
    u.nome_usuario,
    u.role_usuario,
    ap.cod_campus,
    c.nome_campus,
    ap.cod_notificacao,
    n.motivo_notificacao
FROM Analise_Processos ap
LEFT JOIN Processo p ON ap.cod_processo = p.cod_processo
LEFT JOIN Status s ON ap.cod_status = s.cod_status
LEFT JOIN Usuario u ON ap.cod_usuario = u.cod_usuario
LEFT JOIN Campus c ON ap.cod_campus = c.cod_campus
LEFT JOIN Notificacao n ON ap.cod_notificacao = n.cod_notificacao
WHERE ap.cod_processo = %s
ORDER BY ap.data_hora_inicio_analise DESC;
"""

CONTAGEM_POR_STATUS = """
SELECT s.tipo_status, COUNT(*) AS quantidade
FROM Analise_Processos ap
LEFT JOIN Status s ON ap.cod_status = s.cod_status
GROUP BY s.tipo_status
ORDER BY quantidade DESC;
"""

ULTIMAS_ANALISES = """
SELECT
    ap.cod_analise,
    ap.data_hora_inicio_analise,
    ap.data_previsao_fim_analise,
    ap.cod_processo,
    p.numero_processo_florestal,
    ap.cod_status,
    s.tipo_status,
    ap.cod_usuario,
    u.nome_usuario
FROM Analise_Processos ap
LEFT JOIN Processo p ON ap.cod_processo = p.cod_processo
LEFT JOIN Status s ON ap.cod_status = s.cod_status
LEFT JOIN Usuario u ON ap.cod_usuario = u.cod_usuario
ORDER BY ap.data_hora_inicio_analise DESC
LIMIT %s;
"""

ULTIMAS_POR_STATUS = """
SELECT 
    s.tipo_status,
    MAX(s.data_hora_ultima_atualizacao) as ultima_atualizacao
FROM Analise_Processos ap
INNER JOIN Status s ON ap.cod_status = s.cod_status
WHERE s.tipo_status IS NOT NULL
GROUP BY s.tipo_status
ORDER BY s.tipo_status;
"""

CONTAGEM_POR_CAMPUS = """
SELECT c.nome_campus, COUNT(*) AS quantidade
FROM Analise_Processos ap
LEFT JOIN Campus c ON ap.cod_campus = c.cod_campus
WHERE c.nome_campus IS NOT NULL
GROUP BY c.nome_campus
ORDER BY quantidade DESC;
"""

CONTAGEM_POR_ORIENTADOR = """
SELECT u.nome_usuario, COUNT(*) AS quantidade
FROM Analise_Processos ap
LEFT JOIN Usuario u ON ap.cod_usuario = u.cod_usuario
WHERE u.role_usuario = 'orientador'
GROUP BY u.nome_usuario
ORDER BY quantidade DESC;
"""

CONTAGEM_POR_BOLSISTA = """
SELECT u.nome_usuario, COUNT(*) AS quantidade
FROM Analise_Processos ap
LEFT JOIN Usuario u ON ap.cod_usuario = u.cod_usuario
WHERE u.role_usuario = 'bolsista'
GROUP BY u.nome_usuario
ORDER BY quantidade DESC;
"""