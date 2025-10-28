from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import campus_repo, usuario_repo
from util.security import criar_hash_senha, verificar_senha
from fastapi.responses import RedirectResponse
from util.auth_decorator import criar_sessao, requer_autenticacao
from fastapi import Form, status

router = APIRouter()
templates = Jinja2Templates(directory="templates")

'''@router.get("/")
async def get_inicio(request: Request):
    campus = campus_repo.obter_todos()
    response = templates.TemplateResponse(
        "publico/inicio.html", 
        {
            "request": request,
            "campus": campus
        }
    )
    return response'''

# Rota de login
@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None)
):
    usuario = usuario_repo.obter_por_email(email)

    if not usuario or not verificar_senha(senha, usuario.senha):
        return templates.TemplateResponse(
            "publico/publico_login.html",
            {"request": request, "erro": "Email ou senha inválidos"}
        )

    # Criar sessão
    usuario_dict = {
        "cod_usuario": usuario.cod_usuario,
        "cod_campus": usuario.cod_campus,
        "cod_orientador": usuario.cod_orientador,
        "nome_usuario": usuario.nome_usuario,
        "email_usuario": usuario.email_usuario,
        "senha_usuario": usuario.senha_usuario,
        "cpf_usuario": usuario.cpf_usuario,
        "role_usuario": usuario.role_usuario,
        "organizacao_usuario": usuario.organizacao_usuario
    }
    criar_sessao(request, usuario_dict)
    print(usuario_dict)

    # Redirecionar
    if redirect:
        return RedirectResponse(redirect, status.HTTP_303_SEE_OTHER)

    #Um desse para cada perfil
    if usuario.role_usuario and usuario.role_usuario.strip().lower() == "bolsista":
        return RedirectResponse("/bolsista", status.HTTP_303_SEE_OTHER)

    if usuario.role_usuario and usuario.role_usuario.strip().lower() == "orientador":
        return RedirectResponse("/orientador", status.HTTP_303_SEE_OTHER)

    if usuario.role_usuario and usuario.role_usuario.strip().lower() == "consultor":
        return RedirectResponse("/consultor", status.HTTP_303_SEE_OTHER)

    if usuario.role_usuario and usuario.role_usuario.strip().lower() == "coordenador":
        return RedirectResponse("/coordenador", status.HTTP_303_SEE_OTHER)
    
    if usuario.role_usuario and usuario.role_usuario.strip().lower() == "gestor_tecnico":
        return RedirectResponse("/gestor_tecnico", status.HTTP_303_SEE_OTHER)

    if usuario.role_usuario and usuario.role_usuario.strip().lower() == "gestor_administrativo":
        return RedirectResponse("/gestor_administrativo", status.HTTP_303_SEE_OTHER)