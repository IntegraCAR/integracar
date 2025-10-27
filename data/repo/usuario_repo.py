from typing import Optional
from data.model.usuario import Usuario
from data.sql.usuario_sql import *
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
        print(f"Erro ao criar tabela Usuario: {e}")
        return False

def inserir(usuario: Usuario, cursor=None) -> Optional[int]:
    if cursor is not None:
        cursor.execute(INSERIR, (
            usuario.cod_campus,
            usuario.nome_usuario,
            usuario.role_usuario,
            usuario.organizacao_usuario
        ))
        return cursor.fetchone()[0]
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                usuario.cod_campus,
                usuario.nome_usuario,
                usuario.role_usuario,
                usuario.organizacao_usuario
            ))
            cod_usuario = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return cod_usuario

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                usuario.cod_campus,
                usuario.nome_usuario,
                usuario.role_usuario,
                usuario.organizacao_usuario,
                usuario.cod_usuario
            ))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
        return False

def deletar(cod_usuario: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETAR, (cod_usuario,))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")
        return False