"""
Repositório para a entidade Usuario
"""

from typing import Optional, List
from data.model.usuario import Usuario
from data.sql.usuario_sql import *
from util.database import get_connection

def criar_tabela() -> bool:
    """Cria a tabela Usuario no banco de dados"""
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
    """
    Insere um novo usuário no banco
    
    Args:
        usuario: Objeto Usuario a ser inserido
        cursor: Cursor opcional para transações
        
    Returns:
        ID do usuário inserido ou None em caso de erro
    """
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

def atualizar(usuario: Usuario) -> bool:
    """Atualiza um usuário existente"""
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
    """Deleta um usuário pelo código"""
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

def obter_por_id(cod_usuario: int) -> Optional[Usuario]:
    """Obtém um usuário pelo código"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (cod_usuario,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return Usuario(
                    cod_usuario=row[0],
                    cod_campus=row[1],
                    nome_usuario=row[2],
                    role_usuario=row[3],
                    organizacao_usuario=row[4]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter usuário: {e}")
        return None

def obter_todos() -> List[Usuario]:
    """Obtém todos os usuários"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS)
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                Usuario(
                    cod_usuario=row[0],
                    cod_campus=row[1],
                    nome_usuario=row[2],
                    role_usuario=row[3],
                    organizacao_usuario=row[4]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter todos os usuários: {e}")
        return []

def obter_por_campus(cod_campus: int) -> List[Usuario]:
    """Obtém todos os usuários de um campus"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_CAMPUS, (cod_campus,))
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                Usuario(
                    cod_usuario=row[0],
                    cod_campus=row[1],
                    nome_usuario=row[2],
                    role_usuario=row[3],
                    organizacao_usuario=row[4]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter usuários por campus: {e}")
        return []

def buscar_por_nome(nome: str) -> List[Usuario]:
    """Busca usuários por nome (busca parcial, case-insensitive)"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(BUSCAR_POR_NOME, (f"%{nome}%",))
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                Usuario(
                    cod_usuario=row[0],
                    cod_campus=row[1],
                    nome_usuario=row[2],
                    role_usuario=row[3],
                    organizacao_usuario=row[4]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao buscar usuários por nome: {e}")
        return []

def obter_por_role(role: str) -> List[Usuario]:
    """Obtém todos os usuários de uma determinada role"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ROLE, (role,))
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                Usuario(
                    cod_usuario=row[0],
                    cod_campus=row[1],
                    nome_usuario=row[2],
                    role_usuario=row[3],
                    organizacao_usuario=row[4]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter usuários por role: {e}")
        return []
