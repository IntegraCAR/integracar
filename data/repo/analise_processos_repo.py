from typing import Optional, List
from datetime import datetime
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

def atualizar(analise: AnaliseProcessos) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                analise.data_hora_inicio_analise,
                analise.data_previsao_fim_analise,
                analise.cod_campus,
                analise.cod_usuario,
                analise.cod_status,
                analise.cod_notificacao,
                analise.cod_processo,
                analise.cod_analise
            ))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao atualizar análise: {e}")
        return False

def atualizar_status(cod_analise: int, cod_status: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR_STATUS, (cod_status, cod_analise))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao atualizar status da análise: {e}")
        return False

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

def obter_por_id(cod_analise: int) -> Optional[AnaliseProcessos]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (cod_analise,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return AnaliseProcessos(
                    cod_analise=row[0],
                    data_hora_inicio_analise=row[1],
                    data_previsao_fim_analise=row[2],
                    cod_campus=row[3],
                    cod_usuario=row[4],
                    cod_status=row[5],
                    cod_notificacao=row[6],
                    cod_processo=row[7]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter análise: {e}")
        return None

def obter_todos() -> List[AnaliseProcessos]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS)
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                AnaliseProcessos(
                    cod_analise=row[0],
                    data_hora_inicio_analise=row[1],
                    data_previsao_fim_analise=row[2],
                    cod_campus=row[3],
                    cod_usuario=row[4],
                    cod_status=row[5],
                    cod_notificacao=row[6],
                    cod_processo=row[7]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter todas as análises: {e}")
        return []

def obter_por_campus(cod_campus: int) -> List[AnaliseProcessos]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_CAMPUS, (cod_campus,))
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                AnaliseProcessos(
                    cod_analise=row[0],
                    data_hora_inicio_analise=row[1],
                    data_previsao_fim_analise=row[2],
                    cod_campus=row[3],
                    cod_usuario=row[4],
                    cod_status=row[5],
                    cod_notificacao=row[6],
                    cod_processo=row[7]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter análises por campus: {e}")
        return []

def obter_por_usuario(cod_usuario: int) -> List[AnaliseProcessos]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_USUARIO, (cod_usuario,))
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                AnaliseProcessos(
                    cod_analise=row[0],
                    data_hora_inicio_analise=row[1],
                    data_previsao_fim_analise=row[2],
                    cod_campus=row[3],
                    cod_usuario=row[4],
                    cod_status=row[5],
                    cod_notificacao=row[6],
                    cod_processo=row[7]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter análises por usuário: {e}")
        return []

def obter_por_status(cod_status: int) -> List[AnaliseProcessos]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_STATUS, (cod_status,))
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                AnaliseProcessos(
                    cod_analise=row[0],
                    data_hora_inicio_analise=row[1],
                    data_previsao_fim_analise=row[2],
                    cod_campus=row[3],
                    cod_usuario=row[4],
                    cod_status=row[5],
                    cod_notificacao=row[6],
                    cod_processo=row[7]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter análises por status: {e}")
        return []

def obter_por_processo(cod_processo: int) -> List[AnaliseProcessos]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_PROCESSO, (cod_processo,))
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                AnaliseProcessos(
                    cod_analise=row[0],
                    data_hora_inicio_analise=row[1],
                    data_previsao_fim_analise=row[2],
                    cod_campus=row[3],
                    cod_usuario=row[4],
                    cod_status=row[5],
                    cod_notificacao=row[6],
                    cod_processo=row[7]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter análises por processo: {e}")
        return []

def obter_atrasadas() -> List[AnaliseProcessos]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_ATRASADAS)
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                AnaliseProcessos(
                    cod_analise=row[0],
                    data_hora_inicio_analise=row[1],
                    data_previsao_fim_analise=row[2],
                    cod_campus=row[3],
                    cod_usuario=row[4],
                    cod_status=row[5],
                    cod_notificacao=row[6],
                    cod_processo=row[7]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter análises atrasadas: {e}")
        return []
