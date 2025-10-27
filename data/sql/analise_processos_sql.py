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