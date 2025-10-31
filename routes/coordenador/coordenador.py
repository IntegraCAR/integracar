from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import analise_processos_repo
from util.auth_decorator import requer_autenticacao
from fastapi.responses import JSONResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/coordenador")
#@requer_autenticacao(["coordenador"])
async def get_coordenador_home(request: Request, usuario_logado: dict = None):
    obter_todos = analise_processos_repo.obter_todos_detalhado()
    contagem_por_status = analise_processos_repo.obter_contagem_por_status()
    ultimas_analises = analise_processos_repo.obter_ultimas_analises(10)

    return JSONResponse(content={"usuario": usuario_logado, "obter_todos": obter_todos, "contagem_por_status": contagem_por_status, "ultimas_analises": ultimas_analises})


@router.get("/processo/{cod_processo}", response_class=JSONResponse)
async def get_por_processo(cod_processo: int):
    por_processo = analise_processos_repo.obter_por_processo(cod_processo)
    return JSONResponse(content={"analises": por_processo,})