from typing import Optional, List
from data.model.notificacao import Notificacao
from data.sql.notificacao_sql import *
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
        print(f"Erro ao criar tabela Notificacao: {e}")
        return False

def inserir(notificacao: Notificacao, cursor=None) -> Optional[int]:
    if cursor is not None:
        cursor.execute(INSERIR, (notificacao.motivo_notificacao,))
        return cursor.fetchone()[0]
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (notificacao.motivo_notificacao,))
            cod_notificacao = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return cod_notificacao

def atualizar(notificacao: Notificacao) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                notificacao.motivo_notificacao,
                notificacao.cod_notificacao
            ))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao atualizar notificação: {e}")
        return False

def deletar(cod_notificacao: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETAR, (cod_notificacao,))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao deletar notificação: {e}")
        return False

def obter_por_id(cod_notificacao: int) -> Optional[Notificacao]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (cod_notificacao,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return Notificacao(
                    cod_notificacao=row[0],
                    motivo_notificacao=row[1]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter notificação: {e}")
        return None

def obter_todos() -> List[Notificacao]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS)
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                Notificacao(
                    cod_notificacao=row[0],
                    motivo_notificacao=row[1]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter todas as notificações: {e}")
        return []
