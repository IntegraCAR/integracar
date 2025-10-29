from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/gestor-administrativo")
@requer_autenticacao(["gestor_administrativo"])
async def get_gestor_administrativo_home(request: Request, usuario_logado: dict = None):
    from fastapi.responses import JSONResponse
    return JSONResponse(content={"usuario": usuario_logado})