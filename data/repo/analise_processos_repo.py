from typing import Optional, List
from data.model.analise_processos import AnaliseProcessos
from data.sql.analise_processos_sql import *
from util.database import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao criar tabela Analise_Processos: {e}")
        return False

def inserir(analise: AnaliseProcessos, cursor=None) -> Optional[int]:
    if cursor is not None:
        cursor.execute(INSERIR, (
            analise.data_hora_inicio_analise,
            analise.data_previsao_fim_analise,
            analise.cod_campus,
            analise.cod_usuario,
            analise.cod_status,
            analise.cod_notificacao,
            analise.cod_processo
        ))
        return cursor.fetchone()[0]
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                analise.data_hora_inicio_analise,
                analise.data_previsao_fim_analise,
                analise.cod_campus,
                analise.cod_usuario,
                analise.cod_status,
                analise.cod_notificacao,
                analise.cod_processo
            ))
            cod_analise = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return cod_analise

def deletar(cod_analise: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETAR, (cod_analise,))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao deletar análise: {e}")
        return False