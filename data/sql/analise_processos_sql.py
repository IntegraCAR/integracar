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

OBTER_TODOS_DETALHADO = """
SELECT
    ap.cod_analise,
    ap.data_hora_inicio_analise,
    ap.data_previsao_fim_analise,
    ap.cod_processo,
    p.numero_processo_florestal,
    ap.cod_status,
    s.tipo_status,
    s.data_hora_ultima_atualizacao,
    ap.cod_usuario,
    u.nome_usuario,
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
    p.numero_processo_florestal,
    ap.cod_status,
    s.tipo_status,
    s.data_hora_ultima_atualizacao,
    ap.cod_usuario,
    u.nome_usuario,
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