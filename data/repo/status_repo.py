from typing import Optional, List
from datetime import datetime
from data.model.status import Status
from data.sql.status_sql import *
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
        print(f"Erro ao criar tabela Status: {e}")
        return False

def inserir(status: Status, cursor=None) -> Optional[int]:
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
        
def obter_todos() -> List[Status]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cod_status, data_hora_ultima_atualizacao, tipo_status FROM Status")
            registros = cursor.fetchall()
            cursor.close()
            return [Status(
                cod_status=r[0],
                data_hora_ultima_atualizacao=r[1],
                tipo_status=r[2]
            ) for r in registros]
    except Exception as e:
        print(f"Erro ao obter status: {e}")
        return []

def deletar(cod_status: int) -> bool:
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