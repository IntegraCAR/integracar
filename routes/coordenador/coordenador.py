from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import analise_processos_repo, status_repo
from util.auth_decorator import requer_autenticacao
from fastapi.responses import JSONResponse
from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class AtualizarAnaliseRequest(BaseModel):
    data_hora_inicio_analise: Optional[str] = Field(None, description="Data de início da análise")
    data_previsao_fim_analise: Optional[str] = Field(None, description="Data de previsão de fim")
    cod_status: int = Field(..., description="Código do status")
    
    class Config:
        # Permitir campos extras sem erro
        extra = "allow"

def serializar_datetime(obj):
    """Converte objetos datetime/date para string ISO format recursivamente"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: serializar_datetime(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serializar_datetime(item) for item in obj]
    return obj

@router.get("/coordenador")
@requer_autenticacao(["coordenador"])
async def get_coordenador_home(request: Request, usuario_logado: dict = None):
    obter_todos = analise_processos_repo.obter_todos_detalhado()
    contagem_por_status = analise_processos_repo.obter_contagem_por_status()
    ultimas_analises = analise_processos_repo.obter_ultimas_por_status()

    # Serializar datetime para string
    obter_todos_serializado = serializar_datetime(obter_todos)
    contagem_por_status_serializado = serializar_datetime(contagem_por_status)
    ultimas_analises_serializado = serializar_datetime(ultimas_analises)

    return JSONResponse(content={
        "usuario": usuario_logado, 
        "obter_todos": obter_todos_serializado, 
        "contagem_por_status": contagem_por_status_serializado, 
        "ultimas_analises": ultimas_analises_serializado
    })


@router.get("/processo/{cod_processo}", response_class=JSONResponse)
async def get_por_processo(cod_processo: int):
    por_processo = analise_processos_repo.obter_por_processo(cod_processo)
    por_processo_serializado = serializar_datetime(por_processo)
    return JSONResponse(content={"analises": por_processo_serializado})


@router.put("/processo/{cod_processo}")
async def atualizar_analise_processo(
    cod_processo: int,
    request: Request
):
    """Atualiza a análise de um processo"""
    try:
        # Pegar o JSON bruto primeiro
        body = await request.json()
        
        # Validar autenticação
        from util.auth_decorator import obter_usuario_logado
        usuario = obter_usuario_logado(request)
        if not usuario or usuario.get('role_usuario') != 'coordenador':
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "Não autorizado"}
            )
        
        # Extrair dados do body
        data_inicio = body.get('data_hora_inicio_analise', '')
        data_fim = body.get('data_previsao_fim_analise', '')
        cod_status = body.get('cod_status', 0)
        
        # Validar apenas o status (datas são opcionais)
        if not cod_status or cod_status <= 0:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Selecione um status válido"}
            )
        
        # Garantir que as datas estão no formato correto (se fornecidas)
        if data_inicio and 'T' in data_inicio:
            data_inicio = data_inicio.replace('T', ' ')
        if data_fim and 'T' in data_fim:
            data_fim = data_fim.replace('T', ' ')
        
        # Se as datas estiverem vazias, usar None
        data_inicio = data_inicio if data_inicio else None
        data_fim = data_fim if data_fim else None
        
        resultado = analise_processos_repo.atualizar(
            cod_processo=cod_processo,
            data_hora_inicio=data_inicio,
            data_previsao_fim=data_fim,
            cod_status=int(cod_status)
        )
        
        if resultado:
            return JSONResponse(content={
                "success": True,
                "message": "Análise atualizada com sucesso",
                "cod_analise": resultado
            })
        else:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Erro ao atualizar análise"}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Erro: {str(e)}"}
        )


@router.get("/status/listar")
@requer_autenticacao(["coordenador"])
async def listar_status(request: Request, usuario_logado: dict = None):
    """Lista todos os status disponíveis"""
    try:
        status_list = status_repo.obter_todos()
        status_serializado = serializar_datetime(status_list)
        return JSONResponse(content={"status": status_serializado})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro ao listar status: {str(e)}"}
        )
