from typing import Optional, List
from data.model.analise_processos import AnaliseProcessos
from data.model.notificacao import Notificacao
from data.sql.analise_processos_sql import *
from util.database import get_connection


def _row_to_dict_detalhado(r):
    return {
        'cod_analise': r[0],
        'data_hora_inicio_analise': r[1],
        'data_previsao_fim_analise': r[2],
        'cod_processo': r[3],
        'cod_edocs': r[4],
        'num_processo_florestal': r[5],
        'cod_empreendimento': r[6],
        'cod_status': r[7],
        'tipo_status': r[8],
        'data_hora_ultima_atualizacao': r[9],
        'cod_usuario': r[10],
        'nome_usuario': r[11],
        'role_usuario': r[12],
        'cod_campus': r[13],
        'nome_campus': r[14],
        'cod_notificacao': r[15],
        'motivo_notificacao': r[16]
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


def atualizar(cod_processo: int, data_hora_inicio: str, data_previsao_fim: str, cod_status: int) -> Optional[int]:
    """Atualiza uma análise de processo existente e atualiza o status associado."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Mapear cod_status para tipo_status
            status_map = {
                1: "Análise iniciada – ainda sem parecer",
                2: "Aprovado – título emitido, mas não entregue",
                3: "Aprovado – título emitido e entregue",
                4: "Reprovado – notificação ao proprietário/possuidor pendente",
                5: "Reprovado – notificação ao proprietário/possuidor realizada"
            }
            
            tipo_status = status_map.get(cod_status, "Análise iniciada – ainda sem parecer")
            
            # Atualizar a análise do processo (apenas as datas)
            cursor.execute(ATUALIZAR, (
                data_hora_inicio,
                data_previsao_fim,
                cod_processo
            ))
            result = cursor.fetchone()
            if not result:
                return None
                
            cod_analise = result[0]
            cod_status_atual = result[1]
            
            # Atualizar o registro existente de Status
            cursor.execute(ATUALIZAR_STATUS_EXISTENTE, (tipo_status, cod_status_atual))
            
            conn.commit()
            cursor.close()
            return cod_analise
    except Exception as e:
        print(f"Erro ao atualizar análise: {e}")
        import traceback
        traceback.print_exc()
        return None


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
        print(f"Erro ao obter últimas por status: {e}")
        return []


def excluir(cod_processo: int) -> bool:
    """Exclui uma análise de processo do banco de dados."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM Analise_Processos WHERE cod_processo = %s",
                (cod_processo,)
            )
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao excluir análise: {e}")
        import traceback
        traceback.print_exc()
        return False


def obter_contagem_por_campus() -> List[dict]:
    """Retorna a contagem de processos por campus."""
    try:
        from data.sql.analise_processos_sql import CONTAGEM_POR_CAMPUS
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CONTAGEM_POR_CAMPUS)
            registros = cursor.fetchall()
            cursor.close()
            return [
                {
                    'nome_campus': r[0],
                    'quantidade': r[1]
                }
                for r in registros
            ]
    except Exception as e:
        print(f"Erro ao obter contagem por campus: {e}")
        return []


def obter_contagem_por_orientador() -> List[dict]:
    """Retorna a contagem de processos por orientador."""
    try:
        from data.sql.analise_processos_sql import CONTAGEM_POR_ORIENTADOR
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CONTAGEM_POR_ORIENTADOR)
            registros = cursor.fetchall()
            cursor.close()
            return [
                {
                    'nome_usuario': r[0],
                    'quantidade': r[1]
                }
                for r in registros
            ]
    except Exception as e:
        print(f"Erro ao obter contagem por orientador: {e}")
        return []


def obter_contagem_por_bolsista() -> List[dict]:
    """Retorna a contagem de processos por bolsista."""
    try:
        from data.sql.analise_processos_sql import CONTAGEM_POR_BOLSISTA
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CONTAGEM_POR_BOLSISTA)
            registros = cursor.fetchall()
            cursor.close()
            return [
                {
                    'nome_usuario': r[0],
                    'quantidade': r[1]
                }
                for r in registros
            ]
    except Exception as e:
        print(f"Erro ao obter contagem por bolsista: {e}")
        return []


def adicionar_notificacao(cod_processo: int, motivo_notificacao: str) -> Optional[int]:
    """Adiciona uma notificação e atualiza a análise do processo com ela"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Criar a notificação
            cursor.execute(
                "INSERT INTO Notificacao (motivo_notificacao) VALUES (%s) RETURNING cod_notificacao",
                (motivo_notificacao,)
            )
            cod_notificacao = cursor.fetchone()[0]
            
            # 2. Atualizar a análise do processo com a notificação
            cursor.execute(
                "UPDATE Analise_Processos SET cod_notificacao = %s WHERE cod_processo = %s",
                (cod_notificacao, cod_processo)
            )
            
            conn.commit()
            cursor.close()
            return cod_notificacao
    except Exception as e:
        print(f"Erro ao adicionar notificação: {e}")
        return None


def obter_ultimas_por_status() -> List[dict]:
    """Retorna a última atualização de cada tipo de status."""
    try:
        from data.sql.analise_processos_sql import ULTIMAS_POR_STATUS
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ULTIMAS_POR_STATUS)
            registros = cursor.fetchall()
            cursor.close()
            return [
                {
                    'tipo_status': r[0],
                    'ultima_atualizacao': r[1]
                }
                for r in registros
            ]
    except Exception as e:
        print(f"Erro ao obter últimas por status: {e}")
        return []