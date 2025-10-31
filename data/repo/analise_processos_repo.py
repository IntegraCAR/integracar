from typing import Optional, List
from data.model.analise_processos import AnaliseProcessos
from data.sql.analise_processos_sql import *
from util.database import get_connection


def _row_to_dict_detalhado(r):
    return {
        'cod_analise': r[0],
        'data_hora_inicio_analise': r[1],
        'data_previsao_fim_analise': r[2],
        'cod_processo': r[3],
        'numero_processo_florestal': r[4],
        'cod_status': r[5],
        'tipo_status': r[6],
        'data_hora_ultima_atualizacao_status': r[7],
        'cod_usuario': r[8],
        'nome_usuario': r[9],
        'cod_campus': r[10],
        'nome_campus': r[11],
        'cod_notificacao': r[12],
        'motivo_notificacao': r[13]
    }

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


def obter_todos_detalhado() -> List[dict]:
    """Retorna todas as análises com dados relacionados (processo, status, usuário, campus, notificação)."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS_DETALHADO)
            registros = cursor.fetchall()
            cursor.close()
            return [_row_to_dict_detalhado(r) for r in registros]
    except Exception as e:
        print(f"Erro ao obter análises detalhadas: {e}")
        return []


def obter_por_processo(cod_processo: int) -> List[dict]:
    """Retorna análises relacionadas a um processo específico."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_PROCESSO, (cod_processo,))
            registros = cursor.fetchall()
            cursor.close()
            return [_row_to_dict_detalhado(r) for r in registros]
    except Exception as e:
        print(f"Erro ao obter análises por processo: {e}")
        return []


def obter_contagem_por_status() -> List[dict]:
    """Retorna a quantidade de análises agrupadas por tipo de status."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CONTAGEM_POR_STATUS)
            registros = cursor.fetchall()
            cursor.close()
            return [{'tipo_status': r[0], 'quantidade': r[1] or 0} for r in registros]
    except Exception as e:
        print(f"Erro ao obter contagem por status: {e}")
        return []


def obter_ultimas_analises(limit: int = 10) -> List[dict]:
    """Retorna as últimas análises realizadas (limit configurável)."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ULTIMAS_ANALISES, (limit,))
            registros = cursor.fetchall()
            cursor.close()
            # map to a simpler dict
            return [
                {
                    'cod_analise': r[0],
                    'data_hora_inicio_analise': r[1],
                    'data_previsao_fim_analise': r[2],
                    'cod_processo': r[3],
                    'numero_processo_florestal': r[4],
                    'cod_status': r[5],
                    'tipo_status': r[6],
                    'cod_usuario': r[7],
                    'nome_usuario': r[8]
                }
                for r in registros
            ]
    except Exception as e:
        print(f"Erro ao obter últimas análises: {e}")
        return []