from typing import Optional, List
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
            usuario.cod_orientador,
            usuario.nome_usuario,
            usuario.email_usuario,
            usuario.senha_usuario,
            usuario.cpf_usuario,
            usuario.role_usuario,
            usuario.organizacao_usuario
        ))
        result = cursor.fetchone()
        return result[0] if result else None
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                usuario.cod_campus,
                usuario.cod_orientador,
                usuario.nome_usuario,
                usuario.email_usuario,
                usuario.senha_usuario,
                usuario.cpf_usuario,
                usuario.role_usuario,
                usuario.organizacao_usuario
            ))
            result = cursor.fetchone()
            cod_usuario = result[0] if result else None
            conn.commit()
            cursor.close()
            return cod_usuario
        
def atualizar(usuario: Usuario) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                usuario.cod_campus,
                usuario.cod_orientador,
                usuario.nome_usuario,
                usuario.email_usuario,
                usuario.senha_usuario,
                usuario.cpf_usuario,
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

def obter_todos() -> List[Usuario]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cod_usuario, cod_campus, cod_orientador, nome_usuario, email_usuario, senha_usuario, cpf_usuario, role_usuario, organizacao_usuario FROM Usuario")
            registros = cursor.fetchall()
            cursor.close()
            return [Usuario(
                cod_usuario=r[0],
                cod_campus=r[1],
                cod_orientador=r[2],
                nome_usuario=r[3],
                email_usuario=r[4],
                senha_usuario=r[5],
                cpf_usuario=r[6],
                role_usuario=r[7],
                organizacao_usuario=r[8]
            ) for r in registros]
    except Exception as e:
        print(f"Erro ao obter usuários: {e}")
        return []

def obter_por_email(email: str) -> Optional[Usuario]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_EMAIL, (email,))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado:
                return Usuario(
                    cod_usuario=resultado[0],
                    cod_campus=resultado[1],
                    cod_orientador=resultado[2],
                    nome_usuario=resultado[3],
                    email_usuario=resultado[4],
                    senha_usuario=resultado[5],
                    cpf_usuario=resultado[6],
                    role_usuario=resultado[7],
                    organizacao_usuario=resultado[8]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter usuário por email: {e}")
        return None

def obter_por_nome(nome: str) -> Optional[Usuario]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_NOME, (nome,))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado:
                return Usuario(
                    cod_usuario=resultado[0],
                    cod_campus=resultado[1],
                    cod_orientador=resultado[2],
                    nome_usuario=resultado[3],
                    email_usuario=resultado[4],
                    senha_usuario=resultado[5],
                    cpf_usuario=resultado[6],
                    role_usuario=resultado[7],
                    organizacao_usuario=resultado[8]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter usuário por nome: {e}")
        return None

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