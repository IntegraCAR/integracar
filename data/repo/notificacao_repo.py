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

def obter_todos() -> List[Notificacao]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cod_notificacao, motivo_notificacao FROM Notificacao")
            registros = cursor.fetchall()
            cursor.close()
            return [Notificacao(
                cod_notificacao=r[0],
                motivo_notificacao=r[1]
            ) for r in registros]
    except Exception as e:
        print(f"Erro ao obter notificações: {e}")
        return []