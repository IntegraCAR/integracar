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

def atualizar(campus: Campus) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                campus.nome_campus,
                campus.cod_campus
            ))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao atualizar campus: {e}")
        return False

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

def obter_por_id(cod_campus: int) -> Optional[Campus]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (cod_campus,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return Campus(
                    cod_campus=row[0],
                    nome_campus=row[1]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter campus: {e}")
        return None

def obter_todos() -> List[Campus]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS)
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                Campus(cod_campus=row[0], nome_campus=row[1])
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter todos os campus: {e}")
        return []

def buscar_por_nome(nome: str) -> List[Campus]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(BUSCAR_POR_NOME, (f"%{nome}%",))
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                Campus(cod_campus=row[0], nome_campus=row[1])
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao buscar campus por nome: {e}")
        return []
