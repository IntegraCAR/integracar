"""
Repositório para a entidade Status
"""

from typing import Optional, List
from datetime import datetime
from data.model.status import Status
from data.sql.status_sql import *
from util.database import get_connection

def criar_tabela() -> bool:
    """Cria a tabela Status no banco de dados"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao criar tabela Status: {e}")
        return False

def inserir(status: Status, cursor=None) -> Optional[int]:
    """
    Insere um novo status no banco
    
    Args:
        status: Objeto Status a ser inserido
        cursor: Cursor opcional para transações
        
    Returns:
        ID do status inserido ou None em caso de erro
    """
    if cursor is not None:
        cursor.execute(INSERIR, (
            status.tipo_status,
            status.data_hora_ultima_atualizacao or datetime.now()
        ))
        return cursor.fetchone()[0]
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                status.tipo_status,
                status.data_hora_ultima_atualizacao or datetime.now()
            ))
            cod_status = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return cod_status

def atualizar(status: Status) -> bool:
    """Atualiza um status existente"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                status.tipo_status,
                status.data_hora_ultima_atualizacao or datetime.now(),
                status.cod_status
            ))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao atualizar status: {e}")
        return False

def deletar(cod_status: int) -> bool:
    """Deleta um status pelo código"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETAR, (cod_status,))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao deletar status: {e}")
        return False

def obter_por_id(cod_status: int) -> Optional[Status]:
    """Obtém um status pelo código"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (cod_status,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return Status(
                    cod_status=row[0],
                    data_hora_ultima_atualizacao=row[1],
                    tipo_status=row[2]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter status: {e}")
        return None

def obter_todos() -> List[Status]:
    """Obtém todos os status"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS)
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                Status(
                    cod_status=row[0],
                    data_hora_ultima_atualizacao=row[1],
                    tipo_status=row[2]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter todos os status: {e}")
        return []

def obter_por_tipo(tipo: str) -> List[Status]:
    """Obtém todos os status de um determinado tipo"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_TIPO, (tipo,))
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                Status(
                    cod_status=row[0],
                    data_hora_ultima_atualizacao=row[1],
                    tipo_status=row[2]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter status por tipo: {e}")
        return []
