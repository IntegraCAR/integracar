from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/gestor_administrativo")
@requer_autenticacao(["gestor_administrativo"])
async def get_gestor_administrativo_home(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("gestor_administrativo/gestor_administrativo_home.html", {
        "request": request,
        "usuario": usuario_logado
    })
    return response