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

def deletar(cod_processo: int) -> bool:
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
    
def obter_todos() -> List[Processo]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cod_processo, codigo_edocs, numero_processo_florestal, codigo_empreendimento FROM Processo")
            registros = cursor.fetchall()
            cursor.close()
            return [Processo(
                cod_processo=r[0],
                codigo_edocs=r[1],
                numero_processo_florestal=r[2],
                codigo_empreendimento=r[3]
            ) for r in registros]
    except Exception as e:
        print(f"Erro ao obter processos: {e}")
        return []