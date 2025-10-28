from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/consultor")
@requer_autenticacao(["consultor"])
async def get_consultor_home(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("consultor/consultor_home.html", {
        "request": request,
        "usuario": usuario_logado
    })
    return response