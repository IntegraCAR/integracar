from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/orientador")
@requer_autenticacao(["orientador"])
async def get_orientador_home(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("orientador/orientador_home.html", {
        "request": request,
        "usuario": usuario_logado
    })
    return response