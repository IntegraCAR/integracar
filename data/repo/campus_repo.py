from typing import Optional, List
from data.model.campus import Campus
from data.sql.campus_sql import *
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
        print(f"Erro ao criar tabela Campus: {e}")
        return False

def inserir(campus: Campus, cursor=None) -> Optional[int]:
    if cursor is not None:
        cursor.execute(INSERIR, (campus.nome_campus,))
        return cursor.fetchone()[0]
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (campus.nome_campus,))
            cod_campus = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return cod_campus

def deletar(cod_campus: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETAR, (cod_campus,))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao deletar campus: {e}")
        return False
