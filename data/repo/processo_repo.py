from typing import Optional, List
from data.model.processo import Processo
from data.sql.processo_sql import *
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
        print(f"Erro ao criar tabela Processo: {e}")
        return False

def inserir(processo: Processo, cursor=None) -> Optional[int]:
    """
    Insere um novo processo no banco
    
    Args:
        processo: Objeto Processo a ser inserido
        cursor: Cursor opcional para transações
        
    Returns:
        ID do processo inserido ou None em caso de erro
    """
    if cursor is not None:
        cursor.execute(INSERIR, (
            processo.codigo_edocs,
            processo.numero_processo_florestal,
            processo.codigo_empreendimento
        ))
        return cursor.fetchone()[0]
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                processo.codigo_edocs,
                processo.numero_processo_florestal,
                processo.codigo_empreendimento
            ))
            cod_processo = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return cod_processo

def atualizar(processo: Processo) -> bool:
    """Atualiza um processo existente"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                processo.codigo_edocs,
                processo.numero_processo_florestal,
                processo.codigo_empreendimento,
                processo.cod_processo
            ))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao atualizar processo: {e}")
        return False

def deletar(cod_processo: int) -> bool:
    """Deleta um processo pelo código"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETAR, (cod_processo,))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao deletar processo: {e}")
        return False

def obter_por_id(cod_processo: int) -> Optional[Processo]:
    """Obtém um processo pelo código"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (cod_processo,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return Processo(
                    cod_processo=row[0],
                    codigo_edocs=row[1],
                    numero_processo_florestal=row[2],
                    codigo_empreendimento=row[3]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter processo: {e}")
        return None

def obter_todos() -> List[Processo]:
    """Obtém todos os processos"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS)
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                Processo(
                    cod_processo=row[0],
                    codigo_edocs=row[1],
                    numero_processo_florestal=row[2],
                    codigo_empreendimento=row[3]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter todos os processos: {e}")
        return []

def buscar_por_edocs(codigo_edocs: str) -> List[Processo]:
    """Busca processos por código e-Docs (busca parcial)"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(BUSCAR_POR_EDOCS, (f"%{codigo_edocs}%",))
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                Processo(
                    cod_processo=row[0],
                    codigo_edocs=row[1],
                    numero_processo_florestal=row[2],
                    codigo_empreendimento=row[3]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao buscar processos por e-Docs: {e}")
        return []

def buscar_por_processo_florestal(numero: str) -> List[Processo]:
    """Busca processos por número do processo florestal (busca parcial)"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(BUSCAR_POR_PROCESSO_FLORESTAL, (f"%{numero}%",))
            rows = cursor.fetchall()
            cursor.close()
            
            return [
                Processo(
                    cod_processo=row[0],
                    codigo_edocs=row[1],
                    numero_processo_florestal=row[2],
                    codigo_empreendimento=row[3]
                )
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao buscar processos por número florestal: {e}")
        return []
