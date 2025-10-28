from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/coordenador")
@requer_autenticacao(["coordenador"])
async def get_coordenador_home(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("coordenador/coordenador_home.html", {
        "request": request,
        "usuario": usuario_logado
    })
    return response